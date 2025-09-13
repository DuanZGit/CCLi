from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.model_router import ModelRouter
from core.personal_profile import PersonalProfile
from core.event_logger import EventLogger
from core.knowledge_graph import KnowledgeGraph

app = FastAPI(title="CCLi Web UI", description="Claude Code CLI Web Interface")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化核心组件
model_router = ModelRouter()
personal_profile = PersonalProfile(user_id="web_user")
event_logger = EventLogger()
knowledge_graph = KnowledgeGraph()

# 存储活跃的WebSocket连接
active_connections = []

@app.get("/", response_class=HTMLResponse)
async def get():
    """返回主页面"""
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>CCLi - Claude Code CLI</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    overflow: hidden;
                }
                .header {
                    background-color: #2c3e50;
                    color: white;
                    padding: 20px;
                    text-align: center;
                }
                .chat-container {
                    display: flex;
                    height: 70vh;
                }
                .sidebar {
                    width: 250px;
                    background-color: #ecf0f1;
                    padding: 20px;
                    border-right: 1px solid #bdc3c7;
                }
                .main-content {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                }
                .chat-history {
                    flex: 1;
                    padding: 20px;
                    overflow-y: auto;
                    border-bottom: 1px solid #bdc3c7;
                }
                .message {
                    margin-bottom: 15px;
                    padding: 10px;
                    border-radius: 5px;
                }
                .user-message {
                    background-color: #3498db;
                    color: white;
                    text-align: right;
                }
                .ai-message {
                    background-color: #ecf0f1;
                    color: #2c3e50;
                }
                .input-area {
                    padding: 20px;
                    display: flex;
                }
                .task-selector {
                    margin-right: 10px;
                    padding: 10px;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                }
                .message-input {
                    flex: 1;
                    padding: 10px;
                    border: 1px solid #bdc3c7;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .send-button {
                    margin-left: 10px;
                    padding: 10px 20px;
                    background-color: #3498db;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .send-button:hover {
                    background-color: #2980b9;
                }
                .sidebar-section {
                    margin-bottom: 20px;
                }
                .sidebar-title {
                    font-weight: bold;
                    margin-bottom: 10px;
                    color: #2c3e50;
                }
                .sidebar-item {
                    padding: 5px 0;
                    cursor: pointer;
                }
                .sidebar-item:hover {
                    color: #3498db;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>CCLi - Claude Code CLI</h1>
                    <p>智能个人助理系统</p>
                </div>
                
                <div class="chat-container">
                    <div class="sidebar">
                        <div class="sidebar-section">
                            <div class="sidebar-title">任务类型</div>
                            <div class="sidebar-item" onclick="setTaskType('default')">默认任务</div>
                            <div class="sidebar-item" onclick="setTaskType('background')">后台任务</div>
                            <div class="sidebar-item" onclick="setTaskType('think')">思考任务</div>
                            <div class="sidebar-item" onclick="setTaskType('longContext')">长上下文</div>
                            <div class="sidebar-item" onclick="setTaskType('coding')">编程任务</div>
                        </div>
                        
                        <div class="sidebar-section">
                            <div class="sidebar-title">用户画像</div>
                            <div id="user-profile">加载中...</div>
                        </div>
                        
                        <div class="sidebar-section">
                            <div class="sidebar-title">知识图谱</div>
                            <div id="knowledge-graph">加载中...</div>
                        </div>
                    </div>
                    
                    <div class="main-content">
                        <div class="chat-history" id="chat-history">
                            <div class="message ai-message">
                                欢迎使用 CCLi 系统！我是您的智能个人助理。<br>
                                您可以开始与我对话，我会根据任务类型选择最合适的AI模型为您服务。
                            </div>
                        </div>
                        
                        <div class="input-area">
                            <select class="task-selector" id="task-type">
                                <option value="default">默认任务</option>
                                <option value="background">后台任务</option>
                                <option value="think">思考任务</option>
                                <option value="longContext">长上下文</option>
                                <option value="coding">编程任务</option>
                            </select>
                            <input type="text" class="message-input" id="message-input" placeholder="输入您的消息...">
                            <button class="send-button" onclick="sendMessage()">发送</button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                let currentTaskType = "default";
                let ws = null;
                
                // 连接到WebSocket
                function connectWebSocket() {
                    ws = new WebSocket("ws://localhost:8000/ws");
                    
                    ws.onopen = function(event) {
                        console.log("WebSocket连接已建立");
                    };
                    
                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        if (data.type === "chat") {
                            addMessageToChat(data.content, "ai");
                        } else if (data.type === "profile") {
                            document.getElementById("user-profile").innerHTML = JSON.stringify(data.content, null, 2);
                        } else if (data.type === "knowledge") {
                            document.getElementById("knowledge-graph").innerHTML = JSON.stringify(data.content, null, 2);
                        }
                    };
                    
                    ws.onclose = function(event) {
                        console.log("WebSocket连接已关闭，尝试重新连接...");
                        setTimeout(connectWebSocket, 3000);
                    };
                }
                
                // 设置任务类型
                function setTaskType(taskType) {
                    currentTaskType = taskType;
                    document.getElementById("task-type").value = taskType;
                }
                
                // 发送消息
                function sendMessage() {
                    const input = document.getElementById("message-input");
                    const message = input.value.trim();
                    
                    if (message && ws && ws.readyState === WebSocket.OPEN) {
                        const data = {
                            type: "chat",
                            task_type: currentTaskType,
                            content: message
                        };
                        
                        ws.send(JSON.stringify(data));
                        addMessageToChat(message, "user");
                        input.value = "";
                    }
                }
                
                // 添加消息到聊天历史
                function addMessageToChat(message, sender) {
                    const chatHistory = document.getElementById("chat-history");
                    const messageDiv = document.createElement("div");
                    messageDiv.className = `message ${sender}-message`;
                    messageDiv.innerHTML = message.replace(/\\n/g, "<br>");
                    chatHistory.appendChild(messageDiv);
                    chatHistory.scrollTop = chatHistory.scrollHeight;
                }
                
                // 处理回车键发送消息
                document.getElementById("message-input").addEventListener("keypress", function(event) {
                    if (event.key === "Enter") {
                        sendMessage();
                    }
                });
                
                // 页面加载完成后连接WebSocket
                window.onload = function() {
                    connectWebSocket();
                };
            </script>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data["type"] == "chat":
                # 处理聊天消息
                task_type = message_data.get("task_type", "default")
                content = message_data["content"]
                
                # 记录事件
                event_logger.log_event(f"用户发送消息: {content}")
                
                # 发送请求到模型路由
                response = model_router.send_request(task_type, content)
                
                # 解析响应
                if "choices" in response:
                    # OpenAI格式
                    ai_response = response["choices"][0]["message"]["content"]
                elif "content" in response:
                    # Anthropic格式
                    ai_response = response["content"][0]["text"]
                elif "candidates" in response:
                    # Gemini格式
                    ai_response = response["candidates"][0]["content"]["parts"][0]["text"]
                elif "message" in response:
                    # Ollama格式
                    ai_response = response["message"]["content"]
                else:
                    # 模拟响应
                    ai_response = response.get("response", "无法解析响应")
                
                # 发送响应给客户端
                await websocket.send_text(json.dumps({
                    "type": "chat",
                    "content": ai_response
                }))
                
                # 更新用户画像
                profile_summary = personal_profile.get_profile_summary()
                await websocket.send_text(json.dumps({
                    "type": "profile",
                    "content": profile_summary
                }))
                
                # 更新知识图谱
                graph_summary = knowledge_graph.get_graph_summary()
                await websocket.send_text(json.dumps({
                    "type": "knowledge",
                    "content": graph_summary
                }))
                
    except WebSocketDisconnect:
        active_connections.remove(websocket)
    except Exception as e:
        print(f"WebSocket错误: {e}")
        await websocket.send_text(json.dumps({
            "type": "error",
            "content": str(e)
        }))

@app.get("/api/profile")
async def get_profile():
    """获取用户画像"""
    return personal_profile.get_profile_summary()

@app.get("/api/knowledge-graph")
async def get_knowledge_graph():
    """获取知识图谱"""
    return knowledge_graph.get_graph_summary()

@app.get("/api/routes")
async def get_routes():
    """获取路由信息"""
    return {
        "providers": model_router.providers,
        "routes": model_router.routes
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)