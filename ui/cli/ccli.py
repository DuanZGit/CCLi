#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi CLI - 命令行界面
"""

import argparse
import sys
import os
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

# 动态导入模块
def import_core_module(module_name):
    """动态导入核心模块"""
    try:
        import importlib.util
        module_path = os.path.join(project_root, "core", f"{module_name}.py")
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"导入模块 {module_name} 失败: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="CCLi - Claude Code CLI")
    parser.add_argument("command", nargs="?", default="help", 
                        choices=["help", "chat", "profile", "route", "web", "test"],
                        help="要执行的命令")
    parser.add_argument("--task", "-t", default="default",
                        help="任务类型 (default, background, think, longContext, coding, claudeCode, longContext)")
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

def print_help():
    """打印帮助信息"""
    help_text = """
CCLi - Claude Code CLI 帮助信息

用法:
  ccli <command> [options]

命令:
  help          显示帮助信息
  chat          与AI模型对话
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
  ccli profile
  ccli route
  ccli web
  ccli test
"""
    print(help_text)

def chat_command(args):
    """处理聊天命令"""
    if not args.message:
        print("错误: 请提供要发送的消息")
        return
    
    # 导入模型路由模块
    model_router_module = import_core_module("model_router")
    if not model_router_module:
        print("无法导入模型路由模块")
        return
    
    print(f"正在将请求路由到 {args.task} 任务类型的模型...")
    router = model_router_module.ModelRouter()
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
        # 模拟响应
        print(response.get("response", "无法解析响应"))

def profile_command(args):
    """处理用户画像命令"""
    print("用户画像功能正在开发中...")

def route_command(args):
    """处理路由命令"""
    # 导入模型路由模块
    model_router_module = import_core_module("model_router")
    if not model_router_module:
        print("无法导入模型路由模块")
        return
    
    print("模型路由信息:")
    router = model_router_module.ModelRouter()
    
    print("提供商:")
    for name, provider in router.providers.items():
        print(f"  {name}: {provider.get('api_base_url')}")
    
    print("\n路由规则:")
    for task_type, route in router.routes.items():
        print(f"  {task_type}: {route}")

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

