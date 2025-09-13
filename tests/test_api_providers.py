import unittest
import sys
import os

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from integrations.api_providers import (
    OpenRouterProvider,
    DeepSeekProvider,
    OllamaProvider,
    GeminiProvider
)

class TestAPIProviders(unittest.TestCase):

    def test_openrouter_provider(self):
        """测试OpenRouter提供商"""
        provider = OpenRouterProvider(api_key="sk-xxx")
        self.assertIn("openai/gpt-3.5-turbo", provider.get_models())
        
        # 测试模拟响应
        response = provider.send_request("openai/gpt-3.5-turbo", [{"role": "user", "content": "Hello"}])
        self.assertIn("choices", response)
        print("OpenRouter提供商测试通过。")

    def test_deepseek_provider(self):
        """测试DeepSeek提供商"""
        provider = DeepSeekProvider(api_key="sk-xxx")
        self.assertIn("deepseek-chat", provider.get_models())
        
        # 测试模拟响应
        response = provider.send_request("deepseek-chat", [{"role": "user", "content": "Hello"}])
        self.assertIn("choices", response)
        print("DeepSeek提供商测试通过。")

    def test_ollama_provider(self):
        """测试Ollama提供商"""
        provider = OllamaProvider()
        self.assertIn("llama3", provider.get_models())
        
        # 测试模拟响应
        response = provider.send_request("llama3", [{"role": "user", "content": "Hello"}])
        self.assertTrue("message" in response or "choices" in response)
        print("Ollama提供商测试通过。")

    def test_gemini_provider(self):
        """测试Gemini提供商"""
        provider = GeminiProvider(api_key="sk-xxx")
        self.assertIn("gemini-pro", provider.get_models())
        
        # 测试模拟响应
        response = provider.send_request("gemini-pro", [{"role": "user", "content": "Hello"}])
        self.assertTrue("candidates" in response or "choices" in response)
        print("Gemini提供商测试通过。")

if __name__ == '__main__':
    unittest.main()