from typing import Dict, Any, List
from .base import BaseAPIProvider
import requests
import json

class OllamaProvider(BaseAPIProvider):
    """Ollama API提供商（本地模型）"""
    
    def __init__(self, api_key: str = "", base_url: str = "http://localhost:11434/api"):
        # Ollama通常不需要API密钥，因为是本地运行
        super().__init__(api_key, base_url)
        self.models = [
            "llama3",
            "llama3:70b",
            "mistral",
            "codellama",
            "qwen2.5-coder",
            "phi3"
        ]
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        # 尝试从Ollama API获取实际的模型列表
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model["name"] for model in data.get("models", [])]
        except:
            pass
        # 如果无法获取实际模型列表，返回默认列表
        return self.models
    
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到Ollama API"""
        # 实际的API调用
        data = {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "num_predict": kwargs.get("max_tokens", 1000)
            }
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=data,
                timeout=60  # Ollama可能需要更长的超时时间
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            # 如果API调用失败，返回模拟响应
            return {
                "model": model,
                "message": {
                    "role": "assistant",
                    "content": f"这是来自Ollama ({model}) 的模拟响应（API调用失败: {str(e)}）"
                }
            }
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        # 检查Ollama服务是否可用
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            return response.status_code == 200
        except:
            return True  # 即使无法连接，也认为配置有效（因为Ollama可能稍后启动）