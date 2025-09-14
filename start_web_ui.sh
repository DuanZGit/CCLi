#!/bin/bash
# CCLi Web UI 启动脚本（简化版）

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 切换到项目根目录
cd "$SCRIPT_DIR/../.."

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
echo "启动CCLi Web UI (简化版)..."
echo "访问地址: http://localhost:8000"
echo "按 Ctrl+C 停止服务"

# 使用后台进程启动Web UI
python3 ui/web/app.py &

# 保存进程ID
WEB_UI_PID=$!

# 等待进程结束
wait $WEB_UI_PID