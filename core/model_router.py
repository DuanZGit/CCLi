import json
import os
from typing import Dict, Any
from integrations.api_providers import (
    OpenAIProvider, 
    AnthropicProvider,
    OpenRouterProvider,
    DeepSeekProvider,
    OllamaProvider,
    GeminiProvider
)

# 尝试导入Claude Code集成（如果可用）
try:
    from integrations.claude_code import ClaudeCodeAPI, ClaudeCodeIntegration
    CLAUDE_CODE_AVAILABLE = True
except ImportError:
    CLAUDE_CODE_AVAILABLE = False
    print("Claude Code集成不可用，将使用模拟响应")

class ModelRouter:
    def __init__(self, config_path: str = None):
        """
        模型路由系统
        基于 Claude Code Router 的核心功能设计
        """
        self.config = {}
        self.providers = {}
        self.routes = {}
        self.provider_instances = {}
        self.claude_code_api = None
        self.claude_code_integration = None
        self.load_config(config_path)
        
        # 初始化Claude Code集成（如果可用）
        if CLAUDE_CODE_AVAILABLE:
            try:
                self.claude_code_api = ClaudeCodeAPI()
                self.claude_code_integration = ClaudeCodeIntegration()
                print("Claude Code集成已初始化")
            except Exception as e:
                print(f"Claude Code集成初始化失败: {e}")

    def load_config(self, config_path: str = None):
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.expanduser("~/.ccli/config.json")
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            
            self.providers = self.config.get("Providers", {})
            self.routes = self.config.get("Router", {})
            print(f"模型路由配置加载成功: {config_path}")
        else:
            print("未找到配置文件，使用默认配置")
            self._set_default_config()
        
        # 初始化提供商实例
        self._initialize_provider_instances()

    def _set_default_config(self):
        """设置默认配置"""
        self.providers = {
            "openai": {
                "name": "openai",
                "api_base_url": "https://api.openai.com/v1",
                "api_key": "sk-xxx",
                "models": ["gpt-3.5-turbo", "gpt-4"]
            },
            "anthropic": {
                "name": "anthropic",
                "api_base_url": "https://api.anthropic.com/v1",
                "api_key": "sk-xxx",
                "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"]
            },
            "openrouter": {
                "name": "openrouter",
                "api_base_url": "https://openrouter.ai/api/v1",
                "api_key": "sk-xxx",
                "models": ["openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet"]
            },
            "deepseek": {
                "name": "deepseek",
                "api_base_url": "https://api.deepseek.com/v1",
                "api_key": "sk-xxx",
                "models": ["deepseek-chat", "deepseek-coder"]
            },
            "ollama": {
                "name": "ollama",
                "api_base_url": "http://localhost:11434/api",
                "api_key": "",
                "models": ["llama3", "codellama"]
            },
            "gemini": {
                "name": "gemini",
                "api_base_url": "https://generativelanguage.googleapis.com/v1beta",
                "api_key": "sk-xxx",
                "models": ["gemini-pro", "gemini-1.5-pro"]
            }
        }
        self.routes = {
            "default": "openai,gpt-3.5-turbo",
            "background": "ollama,llama3",
            "think": "anthropic,claude-3-sonnet-20240229",
            "longContext": "gemini,gemini-1.5-pro",
            "coding": "deepseek,deepseek-coder",
            "claudeCode": "anthropic,claude-3-opus-20240229"
        }

    def _initialize_provider_instances(self):
        """初始化提供商实例"""
        for provider_name, provider_config in self.providers.items():
            api_key = provider_config.get("api_key", "")
            base_url = provider_config.get("api_base_url", "")
            
            if provider_name == "openai":
                self.provider_instances[provider_name] = OpenAIProvider(
                    api_key=api_key, base_url=base_url
                )
            elif provider_name == "anthropic":
                self.provider_instances[provider_name] = AnthropicProvider(
                    api_key=api_key, base_url=base_url
                )
            elif provider_name == "openrouter":
                self.provider_instances[provider_name] = OpenRouterProvider(
                    api_key=api_key, base_url=base_url
                )
            elif provider_name == "deepseek":
                self.provider_instances[provider_name] = DeepSeekProvider(
                    api_key=api_key, base_url=base_url
                )
            elif provider_name == "ollama":
                self.provider_instances[provider_name] = OllamaProvider(
                    api_key=api_key, base_url=base_url
                )
            elif provider_name == "gemini":
                self.provider_instances[provider_name] = GeminiProvider(
                    api_key=api_key, base_url=base_url
                )
            # 可以在这里添加更多提供商的初始化逻辑

    def get_provider_for_task(self, task_type: str = "default") -> Dict[str, Any]:
        """
        根据任务类型获取对应的提供商配置
        """
        # 特殊处理Claude Code任务类型
        if task_type == "claudeCode" and CLAUDE_CODE_AVAILABLE and self.claude_code_api:
            return {
                "name": "claudeCode",
                "type": "claudeCode",
                "api_key": os.getenv("CLAUDE_API_KEY", "sk-xxx")
            }
        
        route = self.routes.get(task_type, self.routes.get("default"))
        if not route:
            # 如果没有找到路由，返回默认提供商
            return list(self.providers.values())[0] if self.providers else {}
        
        # 解析路由格式 "provider,model"
        parts = route.split(",", 1)
        provider_name = parts[0]
        
        # 查找提供商配置
        for name, provider in self.providers.items():
            if provider.get("name") == provider_name:
                provider_config = provider.copy()
                if len(parts) > 1:
                    provider_config["model"] = parts[1]
                return provider_config
        
        # 如果没有找到指定的提供商，返回默认提供商
        return list(self.providers.values())[0] if self.providers else {}

    def route_request(self, task_type: str, prompt: str) -> Dict[str, Any]:
        """
        路由请求到合适的模型
        """
        provider_config = self.get_provider_for_task(task_type)
        provider_name = provider_config.get("name", "openai")
        
        # 特殊处理Claude Code
        if provider_name == "claudeCode":
            request_data = {
                "prompt": prompt,
                "model": "claude-3-opus-20240229",
                "max_tokens": 1000,
                "temperature": 0.7
            }
        else:
            model = provider_config.get("model", "gpt-3.5-turbo")
            request_data = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": 1000
            }
        
        return {
            "provider": provider_config,
            "request": request_data,
            "provider_instance": self.provider_instances.get(provider_name) if provider_name != "claudeCode" else None
        }

    def add_provider(self, name: str, api_base_url: str, api_key: str, models: list):
        """添加新的提供商"""
        provider = {
            "name": name,
            "api_base_url": api_base_url,
            "api_key": api_key,
            "models": models
        }
        self.providers[name] = provider
        print(f"已添加提供商: {name}")

    def update_route(self, task_type: str, provider_name: str, model: str):
        """更新路由配置"""
        route_key = f"{provider_name},{model}"
        self.routes[task_type] = route_key
        print(f"已更新路由: {task_type} -> {route_key}")

    def send_request(self, task_type: str, prompt: str) -> Dict[str, Any]:
        """
        发送请求到路由选择的模型
        """
        routed_request = self.route_request(task_type, prompt)
        provider_config = routed_request["provider"]
        provider_name = provider_config.get("name", "openai")
        
        # 特殊处理Claude Code
        if provider_name == "claudeCode":
            if CLAUDE_CODE_AVAILABLE and self.claude_code_api:
                # 使用真实的Claude Code API
                api_key = provider_config.get("api_key", "")
                if api_key and api_key != "sk-xxx":
                    self.claude_code_api.set_api_key(api_key)
                
                request_data = routed_request["request"]
                response = self.claude_code_api.send_message(
                    prompt=request_data["prompt"],
                    model=request_data["model"],
                    max_tokens=request_data["max_tokens"],
                    temperature=request_data["temperature"]
                )
                return response
            else:
                # 返回模拟响应
                return {
                    "model": "claude-3-opus-20240229",
                    "response": f"[Claude Code模拟响应] {prompt}",
                    "type": "claudeCode"
                }
        
        # 处理其他提供商
        provider_instance = routed_request.get("provider_instance")
        if provider_instance:
            model = routed_request["request"]["model"]
            messages = routed_request["request"]["messages"]
            response = provider_instance.send_request(model, messages)
            return response
        else:
            # 如果没有提供商实例，返回模拟响应
            return {
                "model": routed_request["request"]["model"],
                "response": f"这是针对任务类型 '{task_type}' 的模拟响应"
            }