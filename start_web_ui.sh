#!/bin/bash
# CCLi Web UI 启动脚本

# 检查是否在项目根目录
if [ ! -f "main.py" ]; then
    echo "请在CCLi项目根目录运行此脚本"
    exit 1
fi

# 激活虚拟环境
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "虚拟环境已激活"
else
    echo "未找到虚拟环境，使用系统Python"
fi

# 启动Web UI
echo "启动CCLi Web UI..."
echo "访问地址: http://localhost:8000"
python3 ui/web/app.py