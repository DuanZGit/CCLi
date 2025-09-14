#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
UI扩展插件
为Claude Code CLI添加Web界面支持
基于 siteboon/claudecodeui 项目整合
"""

import argparse
import sys
import os
import subprocess
from typing import Dict, Any

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

class UIExtension:
    """UI扩展插件"""
    
    def __init__(self):
        self.web_ui_process = None
    
    def add_cli_arguments(self, parser: argparse.ArgumentParser):
        """添加CLI参数"""
        parser.add_argument("--route", "-r", action="store_true",
                          help="使用智能路由模式")
        parser.add_argument("--web", "-w", action="store_true",
                          help="启动Web界面")
        parser.add_argument("--task", "-t", default="default",
                          help="任务类型 (default, think, coding, longContext, claudeCode)")
        return parser
    
    def handle_web_command(self):
        """处理Web界面命令"""
        print("正在启动Web UI...")
        try:
            # 导入Web UI模块
            web_ui_path = os.path.join(project_root, "plugins", "ui", "web_interface", "app.py")
            if os.path.exists(web_ui_path):
                # 使用子进程启动Web UI
                self.web_ui_process = subprocess.Popen([sys.executable, web_ui_path])
                print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
            else:
                print("错误: 找不到Web UI文件")
        except Exception as e:
            print(f"启动Web UI时出错: {e}")
    
    def stop_web_ui(self):
        """停止Web界面"""
        if self.web_ui_process:
            self.web_ui_process.terminate()
            print("Web UI已停止")

# Web应用（简化版）
web_app_content = '''
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from plugins.router.routing_engine.engine import ModelRouter

app = FastAPI(title="Claude Code UI", description="Claude Code CLI with Web Interface")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化路由引擎
model_router = ModelRouter()

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
        <title>Claude Code Web UI</title>
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
            <h1>Claude Code Web UI</h1>
            <p>基于Anthropic Claude Code CLI的Web界面</p>
            
            <h2>Claude Code模式</h2>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('analyze')">分析代码库</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('plan')">制定计划</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('doc')">生成文档</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('test')">生成测试</button>
            <button class="command-btn claude-btn" onclick="sendClaudeCommand('review')">代码审查</button>
            
            <h2>智能路由模式</h2>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('default', '')">默认模型</button>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('think', '解释量子计算的概念')">思考模型</button>
            <button class="command-btn routing-btn" onclick="sendRoutingCommand('coding', '用Python写一个快速排序算法')">编程模型</button>
            
            <h2>自定义消息</h2>
            <div class="input-group">
                <select id="mode-select">
                    <option value="claude">Claude Code模式</option>
                    <option value="routing">路由模式</option>
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
                <p>欢迎使用Claude Code Web UI!</p>
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
                        "message": message || "Hello, AI!"
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
                    response = model_router.send_request(task_type, content)
                    ai_response = response.get("response", str(response))
                    
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
                # 处理Claude Code命令（模拟）
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
    """处理Claude Code命令（模拟）"""
    try:
        if command == "analyze":
            return "代码库分析完成：\n文件数: 45\n目录数: 12\n总大小: 185623 bytes"
        elif command == "plan":
            return "实施计划：\n1. 需求分析\n2. 技术选型\n3. 架构设计\n4. 实现步骤\n5. 测试策略"
        elif command == "doc":
            return "文档生成完成：\n# API文档\n## 接口说明\n### 请求参数\n### 响应格式"
        elif command == "test":
            return "测试代码生成功能已调用。在完整实现中，将生成针对项目代码的单元测试。"
        elif command == "review":
            return "代码审查结果：\n- 代码风格符合规范\n- 潜在问题已识别\n- 改进建议已提供"
        else:
            return f"未知的Claude Code命令: {command}"
    except Exception as e:
        return f"执行Claude Code命令时出错: {str(e)}"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
'''

def create_web_app():
    """创建Web应用文件"""
    web_app_path = os.path.join(project_root, "plugins", "ui", "web_interface", "app.py")
    if not os.path.exists(web_app_path):
        os.makedirs(os.path.dirname(web_app_path), exist_ok=True)
        with open(web_app_path, 'w', encoding='utf-8') as f:
            f.write(web_app_content)
        print(f"Web应用文件已创建: {web_app_path}")

# 插件注册函数
def register_plugin(cli_app):
    """注册插件到CLI应用"""
    ui_ext = UIExtension()
    
    # 创建Web应用文件
    create_web_app()
    
    print("UI扩展插件已注册")
    return ui_ext