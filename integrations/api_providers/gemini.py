from typing import Dict, Any, List
from .base import BaseAPIProvider
import requests
import json

class GeminiProvider(BaseAPIProvider):
    """Gemini API提供商"""
    
    def __init__(self, api_key: str, base_url: str = "https://generativelanguage.googleapis.com/v1beta"):
        super().__init__(api_key, base_url)
        self.models = [
            "gemini-pro",
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-1.0-pro"
        ]
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.models
    
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到Gemini API"""
        # 如果没有提供API密钥，返回模拟响应
        if not self.api_key or self.api_key == "sk-xxx":
            return {
                "model": model,
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "text": f"这是来自Gemini API ({model}) 的模拟响应"
                                }
                            ]
                        }
                    }
                ]
            }
        
        # 将OpenAI格式的消息转换为Gemini格式
        gemini_messages = []
        for msg in messages:
            gemini_messages.append({
                "role": "user" if msg["role"] == "user" else "model",
                "parts": [{"text": msg["content"]}]
            })
        
        # 实际的API调用
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": gemini_messages,
            "generationConfig": {
                "temperature": kwargs.get("temperature", 0.7),
                "maxOutputTokens": kwargs.get("max_tokens", 1000)
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}:generateContent?key={self.api_key}",
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
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {
                                    "text": f"这是来自Gemini API ({model}) 的模拟响应（API调用失败: {str(e)}）"
                                }
                            ]
                        }
                    }
                ]
            }
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        return bool(self.api_key) and self.api_key != "sk-xxx"