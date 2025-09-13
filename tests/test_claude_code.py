import unittest
import sys
import os

# 将项目根目录添加到Python路径中，以便导入模块
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestClaudeCodeIntegration(unittest.TestCase):

    def test_claude_code_import(self):
        """测试Claude Code模块导入"""
        try:
            from integrations.claude_code import ClaudeCodeIntegration
            claude = ClaudeCodeIntegration()
            self.assertIsNotNone(claude)
            print("Claude Code集成模块导入测试通过。")
        except ImportError:
            self.skipTest("Claude Code集成模块不可用")
        except Exception as e:
            self.fail(f"Claude Code集成模块导入失败: {e}")

    def test_claude_code_api_import(self):
        """测试Claude Code API模块导入"""
        try:
            from integrations.claude_code import ClaudeCodeAPI
            api = ClaudeCodeAPI()
            self.assertIsNotNone(api)
            print("Claude Code API模块导入测试通过。")
        except ImportError:
            self.skipTest("Claude Code API模块不可用")
        except Exception as e:
            self.fail(f"Claude Code API模块导入失败: {e}")

    def test_claude_code_cli_import(self):
        """测试Claude Code CLI模块导入"""
        try:
            from integrations.claude_code import ClaudeCodeCLI
            cli = ClaudeCodeCLI()
            self.assertIsNotNone(cli)
            print("Claude Code CLI模块导入测试通过。")
        except ImportError:
            self.skipTest("Claude Code CLI模块不可用")
        except Exception as e:
            self.fail(f"Claude Code CLI模块导入失败: {e}")

    def test_claude_code_mcp_import(self):
        """测试Claude Code MCP模块导入"""
        try:
            from integrations.claude_code import ClaudeCodeMCP
            mcp = ClaudeCodeMCP()
            self.assertIsNotNone(mcp)
            print("Claude Code MCP模块导入测试通过。")
        except ImportError:
            self.skipTest("Claude Code MCP模块不可用")
        except Exception as e:
            self.fail(f"Claude Code MCP模块导入失败: {e}")

    def test_claude_code_core_functionality(self):
        """测试Claude Code核心功能"""
        try:
            from integrations.claude_code import ClaudeCodeIntegration
            claude = ClaudeCodeIntegration()
            
            # 测试代码库分析
            analysis = claude.analyze_codebase()
            self.assertIsInstance(analysis, dict)
            print("Claude Code代码库分析功能测试通过。")
            
            # 测试文档生成
            doc = claude.generate_documentation("测试项目", "readme")
            self.assertIsInstance(doc, str)
            self.assertGreater(len(doc), 0)
            print("Claude Code文档生成功能测试通过。")
            
            # 测试计划制定
            plan = claude.plan_implementation("实现用户认证功能")
            self.assertIsInstance(plan, str)
            self.assertGreater(len(plan), 0)
            print("Claude Code计划制定功能测试通过。")
            
        except ImportError:
            self.skipTest("Claude Code集成模块不可用")
        except Exception as e:
            self.fail(f"Claude Code核心功能测试失败: {e}")

if __name__ == '__main__':
    unittest.main()