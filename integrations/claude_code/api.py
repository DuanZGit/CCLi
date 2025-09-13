from typing import Dict, Any, List, Optional
import requests
import json
import os
from pathlib import Path

class ClaudeCodeAPI:
    """Claude Code API集成类"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://api.anthropic.com/v1"):
        """
        初始化Claude Code API
        
        Args:
            api_key: API密钥
            base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("CLAUDE_API_KEY")
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "CCLi/1.0",
        }
        
        if self.api_key:
            self.headers["X-API-Key"] = self.api_key
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
        self.headers["X-API-Key"] = api_key
    
    def send_message(self, prompt: str, model: str = "claude-3-opus-20240229", 
                     max_tokens: int = 1000, temperature: float = 0.7) -> Dict[str, Any]:
        """
        发送消息到Claude API
        
        Args:
            prompt: 提示文本
            model: 模型名称
            max_tokens: 最大token数
            temperature: 温度参数
            
        Returns:
            API响应
        """
        if not self.api_key:
            return {
                "error": "API key not configured",
                "message": "Please set your Claude API key"
            }
        
        url = f"{self.base_url}/messages"
        
        data = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API request failed with status {response.status_code}",
                    "message": response.text
                }
        except Exception as e:
            return {
                "error": "API request failed",
                "message": str(e)
            }
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        分析代码
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            代码分析结果
        """
        prompt = f"""请分析以下{language}代码并提供详细的分析报告：

{code}

请包括以下内容：
1. 代码功能概述
2. 潜在问题和改进建议
3. 性能优化建议
4. 安全性考虑
5. 代码质量评分（1-10分）

请以结构化的方式提供您的分析。"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def generate_code(self, description: str, language: str = "python") -> Dict[str, Any]:
        """
        根据描述生成代码
        
        Args:
            description: 代码功能描述
            language: 目标编程语言
            
        Returns:
            生成的代码
        """
        prompt = f"""请为以下功能描述生成{language}代码：

功能描述：{description}

要求：
1. 生成完整可运行的代码
2. 包含必要的注释
3. 遵循最佳编程实践
4. 包含错误处理
5. 提供使用示例

请只返回代码，不要包含其他解释。"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def refactor_code(self, code: str, refactor_instruction: str, language: str = "python") -> Dict[str, Any]:
        """
        重构代码
        
        Args:
            code: 原始代码
            refactor_instruction: 重构指令
            language: 编程语言
            
        Returns:
            重构后的代码
        """
        prompt = f"""请根据以下指令重构{language}代码：

重构指令：{refactor_instruction}

原始代码：
{code}

要求：
1. 保持原有功能不变
2. 提高代码质量和可读性
3. 遵循最佳编程实践
4. 添加必要的注释
5. 只返回重构后的代码，不要包含其他解释"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def debug_code(self, code: str, error_message: str, language: str = "python") -> Dict[str, Any]:
        """
        调试代码
        
        Args:
            code: 代码内容
            error_message: 错误信息
            language: 编程语言
            
        Returns:
            调试建议
        """
        prompt = f"""请帮助调试以下{language}代码中的错误：

错误信息：{error_message}

代码：
{code}

请提供：
1. 错误原因分析
2. 具体的修复建议
3. 修复后的完整代码
4. 如何避免类似错误的建议"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def explain_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        解释代码
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            代码解释
        """
        prompt = f"""请详细解释以下{language}代码的功能和实现原理：

代码：
{code}

请包括：
1. 代码功能概述
2. 逐行解释关键部分
3. 使用的算法或设计模式
4. 可能的改进点
5. 相关的最佳实践"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def generate_tests(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        为代码生成测试
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            生成的测试代码
        """
        prompt = f"""请为以下{language}代码生成单元测试：

代码：
{code}

要求：
1. 使用标准的测试框架
2. 覆盖主要功能和边界情况
3. 包含测试说明
4. 只返回测试代码，不要包含其他解释"""
        
        return self.send_message(prompt, max_tokens=2000)
    
    def review_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        代码审查
        
        Args:
            code: 代码内容
            language: 编程语言
            
        Returns:
            审查结果
        """
        prompt = f"""请对以下{language}代码进行代码审查：

代码：
{code}

请从以下方面进行审查：
1. 代码质量和可读性
2. 性能优化建议
3. 安全性问题
4. 最佳实践遵循情况
5. 潜在的bug
6. 改进建议

请提供具体的建议和修改方案。"""
        
        return self.send_message(prompt, max_tokens=2000)

# 使用示例
if __name__ == "__main__":
    # 初始化API
    api = ClaudeCodeAPI()
    
    # 如果有API密钥，可以设置
    # api.set_api_key("your-api-key-here")
    
    # 示例：生成代码
    result = api.generate_code("创建一个计算两个数之和的函数")
    print("Generated Code:")
    print(json.dumps(result, indent=2, ensure_ascii=False))