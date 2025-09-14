#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi - Claude Code CLI 简化版
直接进入Claude Code模式
"""

import sys
import os
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def main():
    """主函数 - 直接进入Claude Code模式"""
    print("CCLi - Claude Code CLI")
    print("直接进入Claude Code模式...")
    print("")
    
    # 导入Claude Code集成模块
    try:
        from integrations.claude_code import ClaudeCodeIntegration
        claude_code = ClaudeCodeIntegration()
        print("Claude Code集成已初始化")
        print("")
        
        # 显示欢迎信息和基本操作
        print("欢迎使用Claude Code CLI!")
        print("支持的操作:")
        print("  analyze    - 分析当前代码库")
        print("  plan       - 制定实施计划")
        print("  doc        - 生成文档")
        print("  test       - 生成测试代码")
        print("  review     - 代码审查")
        print("  web        - 启动Web UI界面")
        print("  help       - 显示帮助信息")
        print("  exit       - 退出程序")
        print("")
        
        # 进入交互模式
        while True:
            try:
                command = input("ccli> ").strip().lower()
                
                if command == "exit":
                    print("再见!")
                    break
                elif command == "help":
                    print("支持的操作:")
                    print("  analyze    - 分析当前代码库")
                    print("  plan       - 制定实施计划")
                    print("  doc        - 生成文档")
                    print("  test       - 生成测试代码")
                    print("  review     - 代码审查")
                    print("  web        - 启动Web UI界面")
                    print("  help       - 显示帮助信息")
                    print("  exit       - 退出程序")
                elif command == "analyze":
                    print("正在分析代码库...")
                    try:
                        analysis = claude_code.analyze_codebase()
                        print(f"代码库分析完成:")
                        print(f"  文件数: {len(analysis.get('files', []))}")
                        print(f"  目录数: {len(analysis.get('directories', []))}")
                        print(f"  总大小: {analysis.get('size', 0)} bytes")
                    except Exception as e:
                        print(f"分析过程中出错: {e}")
                elif command == "plan":
                    print("正在制定实施计划...")
                    try:
                        plan = claude_code.plan_implementation("用户请求的功能实现")
                        print(f"实施计划:")
                        print(plan)
                    except Exception as e:
                        print(f"制定计划时出错: {e}")
                elif command == "doc":
                    print("正在生成文档...")
                    try:
                        doc = claude_code.generate_documentation("项目功能说明", "readme")
                        print(f"文档生成完成:")
                        print(doc)
                    except Exception as e:
                        print(f"生成文档时出错: {e}")
                elif command == "test":
                    print("正在生成测试代码...")
                    try:
                        # 这里应该生成测试代码的示例
                        print("测试代码生成功能已调用。在完整实现中，将生成针对项目代码的单元测试。")
                    except Exception as e:
                        print(f"生成测试代码时出错: {e}")
                elif command == "review":
                    print("正在执行代码审查...")
                    try:
                        review = claude_code.review_code()
                        print(f"代码审查结果:")
                        print(review)
                    except Exception as e:
                        print(f"代码审查时出错: {e}")
                elif command == "web":
                    print("正在启动Web UI...")
                    try:
                        # 启动Web UI
                        web_ui_script = os.path.join(project_root, "start_web_ui.sh")
                        if os.path.exists(web_ui_script):
                            subprocess.Popen(["bash", web_ui_script])
                            print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
                        else:
                            # 直接运行Web应用
                            web_app = os.path.join(project_root, "ui", "web", "app.py")
                            if os.path.exists(web_app):
                                subprocess.Popen([sys.executable, web_app])
                                print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
                            else:
                                print("错误: 找不到Web UI文件")
                    except Exception as e:
                        print(f"启动Web UI时出错: {e}")
                elif command == "":
                    # 空命令，继续循环
                    continue
                else:
                    print(f"未知命令: {command}")
                    print("输入 'help' 查看支持的命令")
                    
            except KeyboardInterrupt:
                print("
再见!")
                break
            except EOFError:
                print("
再见!")
                break
                
    except ImportError as e:
        print(f"无法导入Claude Code集成模块: {e}")
        print("请检查项目安装是否正确")
        return 1
    except Exception as e:
        print(f"初始化Claude Code集成时出错: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())