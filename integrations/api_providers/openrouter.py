from typing import Dict, Any, List
from .base import BaseAPIProvider
import requests
import json

class OpenRouterProvider(BaseAPIProvider):
    """OpenRouter API提供商"""
    
    def __init__(self, api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        super().__init__(api_key, base_url)
        self.models = [
            "openai/gpt-3.5-turbo",
            "openai/gpt-4",
            "anthropic/claude-3-haiku",
            "anthropic/claude-3-sonnet",
            "google/gemini-pro",
            "meta-llama/llama-3-8b",
            "mistralai/mistral-7b-instruct"
        ]
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.models
    
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到OpenRouter API"""
        # 如果没有提供API密钥，返回模拟响应
        if not self.api_key or self.api_key == "sk-xxx":
            return {
                "model": model,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"这是来自OpenRouter API ({model}) 的模拟响应"
                        }
                    }
                ]
            }
        
        # 实际的API调用
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 1000)
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # 如果API调用失败，返回模拟响应
            return {
                "model": model,
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": f"这是来自OpenRouter API ({model}) 的模拟响应（API调用失败: {str(e)}）"
                        }
                    }
                ]
            }
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        return bool(self.api_key) and self.api_key != "sk-xxx"