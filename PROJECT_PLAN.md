# Claude Code CLI with CCLi Extensions

基于Anthropic Claude Code CLI，集成智能路由和UI扩展功能

## 项目结构

```
claude-code-ccli/
├── claude_code/              # 原始Claude Code CLI核心
│   ├── core/                 # Claude Code核心功能
│   ├── cli/                  # 命令行接口
│   └── utils/                # 工具函数
├── plugins/                  # CCLi扩展插件
│   ├── router/               # 智能模型路由插件
│   │   ├── providers/        # 各种AI提供商支持
│   │   └── routing_engine/   # 路由引擎
│   └── ui/                   # UI界面插件
│       ├── cli_extension/    # CLI扩展
│       └── web_interface/    # Web界面
├── config/                   # 配置文件
├── docs/                     # 文档
├── tests/                    # 测试
└── main.py                  # 主入口
```

## 核心功能

### 1. Claude Code CLI核心功能（保持原样）
- 代码分析和理解
- 文档生成
- 任务规划
- 代码生成
- 测试生成
- 代码审查

### 2. CCLi插件扩展

#### 智能路由插件
基于以下项目整合：
- **musistudio/claude-code-router**: 智能模型路由系统
- **xixu-me/Claude-Code-Toolkit**: 任务类型优化和路由策略

功能特性：
- 多模型提供商支持（OpenAI, Anthropic, OpenRouter, DeepSeek, Ollama, Gemini等）
- 基于任务类型的智能路由（默认、后台任务、思考、长上下文、编程任务、Claude Code）
- 可配置的路由规则
- 模型性能监控和自动切换

#### UI界面插件
基于以下项目整合：
- **siteboon/claudecodeui**: 图形化用户界面

功能特性：
- 命令行界面扩展（保持Claude Code CLI原生体验）
- Web界面（实时交互、可视化操作）
- 统一的用户交互体验
- 实时WebSocket通信

## 使用方式

### 命令行使用（保持Claude Code CLI原生方式）
```bash
# 直接使用Claude Code功能（默认模式）
ccli analyze
ccli plan
ccli doc
ccli test
ccli review

# 使用智能路由
ccli --route think "解释量子计算的概念"
ccli --route coding "用Python写一个快速排序算法"
```

### Web界面使用
```bash
# 启动Web UI
ccli --web

# 然后在浏览器中访问 http://localhost:8000
```

## 配置说明

配置文件位于 `~/.ccli/config.json`：

```json
{
  "Providers": {
    "anthropic": {
      "name": "anthropic",
      "api_base_url": "https://api.anthropic.com/v1",
      "api_key": "sk-xxx",
      "models": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]
    },
    "openai": {
      "name": "openai",
      "api_base_url": "https://api.openai.com/v1",
      "api_key": "sk-xxx",
      "models": ["gpt-3.5-turbo", "gpt-4"]
    }
  },
  "Router": {
    "default": "anthropic,claude-3-sonnet-20240229",
    "background": "ollama,llama3",
    "think": "anthropic,claude-3-opus-20240229",
    "longContext": "gemini,gemini-1.5-pro",
    "coding": "deepseek,deepseek-coder",
    "claudeCode": "anthropic,claude-3-opus-20240229"
  }
}
```

## 开发指南

### 插件开发

#### 路由插件开发
1. 在 `plugins/router/providers/` 目录下添加新的提供商支持
2. 实现提供商接口
3. 在路由配置中注册新的提供商

#### UI插件开发
1. 在 `plugins/ui/` 目录下扩展界面功能
2. 保持与Claude Code CLI核心的一致性
3. 提供统一的用户交互体验

## 许可证

本项目采用 MIT License，详情请查看 [LICENSE](LICENSE) 文件。