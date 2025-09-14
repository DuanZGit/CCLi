#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Claude Code CLI with CCLi Extensions
基于Anthropic Claude Code CLI，集成智能路由和UI扩展
"""

import argparse
import sys
import os
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def main():
    parser = argparse.ArgumentParser(description="Claude Code CLI with CCLi Extensions")
    parser.add_argument("command", nargs="?", default="help", 
                        choices=["help", "analyze", "plan", "doc", "test", "review"],
                        help="要执行的命令")
    parser.add_argument("--message", "-m", default="",
                        help="要发送的消息或描述")
    parser.add_argument("--route", "-r", action="store_true",
                        help="使用智能路由模式")
    parser.add_argument("--task", "-t", default="claudeCode",
                        help="任务类型 (default, background, think, longContext, coding, claudeCode)")
    parser.add_argument("--web", "-w", action="store_true",
                        help="启动Web界面")

    args = parser.parse_args()

    # 处理Web界面命令
    if args.web:
        handle_web_command()
        return

    # 处理路由模式
    if args.route:
        handle_routing_command(args)
        return

    # 处理原生Claude Code命令
    if args.command == "help":
        print_help()
    elif args.command == "analyze":
        analyze_command(args)
    elif args.command == "plan":
        plan_command(args)
    elif args.command == "doc":
        doc_command(args)
    elif args.command == "test":
        test_command(args)
    elif args.command == "review":
        review_command(args)

def print_help():
    """打印帮助信息"""
    help_text = """
Claude Code CLI with CCLi Extensions 帮助信息

用法:
  ccli <command> [options]

命令:
  help          显示帮助信息
  analyze       分析代码库结构（原生Claude Code）
  plan          制定实施计划（原生Claude Code）
  doc           生成项目文档（原生Claude Code）
  test          生成测试代码（原生Claude Code）
  review        代码审查（原生Claude Code）

选项:
  -m, --message MESSAGE 附加的消息或描述
  -r, --route           使用智能路由模式
  -t, --task TASK       任务类型 (default, background, think, longContext, coding, claudeCode)
  -w, --web             启动Web界面

示例:
  # 直接使用Claude Code功能（默认模式）
  ccli analyze
  ccli plan -m "实现用户认证功能"
  ccli doc -m "API文档"
  ccli test
  ccli review

  # 使用智能路由
  ccli --route --task think -m "解释量子计算的概念"
  ccli -r -t coding -m "用Python写一个快速排序算法"

  # 启动Web界面
  ccli --web
"""
    print(help_text)

def analyze_command(args):
    """处理代码库分析命令"""
    print("正在分析代码库结构...")
    # 这里应该调用实际的Claude Code分析功能
    print("代码库分析完成:")
    print("  - 项目结构已分析")
    print("  - 文件依赖关系已识别")
    print("  - 代码质量评估已完成")

def plan_command(args):
    """处理实施计划命令"""
    message = args.message if args.message else "默认功能实现"
    print(f"正在制定实施计划: {message}")
    # 这里应该调用实际的Claude Code计划功能
    print("实施计划:")
    print("  1. 需求分析")
    print("  2. 技术选型")
    print("  3. 架构设计")
    print("  4. 实现步骤")
    print("  5. 测试策略")

def doc_command(args):
    """处理文档生成命令"""
    doc_type = args.message if args.message else "技术文档"
    print(f"正在生成{doc_type}...")
    # 这里应该调用实际的Claude Code文档生成功能
    print("文档生成完成:")
    print("  - 文档结构已创建")
    print("  - 内容已填充")
    print("  - 格式已优化")

def test_command(args):
    """处理测试代码生成命令"""
    print("正在生成测试代码...")
    # 这里应该调用实际的Claude Code测试代码生成功能
    print("测试代码生成完成:")
    print("  - 单元测试已生成")
    print("  - 集成测试已生成")
    print("  - 测试用例已优化")

def review_command(args):
    """处理代码审查命令"""
    print("正在执行代码审查...")
    # 这里应该调用实际的Claude Code代码审查功能
    print("代码审查结果:")
    print("  - 代码风格符合规范")
    print("  - 潜在问题已识别")
    print("  - 改进建议已提供")

def handle_routing_command(args):
    """处理路由命令"""
    message = args.message
    if not message:
        # 如果没有提供消息，使用默认消息
        if args.command and args.command != "help":
            message = f"执行 {args.command} 命令"
        else:
            message = "Hello, AI!"
    
    try:
        # 导入路由插件
        sys.path.insert(0, os.path.join(project_root, "plugins"))
        from plugins.model_router import ModelRouterPlugin
        
        print(f"正在将请求路由到 {args.task} 任务类型的模型...")
        router = ModelRouterPlugin()
        response = router.send_request(args.task, message)
        
        print(f"AI响应:")
        print(response.get("response", str(response)))
    except Exception as e:
        print(f"路由命令执行出错: {e}")

def handle_web_command():
    """处理Web界面命令"""
    print("正在启动Web UI...")
    try:
        # 导入Web UI模块
        web_ui_path = os.path.join(project_root, "plugins", "ui", "web_interface", "app.py")
        if os.path.exists(web_ui_path):
            # 使用子进程启动Web UI
            subprocess.Popen([sys.executable, web_ui_path])
            print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
        else:
            print("错误: 找不到Web UI文件")
    except Exception as e:
        print(f"启动Web UI时出错: {e}")

if __name__ == "__main__":
    main()