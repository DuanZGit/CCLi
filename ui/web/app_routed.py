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

from core.model_router import ModelRouter
from integrations.claude_code import ClaudeCodeIntegration

app = FastAPI(title="CCLi Web UI", description="Claude Code CLI with Model Routing Web Interface")

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

# 初始化核心组件
model_router = ModelRouter()
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
                .claude-btn {
                    background-color: #2196F3;
                }
                .routing-btn {
                    background-color: #FF9800;
                }
                #output { 
                    border: 1px solid #ccc; 
                    padding: 20px; 
                    margin-top: 20px; 
                    background-color: #f9f9f9; 
                    min-height: 200px; 
                    max-height: 400px;
                    overflow-y: auto;
                }
                .input-group {
                    margin: 20px 0;
                }
                #message-input {
                    width: 70%;
                    padding: 10px;
                    font-size: 16px;
                }
                #send-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CCLi Web UI - Claude Code with Model Routing</h1>
                <p>智能模型路由的Claude Code界面</p>
                
                <h2>路由模式 (Model Routing)</h2>
                <button class="command-btn routing-btn" onclick="sendRoutingCommand('default', '')">默认模型</button>
                <button class="command-btn routing-btn" onclick="sendRoutingCommand('think', '解释量子计算的概念')">思考模型</button>
                <button class="command-btn routing-btn" onclick="sendRoutingCommand('coding', '用Python写一个快速排序算法')">编程模型</button>
                <button class="command-btn routing-btn" onclick="sendRoutingCommand('longContext', '总结这份长文档的主要内容')">长文本模型</button>
                
                <h2>Claude Code模式</h2>
                <button class="command-btn claude-btn" onclick="sendClaudeCommand('analyze')">分析代码库</button>
                <button class="command-btn claude-btn" onclick="sendClaudeCommand('plan')">制定计划</button>
                <button class="command-btn claude-btn" onclick="sendClaudeCommand('doc')">生成文档</button>
                <button class="command-btn claude-btn" onclick="sendClaudeCommand('test')">生成测试</button>
                <button class="command-btn claude-btn" onclick="sendClaudeCommand('review')">代码审查</button>
                
                <h2>自定义消息</h2>
                <div class="input-group">
                    <select id="mode-select">
                        <option value="mode">路由模式</option>
                        <option value="claude">Claude Code模式</option>
                    </select>
                    <select id="task-type">
                        <option value="default">默认</option>
                        <option value="think">思考</option>
                        <option value="coding">编程</option>
                        <option value="longContext">长文本</option>
                        <option value="claudeCode">Claude Code</option>
                    </select>
                    <input type="text" id="message-input" placeholder="输入您的消息...">
                    <button id="send-btn" onclick="sendMessage()">发送</button>
                </div>
                
                <div id="output">
                    <p>欢迎使用CCLi Web UI!</p>
                    <p>选择上面的按钮或输入自定义消息开始使用。</p>
                </div>
            </div>

            <script>
                let ws = new WebSocket("ws://localhost:8000/ws");
                
                ws.onmessage = function(event) {
                    const output = document.getElementById('output');
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'response') {
                        output.innerHTML += '<p><strong>' + data.mode + '响应:</strong></p>';
                        output.innerHTML += '<p>' + data.content + '</p>';
                    } else {
                        output.innerHTML += '<p>' + event.data + '</p>';
                    }
                    
                    output.scrollTop = output.scrollHeight;
                };
                
                ws.onopen = function(event) {
                    document.getElementById('output').innerHTML += '<p>WebSocket连接已建立</p>';
                };
                
                function sendRoutingCommand(taskType, message) {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({
                            "type": "routing_command",
                            "task_type": taskType,
                            "message": message || "Hello, AI!"
                        }));
                    }
                }
                
                function sendClaudeCommand(command) {
                    if (ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({
                            "type": "claude_command",
                            "command": command
                        }));
                    }
                }
                
                function sendMessage() {
                    const mode = document.getElementById('mode-select').value;
                    const taskType = document.getElementById('task-type').value;
                    const message = document.getElementById('message-input').value;
                    
                    if (!message) {
                        alert('请输入消息');
                        return;
                    }
                    
                    if (mode === 'routing') {
                        sendRoutingCommand(taskType, message);
                    } else {
                        if (ws.readyState === WebSocket.OPEN) {
                            ws.send(JSON.stringify({
                                "type": "claude_message",
                                "task_type": taskType,
                                "message": message
                            }));
                        }
                    }
                    
                    document.getElementById('message-input').value = '';
                }
                
                // 回车发送消息
                document.getElementById('message-input').addEventListener('keypress', function(e) {
                    if (e.key === 'Enter') {
                        sendMessage();
                    }
                });
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
            
            if message_data["type"] == "routing_command":
                # 处理路由命令
                task_type = message_data.get("task_type", "default")
                content = message_data["message"]
                
                try:
                    response = model_router.send_request(task_type, content)
                    ai_response = parse_model_response(response)
                    
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "路由模式",
                        "content": ai_response
                    }), websocket)
                except Exception as e:
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "路由模式",
                        "content": f"错误: {str(e)}"
                    }), websocket)
                    
            elif message_data["type"] == "claude_command":
                # 处理Claude Code命令
                command = message_data.get("command", "")
                response = handle_claude_command(command)
                
                await manager.send_personal_message(json.dumps({
                    "type": "response",
                    "mode": "Claude Code模式",
                    "content": response
                }), websocket)
                
            elif message_data["type"] == "claude_message":
                # 处理Claude Code消息
                task_type = message_data.get("task_type", "claudeCode")
                content = message_data["message"]
                
                try:
                    response = claude_code_integration.send_prompt(content, task_type)
                    
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "Claude Code模式",
                        "content": response
                    }), websocket)
                except Exception as e:
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "Claude Code模式",
                        "content": f"错误: {str(e)}"
                    }), websocket)
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket错误: {e}")
        await manager.send_personal_message(json.dumps({
            "type": "error",
            "content": str(e)
        }), websocket)

