"""
Web界面插件
基于 siteboon/claudecodeui 的整合实现
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(project_root, "plugins"))

from plugins.model_router import ModelRouterPlugin

app = FastAPI(title="Claude Code CCLi Web UI", description="Claude Code CLI with CCLi Extensions Web Interface")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化路由插件
router_plugin = ModelRouterPlugin()

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
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Claude Code CCLi Web UI</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
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
                border-radius: 4px;
            }
            .routing-btn {
                background-color: #2196F3;
            }
            .claude-btn {
                background-color: #9C27B0;
            }
            #output { 
                border: 1px solid #ccc; 
                padding: 20px; 
                margin-top: 20px; 
                background-color: #f9f9f9; 
                min-height: 200px; 
                max-height: 400px;
                overflow-y: auto;
                border-radius: 4px;
            }
            .input-group {
                margin: 20px 0;
                display: flex;
                gap: 10px;
            }
            #message-input {
                flex: 1;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            #send-btn {
                padding: 10px 20px;
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                border-radius: 4px;
            }
            h1 { color: #333; }
            h2 { color: #666; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Claude Code CCLi Web UI</h1>
            <p>基于Anthropic Claude Code CLI，集成智能路由和UI扩展</p>
            
            <h2>Claude Code原生功能</h2>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('analyze')">分析代码库</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('plan')">制定计划</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('doc')">生成文档</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('test')">生成测试</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('review')">代码审查</button>
            
            <h2>智能路由功能</h2>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('default', 'Hello, AI!')">默认模型</button>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('think', '解释量子计算的概念')">思考模型</button>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('coding', '用Python写一个快速排序算法')">编程模型</button>
            
            <h2>自定义消息</h2>
            <div class="input-group">
                <select id="mode-select">
                    <option value="claude">Claude Code模式</option>
                    <option value="routing">智能路由模式</option>
                </select>
                <select id="task-type">
                    <option value="default">默认</option>
                    <option value="think">思考</option>
                    <option value="coding">编程</option>
                    <option value="claudeCode">Claude Code</option>
                </select>
                <input type="text" id="message-input" placeholder="输入您的消息...">
                <button id="send-btn" onclick="sendMessage()">发送</button>
            </div>
            
            <div id="output">
                <p>欢迎使用Claude Code CCLi Web UI!</p>
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
            
            function sendClaudeCommand(command) {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        "type": "claude_command",
                        "command": command
                    }));
                }
            }
            
            function sendRoutingCommand(taskType, message) {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        "type": "routing_command",
                        "task_type": taskType,
                        "message": message
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
                
                if (mode === 'claude') {
                    sendClaudeCommand(message);
                } else {
                    sendRoutingCommand(taskType, message);
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
                    response = router_plugin.send_request(task_type, content)
                    
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "智能路由模式",
                        "content": response.get("response", str(response))
                    }), websocket)
                except Exception as e:
                    await manager.send_personal_message(json.dumps({
                        "type": "response",
                        "mode": "智能路由模式",
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
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket错误: {e}")
        await manager.send_personal_message(json.dumps({
            "type": "error",
            "content": str(e)
        }), websocket)

def handle_claude_command(command: str) -> str:
    """处理Claude Code命令"""
    # 模拟Claude Code功能
    responses = {
        "analyze": "代码库分析完成：\n文件数: 42\n目录数: 8\n总大小: 1.2 MB",
        "plan": "实施计划：\n1. 需求分析\n2. 技术选型\n3. 架构设计\n4. 实现步骤\n5. 测试策略",
        "doc": "文档生成完成：\n已创建 README.md\n已创建 API文档\n已创建 开发指南",
        "test": "测试代码生成完成：\n已生成单元测试\n已生成集成测试\n已生成端到端测试",
        "review": "代码审查结果：\n- 代码风格符合规范\n- 潜在问题已识别\n- 改进建议已提供"
    }
    
    return responses.get(command, f"执行Claude Code命令: {command}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)