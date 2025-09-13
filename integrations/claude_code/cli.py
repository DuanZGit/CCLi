import subprocess
import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Optional

class ClaudeCodeCLI:
    """Claude Code命令行工具集成类"""
    
    def __init__(self, claude_path: str = "claude"):
        """
        初始化Claude Code CLI
        
        Args:
            claude_path: Claude命令行工具的路径
        """
        self.claude_path = claude_path
        self.temp_dir = Path(tempfile.gettempdir()) / "ccli_temp"
        self.temp_dir.mkdir(exist_ok=True)
    
    def check_installation(self) -> bool:
        """
        检查Claude Code是否已安装
        
        Returns:
            是否已安装
        """
        try:
            result = subprocess.run(
                [self.claude_path, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def send_prompt(self, prompt: str, headless: bool = True) -> Dict[str, Any]:
        """
        发送提示给Claude Code
        
        Args:
            prompt: 提示文本
            headless: 是否使用无头模式
            
        Returns:
            Claude Code的响应
        """
        try:
            cmd = [self.claude_path]
            if headless:
                cmd.extend(["-p", prompt])
            else:
                # 交互模式需要更复杂的处理
                return {
                    "error": "Interactive mode not supported in this integration",
                    "message": "Please use headless mode (-p flag)"
                }
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=os.getcwd()
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "output": "",
                "error": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1
            }
    
    def analyze_project(self) -> Dict[str, Any]:
        """
        分析项目结构
        
        Returns:
            项目分析结果
        """
        prompt = """/init
        
        请分析当前项目的结构并提供详细的报告。"""
        
        return self.send_prompt(prompt)
    
    def generate_documentation(self, doc_type: str = "readme") -> Dict[str, Any]:
        """
        生成项目文档
        
        Args:
            doc_type: 文档类型
            
        Returns:
            生成的文档
        """
        prompts = {
            "readme": "请为当前项目生成README.md文件，包括项目描述、安装说明、使用方法和贡献指南。",
            "api": "请为当前项目生成API文档，详细描述所有公共接口和使用方法。",
            "contributing": "请为当前项目生成贡献指南，包括开发流程、代码规范和提交要求。"
        }
        
        prompt = prompts.get(doc_type, prompts["readme"])
        return self.send_prompt(prompt)
    
    def run_tests(self) -> Dict[str, Any]:
        """
        运行项目测试
        
        Returns:
            测试结果
        """
        prompt = """请运行项目中的所有测试并报告结果。
        
        如果测试失败，请提供详细的错误信息和修复建议。"""
        
        return self.send_prompt(prompt)
    
    def fix_linting_issues(self) -> Dict[str, Any]:
        """
        修复代码规范问题
        
        Returns:
            修复结果
        """
        prompt = """请检查项目中的代码规范问题并自动修复。
        
        使用适当的linter工具，修复发现的所有问题。"""
        
        return self.send_prompt(prompt)
    
    def create_branch(self, branch_name: str, base_branch: str = "main") -> Dict[str, Any]:
        """
        创建Git分支
        
        Args:
            branch_name: 分支名称
            base_branch: 基础分支
            
        Returns:
            操作结果
        """
        prompt = f"""请创建一个新的Git分支：
        
        分支名称：{branch_name}
        基础分支：{base_branch}
        
        确保分支创建成功并切换到新分支。"""
        
        return self.send_prompt(prompt)
    
    def commit_changes(self, message: str) -> Dict[str, Any]:
        """
        提交代码变更
        
        Args:
            message: 提交信息
            
        Returns:
            提交结果
        """
        prompt = f"""请提交当前的所有代码变更：
        
        提交信息：{message}
        
        确保所有相关文件都被正确提交。"""
        
        return self.send_prompt(prompt)
    
    def create_pull_request(self, title: str, description: str = "") -> Dict[str, Any]:
        """
        创建Pull Request
        
        Args:
            title: PR标题
            description: PR描述
            
        Returns:
            创建结果
        """
        prompt = f"""请创建一个Pull Request：
        
        标题：{title}
        描述：{description}
        
        确保PR包含所有相关变更的详细说明。"""
        
        return self.send_prompt(prompt)
    
    def review_code(self) -> Dict[str, Any]:
        """
        代码审查
        
        Returns:
            审查结果
        """
        prompt = """请对当前项目进行代码审查：
        
        1. 检查代码质量和可读性
        2. 识别潜在的性能问题
        3. 发现安全漏洞
        4. 提供改进建议
        5. 确保遵循最佳实践"""
        
        return self.send_prompt(prompt)
    
    def optimize_performance(self) -> Dict[str, Any]:
        """
        性能优化
        
        Returns:
            优化建议
        """
        prompt = """请分析当前项目的性能并提供优化建议：
        
        1. 识别性能瓶颈
        2. 提供具体的优化方案
        3. 估计优化后的性能提升
        4. 给出实施优先级建议"""
        
        return self.send_prompt(prompt)
    
    def generate_plan(self, task: str) -> Dict[str, Any]:
        """
        生成任务计划
        
        Args:
            task: 任务描述
            
        Returns:
            任务计划
        """
        prompt = f"""[Shift+Tab]
        
        请为以下任务生成详细的实施计划：
        
        任务：{task}
        
        要求：
        1. 列出所有必要的步骤
        2. 估计每个步骤的时间
        3. 识别潜在的风险和挑战
        4. 提供备选方案
        5. 给出成功标准"""
        
        return self.send_prompt(prompt)

# 使用示例
if __name__ == "__main__":
    # 初始化CLI集成
    cli = ClaudeCodeCLI()
    
    # 检查安装
    if cli.check_installation():
        print("Claude Code is installed")
        
        # 生成README
        result = cli.generate_documentation("readme")
        print("README Generation Result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("Claude Code is not installed or not in PATH")