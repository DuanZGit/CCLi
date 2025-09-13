# CCLi Docker 配置文件

# 使用 Python 3.11 作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user
ENV APP_HOME=/home/user/app
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
COPY --chown=user . $APP_HOME

# 创建虚拟环境并安装Python依赖
RUN python -m venv venv \
    && venv/bin/pip install --upgrade pip \
    && venv/bin/pip install -r requirements.txt

# 创建配置目录
RUN mkdir -p $HOME/.ccli

# 创建默认配置文件
RUN echo '{
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
      "api_base_url": "http://host.docker.internal:11434/api",
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
}' > $HOME/.ccli/config.json

# 暴露端口
EXPOSE 8000

# 运行测试
RUN venv/bin/python -m pytest tests/ -v

# 启动Web UI
CMD ["venv/bin/python", "ui/web/app.py"]