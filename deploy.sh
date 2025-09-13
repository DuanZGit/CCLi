#!/bin/bash

# CCLi 一键部署脚本 (Linux/macOS)
# 作者: CCLi Team
# 日期: 2025年9月13日

set -e  # 遇到错误时退出

echo "========================================"
echo "        CCLi 一键部署脚本"
echo "========================================"
echo ""

# 检查系统类型
UNAME=$(uname)
if [[ "$UNAME" == "Linux" ]]; then
    echo "检测到 Linux 系统"
    SYSTEM="Linux"
elif [[ "$UNAME" == "Darwin" ]]; then
    echo "检测到 macOS 系统"
    SYSTEM="macOS"
else
    echo "不支持的操作系统: $UNAME"
    exit 1
fi

# 检查必要工具
echo "检查必要工具..."
if ! command -v git &> /dev/null; then
    echo "错误: 未安装 git"
    if [[ "$SYSTEM" == "Linux" ]]; then
        echo "请运行以下命令安装 git:"
        echo "sudo apt update && sudo apt install git -y"
    else
        echo "请运行以下命令安装 git:"
        echo "brew install git"
    fi
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    echo "错误: 未安装 Python 3"
    if [[ "$SYSTEM" == "Linux" ]]; then
        echo "请运行以下命令安装 Python 3:"
        echo "sudo apt update && sudo apt install python3 python3-venv python3-pip -y"
    else
        echo "请从 https://www.python.org/downloads/ 下载安装 Python 3"
    fi
    exit 1
fi

echo "所有必要工具已安装"

# 创建安装目录
INSTALL_DIR="$HOME/ccli"
echo "创建安装目录: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# 克隆项目
echo "克隆 CCLi 项目..."
if [ -d ".git" ]; then
    echo "项目已存在，正在更新..."
    git pull
else
    git clone https://github.com/your-username/ccli.git .
fi

# 创建虚拟环境
echo "创建 Python 虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 升级 pip
echo "升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
if [[ "$SYSTEM" == "Linux" ]]; then
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
else
    pip install -r requirements.txt
fi

# 创建配置目录
echo "创建配置目录..."
mkdir -p "$HOME/.ccli"

# 创建默认配置文件
echo "创建默认配置文件..."
cat > "$HOME/.ccli/config.json" << EOF
{
  "Providers": {
    "openai": {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1",
      "api_key": "sk-xxx",
      "models": ["gpt-3.5-turbo", "gpt-4"]
    },
    "anthropic": {
      "name": "anthropic",
      "api_base_url": "https://api.anthropic.com/v1",
      "api_key": "sk-xxx",
      "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"]
    },
    "openrouter": {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1",
      "api_key": "sk-xxx",
      "models": ["openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet"]
    },
    "deepseek": {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/v1",
      "api_key": "sk-xxx",
      "models": ["deepseek-chat", "deepseek-coder"]
    },
    "ollama": {
      "name": "ollama",
      "api_base_url": "http://localhost:11434/api",
      "api_key": "",
      "models": ["llama3", "codellama"]
    },
    "gemini": {
      "name": "gemini",
      "api_base_url": "https://generativelanguage.googleapis.com/v1beta",
      "api_key": "sk-xxx",
      "models": ["gemini-pro", "gemini-1.5-pro"]
    }
  },
  "Router": {
    "default": "openai,gpt-3.5-turbo",
    "background": "ollama,llama3",
    "think": "anthropic,claude-3-sonnet-20240229",
    "longContext": "gemini,gemini-1.5-pro",
    "coding": "deepseek,deepseek-coder",
    "claudeCode": "anthropic,claude-3-opus-20240229"
  }
}
EOF

# 运行测试
echo "运行测试..."
python3 -m pytest tests/ -v

# 创建启动脚本
echo "创建启动脚本..."
cat > "$INSTALL_DIR/start.sh" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source venv/bin/activate
python3 main.py
EOF

chmod +x "$INSTALL_DIR/start.sh"

cat > "$INSTALL_DIR/start-web.sh" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source venv/bin/activate
python3 ui/web/app.py
EOF

chmod +x "$INSTALL_DIR/start-web.sh"

# 完成信息
echo ""
echo "========================================"
echo "        CCLi 部署完成!"
echo "========================================"
echo ""
echo "项目已安装到: $INSTALL_DIR"
echo "配置文件位置: $HOME/.ccli/config.json"
echo ""
echo "启动 CLI:"
echo "  $INSTALL_DIR/start.sh"
echo ""
echo "启动 Web UI:"
echo "  $INSTALL_DIR/start-web.sh"
echo "  然后在浏览器中访问 http://localhost:8000"
echo ""
echo "请编辑 $HOME/.ccli/config.json 文件添加您的 API 密钥"
echo ""
echo "查看帮助信息:"
echo "  $INSTALL_DIR/venv/bin/python3 ui/cli/ccli.py --help"
echo ""