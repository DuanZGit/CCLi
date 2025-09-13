#!/bin/bash
# CCLi 安装脚本

set -e

echo "正在安装 CCLi - Claude Code CLI..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python3"
    exit 1
fi

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: 未找到 pip3"
    exit 1
fi

# 安装依赖
echo "正在安装依赖包..."
pip3 install -r requirements.txt

# 创建配置目录
echo "正在创建配置目录..."
mkdir -p ~/.ccli

echo "安装完成！"
echo ""
echo "使用方法:"
echo "  python3 main.py         # 运行主程序"
echo "  python3 ui/cli/ccli.py  # 运行CLI界面"
echo ""
echo "CLI命令示例:"
echo "  python3 ui/cli/ccli.py help"
echo "  python3 ui/cli/ccli.py chat -m \"你好，世界！\""
echo "  python3 ui/cli/ccli.py route"