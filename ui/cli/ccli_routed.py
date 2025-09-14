#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi - Claude Code CLI with Model Routing
智能模型路由的Claude Code命令行界面
"""

import argparse
import sys
import os
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def main():
    parser = argparse.ArgumentParser(description="CCLi - Claude Code CLI with Model Routing")
    parser.add_argument("command", nargs="?", default="help", 
                        choices=["help", "chat", "profile", "route", "web", "test", "claude"],
                        help="要执行的命令")
    parser.add_argument("--task", "-t", default="claudeCode",
                        help="任务类型 (default, background, think, longContext, coding, claudeCode)")
    parser.add_argument("--message", "-m", default="",
                        help="要发送的消息")
    parser.add_argument("--user-id", "-u", default="001",
                        help="用户ID")

    args = parser.parse_args()

    if args.command == "help":
        print_help()
    elif args.command == "chat":
        chat_command(args)
    elif args.command == "profile":
        profile_command(args)
    elif args.command == "route":
        route_command(args)
    elif args.command == "web":
        web_command(args)
    elif args.command == "test":
        test_command(args)
    elif args.command == "claude":
        claude_command(args)

def print_help():
    """打印帮助信息"""
    help_text = """
CCLi - Claude Code CLI with Model Routing 帮助信息

用法:
  ccli <command> [options]

命令:
  help          显示帮助信息
  chat          与AI模型对话（通过智能路由）
  claude        直接使用Claude Code功能
  profile       查看或更新用户画像
  route         查看模型路由信息
  web           启动Web UI界面
  test          运行项目测试

选项:
  -t, --task TASK       任务类型 (default, background, think, longContext, coding, claudeCode)
  -m, --message MESSAGE 要发送的消息
  -u, --user-id USER_ID 用户ID

示例:
  ccli chat -m "你好，世界！"
  ccli chat -t think -m "解释量子计算的概念"
  ccli claude -m "分析当前代码库结构"
  ccli profile
  ccli route
  ccli web
  ccli test
"""
    print(help_text)

def chat_command(args):
    """处理聊天命令（通过模型路由）"""
    if not args.message:
        print("错误: 请提供要发送的消息")
        return
    
    try:
        # 导入模型路由模块
        from core.model_router import ModelRouter
        print(f"正在将请求路由到 {args.task} 任务类型的模型...")
        router = ModelRouter()
        response = router.send_request(args.task, args.message)
        
        print(f"AI响应:")
        if "content" in response:
            # Anthropic格式
            for content_item in response["content"]:
                if content_item["type"] == "text":
                    print(content_item["text"])
        elif "choices" in response:
            # OpenAI格式
            for choice in response["choices"]:
                if "message" in choice:
                    print(choice["message"]["content"])
        else:
            # 模拟响应或其他格式
            print(response.get("response", str(response)))
    except Exception as e:
        print(f"聊天命令执行出错: {e}")

def claude_command(args):
    """处理Claude Code命令（直接调用）"""
    try:
        # 导入Claude Code集成模块
        from integrations.claude_code import ClaudeCodeIntegration
        claude = ClaudeCodeIntegration()
        
        if not args.message:
            print("Claude Code功能:")
            print("  直接调用Claude Code进行代码分析、文档生成等操作")
            print("  示例: ccli claude -m '分析当前代码库结构'")
            return
        
        print("正在调用Claude Code...")
        response = claude.send_prompt(args.message, args.task)
        print(f"Claude Code响应:")
        print(response)
    except ImportError:
        print("Claude Code集成不可用")
    except Exception as e:
        print(f"Claude Code命令执行出错: {e}")

def profile_command(args):
    """处理用户画像命令"""
    print("用户画像功能正在开发中...")

def route_command(args):
    """处理路由命令"""
    try:
        from core.model_router import ModelRouter
        print("模型路由信息:")
        router = ModelRouter()
        
        print("提供商:")
        for name, provider in router.providers.items():
            print(f"  {name}: {provider.get('api_base_url')}")
        
        print("\n路由规则:")
        for task_type, route in router.routes.items():
            print(f"  {task_type}: {route}")
    except Exception as e:
        print(f"路由命令执行出错: {e}")

def web_command(args):
    """处理Web UI命令"""
    print("正在启动Web UI...")
    try:
        # 导入Web UI模块
        web_ui_path = os.path.join(project_root, "ui", "web", "app.py")
        if os.path.exists(web_ui_path):
            # 使用子进程启动Web UI
            subprocess.Popen([sys.executable, web_ui_path])
            print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
        else:
            print("错误: 找不到Web UI文件")
    except Exception as e:
        print(f"启动Web UI时出错: {e}")

def test_command(args):
    """处理测试命令"""
    print("正在运行项目测试...")
    try:
        # 运行测试
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              cwd=project_root, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        print(f"测试完成，退出码: {result.returncode}")
    except Exception as e:
        print(f"运行测试时出错: {e}")

if __name__ == "__main__":
    main()
