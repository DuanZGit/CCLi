"""
CLI扩展插件
为Claude Code CLI添加扩展命令和选项
"""

import argparse
import sys
import os
import subprocess

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(project_root, "plugins"))

from plugins.model_router import ModelRouterPlugin

class CLIExtensionPlugin:
    """CLI扩展插件"""
    
    def __init__(self):
        """初始化CLI扩展插件"""
        self.router = ModelRouterPlugin()
    
    def add_routing_options(self, parser):
        """添加路由相关选项到CLI解析器"""
        parser.add_argument("--route", "-r", action="store_true",
                          help="使用智能路由模式")
        parser.add_argument("--task", "-t", default="default",
                          help="任务类型 (default, background, think, longContext, coding, claudeCode)")
        parser.add_argument("--web", "-w", action="store_true",
                          help="启动Web界面")
    
    def handle_routing_command(self, args, original_message):
        """处理路由命令"""
        if not hasattr(args, 'route') or not args.route:
            return False
            
        if not original_message:
            print("错误: 请提供要发送的消息")
            return True
        
        try:
            print(f"正在将请求路由到 {args.task} 任务类型的模型...")
            response = self.router.send_request(args.task, original_message)
            
            print(f"AI响应:")
            print(response.get("response", str(response)))
            return True
        except Exception as e:
            print(f"路由命令执行出错: {e}")
            return True
    
    def handle_web_command(self, args):
        """处理Web界面命令"""
        if not hasattr(args, 'web') or not args.web:
            return False
            
        print("正在启动Web UI...")
        try:
            # 这里应该启动Web界面
            web_ui_path = os.path.join(project_root, "plugins", "ui", "web_interface", "app.py")
            if os.path.exists(web_ui_path):
                subprocess.Popen([sys.executable, web_ui_path])
                print("Web UI已启动，请在浏览器中访问 http://localhost:8000")
            else:
                print("错误: 找不到Web UI文件")
        except Exception as e:
            print(f"启动Web UI时出错: {e}")
        return True

# 插件注册函数
def register_plugin(cli_app):
    """注册插件到CLI应用"""
    extension = CLIExtensionPlugin()
    print("CLI扩展插件已注册")
    return extension