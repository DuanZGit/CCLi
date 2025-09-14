from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from integrations.claude_code import ClaudeCodeIntegration

app = FastAPI(title="CCLi Web UI", description="Claude Code CLI Web Interface")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# 初始化模板
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    # 如果没有模板目录，创建一个简单的HTML响应
    templates = None

# 初始化Claude Code集成
claude_code_integration = ClaudeCodeIntegration()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """返回主页面"""
    if templates:
        return templates.TemplateResponse("index.html", {"request": request})
    else:
        # 简单的HTML页面
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>CCLi Web UI</title>
            <meta charset="utf-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .command-btn { 
                    background-color: #4CAF50; 
                    border: none; 
                    color: white; 
                    padding: 15px 32px; 
                    text-align: center; 
                    text-decoration: none; 
                    display: inline-block; 
                    font-size: 16px; 
                    margin: 4px 2px; 
                    cursor: pointer; 
                }
                #output { 
                    border: 1px solid #ccc; 
                    padding: 20px; 
                    margin-top: 20px; 
                    background-color: #f9f9f9; 
                    min-height: 200px; 
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CCLi Web UI - Claude Code模式</h1>
                <p>直接进入Claude Code项目，无需复杂命令</p>
                
                <button class="command-btn" onclick="sendCommand('analyze')">分析代码库</button>
                <button class="command-btn" onclick="sendCommand('plan')">制定计划</button>
                <button class="command-btn" onclick="sendCommand('doc')">生成文档</button>
                <button class="command-btn" onclick="sendCommand('test')">生成测试</button>
                <button class="command-btn" onclick="sendCommand('review')">代码审查</button>
                
                <div id="output">
                    <p>欢迎使用CCLi Web UI!</p>
                    <p>点击上面的按钮开始使用Claude Code功能。</p>
                </div>
            </div>

            <script>
                let ws = new WebSocket("ws://localhost:8000/ws");
                
                ws.onmessage = function(event) {
                    const output = document.getElementById('output');
                    output.innerHTML += '<p>' + event.data + '</p>';
                    output.scrollTop = output.scrollHeight;
                };
                
                function sendCommand(command) {
                    const output = document.getElementById('output');
                    output.innerHTML += '<p>执行命令: ' + command + '</p>';
                    
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({
                            "type": "claude_command",
                            "command": command
                        }));
                    } else {
                        output.innerHTML += '<p>WebSocket连接未建立</p>';
                    }
                }
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "claude_command":
                command = message_data.get("command", "")
                response = handle_claude_command(command)
                
                # 发送响应给客户端
                await manager.send_personal_message(response, websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket错误: {e}")
        await manager.send_personal_message(f"错误: {str(e)}", websocket)

def handle_claude_command(command: str) -> str:
    """处理Claude Code命令"""
    try:
        if command == "analyze":
            analysis = claude_code_integration.analyze_codebase()
            return f"代码库分析完成：\\n文件数: {len(analysis.get('files', []))}\\n目录数: {len(analysis.get('directories', []))}\\n总大小: {analysis.get('size', 0)} bytes"
        elif command == "plan":
            plan = claude_code_integration.plan_implementation("用户请求的功能实现")
            return f"实施计划：\\n{plan}"
        elif command == "doc":
            doc = claude_code_integration.generate_documentation("项目功能说明", "readme")
            return f"文档生成完成：\\n{doc}"
        elif command == "test":
            # 这里应该生成测试代码的示例
            return "测试代码生成功能已调用。在完整实现中，将生成针对项目代码的单元测试。"
        elif command == "review":
            review = claude_code_integration.review_code()
            return f"代码审查结果：\\n{review}"
        else:
            return f"未知的Claude Code命令: {command}"
    except Exception as e:
        return f"执行Claude Code命令时出错: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)