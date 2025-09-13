# CCLi 部署指南

本指南将帮助您在任何环境中快速部署和运行 CCLi (Claude Code CLI) 项目。

## 系统要求

- Linux/macOS/Windows (WSL)
- Python 3.8 或更高版本
- Git
- 网络连接

## 一键部署脚本

我们提供了一键部署脚本，可以自动完成环境配置和项目安装。

### Linux/macOS 一键部署

```bash
# 下载并运行一键部署脚本
curl -s https://raw.githubusercontent.com/your-username/ccli/main/deploy.sh | bash
```

或者手动下载并运行：

```bash
# 克隆项目
git clone https://github.com/your-username/ccli.git
cd ccli

# 运行部署脚本
./deploy.sh
```

### Windows 一键部署

```powershell
# 下载并运行一键部署脚本
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/your-username/ccli/main/deploy.ps1" -OutFile "deploy.ps1"
.\deploy.ps1
```

## 手动部署步骤

如果您希望手动部署，可以按照以下步骤操作：

### 1. 克隆项目

```bash
git clone https://github.com/your-username/ccli.git
cd ccli
```

### 2. 创建虚拟环境

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或者在Windows上: venv\Scripts\activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境

创建配置文件目录：
```bash
mkdir -p ~/.ccli
```

创建基本配置文件 `~/.ccli/config.json`：
```json
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

### 5. 运行测试

```bash
python3 -m pytest tests/
```

## 一键启动方式

### 启动 CLI 界面

```bash
# 激活虚拟环境
source venv/bin/activate

# 运行主程序
python3 main.py

# 或者使用CLI工具
python3 ui/cli/ccli.py --help
```

### 启动 Web UI

```bash
# 激活虚拟环境
source venv/bin/activate

# 启动Web服务
./start_web_ui.sh

# 或者直接运行
python3 ui/web/app.py
```

然后在浏览器中访问 `http://localhost:8000`

## API密钥配置

要使用真实的AI服务，您需要配置相应的API密钥：

1. **OpenAI**: 在 [OpenAI API Keys](https://platform.openai.com/api-keys) 获取
2. **Anthropic**: 在 [Anthropic Console](https://console.anthropic.com/) 获取
3. **其他提供商**: 根据相应服务商的要求获取API密钥

将获取的API密钥填入配置文件 `~/.ccli/config.json` 中相应的位置。

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
# 构建镜像
docker build -t ccli .

# 运行容器
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

## 贡献

欢迎提交 Issue 和 Pull Request 来改进 CCLi 项目！

## 许可证

MIT License