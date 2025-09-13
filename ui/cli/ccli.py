#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCLi CLI - 命令行界面
"""

import argparse
import sys
import os

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
                        choices=["help", "chat", "profile", "route"],
                        help="要执行的命令")
    parser.add_argument("--task", "-t", default="default",
                        help="任务类型 (default, background, think, longContext)")
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

选项:
  -t, --task TASK       任务类型 (default, background, think, longContext)
  -m, --message MESSAGE 要发送的消息
  -u, --user-id USER_ID 用户ID

示例:
  ccli chat -m "你好，世界！"
  ccli chat -t think -m "解释量子计算的概念"
  ccli profile
  ccli route
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

if __name__ == "__main__":
    main()
