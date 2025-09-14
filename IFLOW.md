# CCLi - Claude Code CLI 项目上下文

## 项目概述

CCLi (Claude Code CLI) 是一个专注于两个核心功能的AI系统：

1. **智能模型路由系统**：支持多模型提供商路由，根据任务类型自动选择最优模型
2. **中文UI界面**：提供命令行和Web两种中文用户界面，方便用户交互

## 项目结构

```
CCLi/
├── core/                    # 核心模块
│   ├── personal_profile.py  # 个人画像系统
│   ├── event_logger.py      # 事件记录系统
│   ├── knowledge_graph.py   # 知识图谱
│   └── model_router.py      # 模型路由系统
├── integrations/            # 集成模块
│   ├── api_providers/       # 第三方API提供商
│   │   ├── base.py          # 基础提供商类
│   │   ├── deepseek.py      # DeepSeek提供商
│   │   ├── gemini.py        # Gemini提供商
│   │   ├── ollama.py        # Ollama提供商
│   │   └── openrouter.py    # OpenRouter提供商
│   └── claude_code/         # Claude Code集成
│       ├── api.py           # Claude Code API接口
│       ├── cli.py           # Claude Code CLI集成
│       ├── core.py          # Claude Code核心功能
│       └── mcp.py           # MCP协议支持
├── ui/                      # 用户界面
│   ├── cli/                 # 命令行界面
│   │   └── ccli.py          # CLI主程序
│   └── web/                 # Web界面
│       ├── app.py           # Web应用主程序
│       ├── main.py          # Web应用入口
│       ├── static/          # 静态资源
│       └── templates/       # HTML模板
├── config/                  # 配置文件
├── tests/                   # 测试文件
├── docs/                    # 文档
├── main.py                  # 主程序
├── requirements.txt         # 依赖包列表
├── start_web_ui.sh          # Web UI启动脚本
├── deploy.sh                # Linux/macOS一键部署脚本
├── deploy.ps1               # Windows一键部署脚本
├── Dockerfile               # Docker配置文件
└── docker-compose.yml       # Docker Compose配置文件
```

## 核心组件说明

### 模型路由系统 (core/model_router.py)
- 支持多提供商模型路由（OpenAI, Anthropic, OpenRouter, DeepSeek, Ollama, Gemini等）
- 根据任务类型自动选择最优模型
- 可配置的路由规则（默认、后台任务、思考、长上下文、编程任务、Claude Code）
- 支持Claude Code集成，提供代码分析、文档生成、任务规划等功能

### 中文UI界面
- **CLI界面**：命令行交互，适合快速操作 (ui/cli/ccli.py)，全中文提示和响应
- **Web UI界面**：图形化界面，功能更丰富，支持实时交互 (ui/web/app.py)，全中文界面
- 支持多种任务类型选择（默认、思考、编程、长上下文、Claude Code等）
- 实时WebSocket通信，提供流畅的聊天体验

## 一键部署

### Linux/macOS 一键部署

```bash
# 下载并运行一键部署脚本
curl -s https://raw.githubusercontent.com/DuanZGit/CCLi/main/deploy.sh | bash
```

### Windows 一键部署

```powershell
# 下载并运行一键部署脚本
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/DuanZGit/CCLi/main/deploy.ps1" -OutFile "deploy.ps1"
.\deploy.ps1
```

### Docker 部署

```bash
# 使用 Docker Compose (推荐)
docker-compose up -d

# 或者单独构建和运行
docker build -t ccli .
docker run -p 8000:8000 ccli
```

## 构建和运行

### 环境要求
- Python 3.8+
- 依赖包：PyYAML, requests, fastapi, uvicorn, websockets, pytest等

### 手动安装步骤
```bash
# 克隆项目
git clone https://github.com/DuanZGit/CCLi.git
cd CCLi

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 运行CLI界面
```bash
# 查看帮助信息
python3 ui/cli/ccli.py --help

# 与AI对话（默认任务类型）
python3 ui/cli/ccli.py chat -m "你好，世界！"

# 与AI对话（思考任务类型）
python3 ui/cli/ccli.py chat -t think -m "解释量子计算的概念"

# 与AI对话（编程任务类型）
python3 ui/cli/ccli.py chat -t coding -m "用Python写一个快速排序算法"

# 与AI对话（Claude Code任务类型）
python3 ui/cli/ccli.py chat -t claudeCode -m "分析当前代码库结构"

# 与AI对话（长上下文任务类型）
python3 ui/cli/ccli.py chat -t longContext -m "总结这份长文档的主要内容"

# 查看路由配置
python3 ui/cli/ccli.py route
```

### 运行Web UI界面
```bash
# 启动Web UI
./start_web_ui.sh

# 或者直接运行
python3 ui/web/app.py

# 然后在浏览器中访问 http://localhost:8000
```

### 运行测试
```bash
# 运行所有测试
python3 -m pytest tests/

# 运行特定测试
python3 -m pytest tests/test_model_router.py -v
```

## 配置说明

配置文件位于 `~/.ccli/config.json`，主要配置项包括：
- 模型提供商API密钥
- 路由规则
- UI设置

示例配置：
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
```

## 开发约定

### 代码风格
- 使用Python 3标准语法
- 遵循PEP 8代码规范
- 重要模块和函数添加文档字符串

### 扩展功能

#### Claude Code集成
CCLi集成了Claude Code的核心功能，包括：
- **代码库分析**：自动分析项目结构和文件组成
- **文档生成**：自动生成README、API文档等
- **任务规划**：制定详细的实施计划
- **代码生成**：根据描述生成代码实现
- **测试生成**：为现有代码生成单元测试
- **代码审查**：提供代码质量分析和改进建议

#### 添加新的API提供商
1. 在 `integrations/api_providers/` 目录下创建新的提供商类
2. 继承 `BaseAPIProvider` 基类
3. 实现必要的方法
4. 在 `integrations/api_providers/__init__.py` 中导出
5. 更新 `core/model_router.py` 中的初始化逻辑