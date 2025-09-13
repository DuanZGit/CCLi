from abc import ABC, abstractmethod
from typing import Dict, Any, List

class BaseAPIProvider(ABC):
    """API提供商基类"""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    @abstractmethod
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        pass
    
    @abstractmethod
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到API"""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        pass

class OpenAIProvider(BaseAPIProvider):
    """OpenAI API提供商"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        super().__init__(api_key, base_url)
        self.models = [
            "gpt-3.5-turbo",
            "gpt-4",
            "gpt-4-turbo",
            "gpt-4o"
        ]
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.models
    
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到OpenAI API"""
        # 这里应该实现实际的API调用
        # 为简化起见，我们返回模拟响应
        return {
            "model": model,
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": "这是来自OpenAI API的模拟响应"
                    }
                }
            ]
        }
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        # 这里应该实现实际的验证逻辑
        return bool(self.api_key)

class AnthropicProvider(BaseAPIProvider):
    """Anthropic API提供商"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com/v1"):
        super().__init__(api_key, base_url)
        self.models = [
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229",
            "claude-3-opus-20240229"
        ]
    
    def get_models(self) -> List[str]:
        """获取可用模型列表"""
        return self.models
    
    def send_request(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """发送请求到Anthropic API"""
        # 这里应该实现实际的API调用
        # 为简化起见，我们返回模拟响应
        return {
            "model": model,
            "content": [
                {
                    "type": "text",
                    "text": "这是来自Anthropic API的模拟响应"
                }
            ]
        }
    
    def validate_config(self) -> bool:
        """验证配置是否有效"""
        # 这里应该实现实际的验证逻辑
        return bool(self.api_key)