def parse_model_response(response: dict) -> str:
    """解析模型响应"""
    if "choices" in response:
        # OpenAI格式
        return response["choices"][0]["message"]["content"]
    elif "content" in response:
        # Anthropic格式
        return response["content"][0]["text"]
    elif "candidates" in response:
        # Gemini格式
        return response["candidates"][0]["content"]["parts"][0]["text"]
    elif "message" in response:
        # Ollama格式
        return response["message"]["content"]
    elif "response" in response:
        # 模拟响应或Claude Code响应
        return response["response"]
    else:
        # 未知格式
        return json.dumps(response, ensure_ascii=False, indent=2)

def handle_claude_command(command: str) -> str:
    """处理Claude Code命令"""
    try:
        if command == "analyze":
            analysis = claude_code_integration.analyze_codebase()
            return f"代码库分析完成：\n文件数: {len(analysis.get('files', []))}\n目录数: {len(analysis.get('directories', []))}\n总大小: {analysis.get('size', 0)} bytes"
        elif command == "plan":
            plan = claude_code_integration.plan_implementation("用户请求的功能实现")
            return f"实施计划：\n{plan}"
        elif command == "doc":
            doc = claude_code_integration.generate_documentation("项目功能说明", "readme")
            return f"文档生成完成：\n{doc}"
        elif command == "test":
            # 这里应该生成测试代码的示例
            return "测试代码生成功能已调用。在完整实现中，将生成针对项目代码的单元测试。"
        elif command == "review":
            review = claude_code_integration.review_code()
            return f"代码审查结果：\n{review}"
        else:
            return f"未知的Claude Code命令: {command}"
    except Exception as e:
        return f"执行Claude Code命令时出错: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)