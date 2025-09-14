# CCLi 部署指南

本指南将帮助您在任何环境中快速部署和运行 CCLi (Claude Code CLI) 项目。

## 系统要求

- Linux/macOS/Windows (WSL)
- Python 3.8 或更高版本
- Git
- 网络连接

## 安装方式

### 方法1: 使用安装脚本（推荐）

```bash
# 克隆项目
git clone https://github.com/DuanZGit/CCLi.git
cd CCLi

# 运行安装脚本
./install.sh
```

安装脚本会自动完成以下操作：
1. 创建Python虚拟环境
2. 安装项目依赖
3. 创建配置文件
4. 设置全局命令

### 方法2: 手动安装

```bash
# 克隆项目
git clone https://github.com/DuanZGit/CCLi.git
cd CCLi

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 创建配置目录
mkdir -p ~/.ccli

# 创建基本配置文件
echo '{"Providers": {"openai": {"name": "openai", "api_base_url": "https://api.openai.com/v1", "api_key": "sk-xxx", "models": ["gpt-3.5-turbo", "gpt-4"]}}, "Router": {"default": "openai,gpt-3.5-turbo"}}' > ~/.ccli/config.json
```

## 使用CLI

安装完成后，您可以通过以下方式使用CLI：

```bash
# 方法1: 使用项目目录中的命令
./ccli --help

# 方法2: 添加到PATH后使用全局命令
ccli --help
```

### CLI命令

```bash
# 查看帮助信息
./ccli --help

# 与AI对话（默认任务类型）
./ccli chat -m "你好，世界！"

# 与AI对话（思考任务类型）
./ccli chat -t think -m "解释量子计算的概念"

# 与AI对话（编程任务类型）
./ccli chat -t coding -m "用Python写一个快速排序算法"

# 与AI对话（Claude Code任务类型）
./ccli chat -t claudeCode -m "分析当前代码库结构"

# 与AI对话（长上下文任务类型）
./ccli chat -t longContext -m "总结这份长文档的主要内容"

# 查看路由配置
./ccli route

# 启动Web UI
./ccli web

# 运行测试
./ccli test
```

## 使用Web UI

### 方法1: 使用CLI命令启动

```bash
# 启动Web UI
./ccli web
```

### 方法2: 使用启动脚本

```bash
# 启动Web UI
./start_web_ui.sh
```

### 方法3: 直接运行

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动Web服务
python ui/web/app.py
```

启动后在浏览器中访问 `http://localhost:8000`

## API密钥配置

要使用真实的AI服务，您需要配置相应的API密钥：

1. **OpenAI**: 在 [OpenAI API Keys](https://platform.openai.com/api-keys) 获取
2. **Anthropic**: 在 [Anthropic Console](https://console.anthropic.com/) 获取
3. **其他提供商**: 根据相应服务商的要求获取API密钥

将获取的API密钥填入配置文件 `~/.ccli/config.json` 中相应的位置。

### 配置文件示例

```json
{
  "Providers": {
    "openai": {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1",
      "api_key": "sk-xxxxxx",
      "models": ["gpt-3.5-turbo", "gpt-4"]
    },
    "anthropic": {
      "name": "anthropic",
      "api_base_url": "https://api.anthropic.com/v1",
      "api_key": "sk-xxxxxx",
      "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"]
    },
    "openrouter": {
      "name": "openrouter",
      "api_base_url": "https://openrouter.ai/api/v1",
      "api_key": "sk-xxxxxx",
      "models": ["openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet"]
    },
    "deepseek": {
      "name": "deepseek",
      "api_base_url": "https://api.deepseek.com/v1",
      "api_key": "sk-xxxxxx",
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
      "api_key": "xxxxxx",
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
```

## 本地模型支持

CCLi 支持本地模型运行，如 Ollama：

### 安装 Ollama

```bash
# Linux
curl -fsSL https://ollama.com/install.sh | sh

# macOS
brew install ollama

# Windows
# 从 https://ollama.com/download/OllamaSetup.exe 下载安装
```

### 运行本地模型

```bash
# 拉取并运行模型
ollama run llama3
ollama run codellama
```

## Docker 部署（可选）

我们还提供了 Docker 配置文件，可以使用 Docker 进行部署：

```bash
# 使用 Docker Compose (推荐)
docker-compose up -d

# 或者单独构建和运行
docker build -t ccli .
docker run -p 8000:8000 ccli
```

## 常见问题

### 1. 依赖安装失败

如果在安装依赖时遇到问题，尝试使用国内镜像源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. Web UI 无法访问

确保防火墙没有阻止 8000 端口，或者修改 `ui/web/app.py` 中的端口配置。

### 3. API 密钥配置

确保配置文件路径正确，并且API密钥具有相应的权限。

### 4. 命令未找到

如果使用 `ccli` 命令时提示"命令未找到"，请确保：
1. 已运行安装脚本
2. `$HOME/.local/bin` 在您的 PATH 环境变量中

添加到 PATH 的方法：
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

## 贡献

欢迎提交 Issue 和 Pull Request 来改进 CCLi 项目！

## 许可证

MIT License