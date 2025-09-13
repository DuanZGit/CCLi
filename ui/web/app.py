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
from core.personal_profile import PersonalProfile
from core.event_logger import EventLogger
from core.knowledge_graph import KnowledgeGraph

# 尝试导入Claude Code集成
try:
    from integrations.claude_code import ClaudeCodeIntegration
    CLAUDE_CODE_AVAILABLE = True
except ImportError:
    CLAUDE_CODE_AVAILABLE = False
    print("Claude Code集成不可用")

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
app.mount("/static", StaticFiles(directory="ui/web/static"), name="static")

# 初始化模板
templates = Jinja2Templates(directory="ui/web/templates")

# 初始化核心组件
model_router = ModelRouter()
personal_profile = PersonalProfile(user_id="web_user")
event_logger = EventLogger()
knowledge_graph = KnowledgeGraph()

# 初始化Claude Code集成（如果可用）
claude_code_integration = None
if CLAUDE_CODE_AVAILABLE:
    try:
        claude_code_integration = ClaudeCodeIntegration()
        print("Claude Code集成已初始化")
    except Exception as e:
        print(f"Claude Code集成初始化失败: {e}")

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

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    """返回主页面"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/chat", response_class=HTMLResponse)
async def get_chat(request: Request):
    """返回聊天页面"""
    return templates.TemplateResponse("chat.html", {"request": request})

@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request):
    """返回用户画像页面"""
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/knowledge", response_class=HTMLResponse)
async def get_knowledge(request: Request):
    """返回知识图谱页面"""
    return templates.TemplateResponse("knowledge.html", {"request": request})

@app.get("/settings", response_class=HTMLResponse)
async def get_settings(request: Request):
    """返回设置页面"""
    return templates.TemplateResponse("settings.html", {"request": request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket端点"""
    await manager.connect(websocket)
    
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
                ai_response = parse_model_response(response)
                
                # 发送响应给客户端
                await manager.send_personal_message(json.dumps({
                    "type": "chat",
                    "content": ai_response,
                    "task_type": task_type
                }), websocket)
                
                # 更新用户画像
                profile_summary = personal_profile.get_profile_summary()
                await manager.send_personal_message(json.dumps({
                    "type": "profile",
                    "content": profile_summary
                }), websocket)
                
                # 更新知识图谱
                graph_summary = knowledge_graph.get_graph_summary()
                await manager.send_personal_message(json.dumps({
                    "type": "knowledge",
                    "content": graph_summary
                }), websocket)
                
            elif message_data["type"] == "claude_command":
                # 处理Claude Code命令
                if CLAUDE_CODE_AVAILABLE and claude_code_integration:
                    command = message_data.get("command", "")
                    response = handle_claude_command(command, claude_code_integration)
                    
                    # 发送响应给客户端
                    await manager.send_personal_message(json.dumps({
                        "type": "chat",
                        "content": response,
                        "task_type": "claudeCode"
                    }), websocket)
                else:
                    # Claude Code不可用
                    await manager.send_personal_message(json.dumps({
                        "type": "chat",
                        "content": "Claude Code功能不可用，请检查集成配置。",
                        "task_type": "claudeCode"
                    }), websocket)
                
            elif message_data["type"] == "get_claude_status":
                # 获取Claude Code状态
                await manager.send_personal_message(json.dumps({
                    "type": "claude_status",
                    "content": CLAUDE_CODE_AVAILABLE and claude_code_integration is not None
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

def handle_claude_command(command: str, claude_integration) -> str:
    """处理Claude Code命令"""
    try:
        if command == "analyze":
            analysis = claude_integration.analyze_codebase()
            return f"代码库分析完成：\n文件数: {len(analysis.get('files', []))}\n目录数: {len(analysis.get('directories', []))}\n总大小: {analysis.get('size', 0)} bytes"
        elif command == "plan":
            plan = claude_integration.plan_implementation("用户请求的功能实现")
            return f"实施计划：\n{plan}"
        elif command == "doc":
            doc = claude_integration.generate_documentation("项目功能说明", "readme")
            return f"文档生成完成：\n{doc}"
        elif command == "test":
            # 这里应该生成测试代码的示例
            return "测试代码生成功能已调用。在完整实现中，将生成针对项目代码的单元测试。"
        else:
            return f"未知的Claude Code命令: {command}"
    except Exception as e:
        return f"执行Claude Code命令时出错: {str(e)}"

@app.get("/api/profile")
async def get_profile_api():
    """获取用户画像API"""
    return personal_profile.get_profile_summary()

@app.get("/api/knowledge-graph")
async def get_knowledge_graph_api():
    """获取知识图谱API"""
    return knowledge_graph.get_graph_summary()

@app.get("/api/routes")
async def get_routes_api():
    """获取路由信息API"""
    return {
        "providers": model_router.providers,
        "routes": model_router.routes
    }

@app.get("/api/models")
async def get_models_api():
    """获取可用模型API"""
    models = {}
    for provider_name, provider_instance in model_router.provider_instances.items():
        models[provider_name] = provider_instance.get_models()
    return models

@app.get("/api/claude-status")
async def get_claude_status_api():
    """获取Claude Code状态API"""
    return {
        "available": CLAUDE_CODE_AVAILABLE,
        "integrated": claude_code_integration is not None
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)