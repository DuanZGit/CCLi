# Claude Code CLI with CCLi Extensions

基于Anthropic Claude Code CLI，集成智能路由和UI扩展功能

## 项目简介

这是一个基于Anthropic Claude Code CLI的增强版本，集成了两个核心插件：

1. **智能模型路由插件** - 整合自 musistudio/claude-code-router 和 xixu-me/Claude-Code-Toolkit
2. **UI界面插件** - 整合自 siteboon/claudecodeui

保持Claude Code CLI的原生功能和使用方式，同时添加了智能路由和Web界面扩展。

## 核心功能

### Claude Code原生功能（保持不变）
- `analyze` - 分析代码库结构
- `plan` - 制定实施计划
- `doc` - 生成项目文档
- `test` - 生成测试代码
- `review` - 代码审查

### CCLi扩展功能
- **智能路由模式** - 根据任务类型自动选择最优AI模型
- **Web界面** - 提供图形化操作界面
- **统一配置管理** - 集中式配置文件管理所有AI提供商

## 安装与使用

### 快速开始

```bash
# 克隆项目
git clone <repository-url>
cd claude-code-ccli

# 创建虚拟环境并安装依赖
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 创建配置文件
mkdir -p ~/.ccli
cp config/config.example.json ~/.ccli/config.json
# 编辑 ~/.ccli/config.json 添加您的API密钥
```

### 使用方式

#### 1. 原生Claude Code CLI方式（保持原样）

```bash
# 直接使用Claude Code功能
./ccli analyze
./ccli plan -m "实现用户认证功能"
./ccli doc -m "API文档"
./ccli test
./ccli review
```

#### 2. 智能路由模式

```bash
# 使用智能路由
./ccli --route --task think -m "解释量子计算的概念"
./ccli -r -t coding -m "用Python写一个快速排序算法"

# 或者使用默认Claude Code路由
./ccli -r -m "分析当前代码库"
```

#### 3. Web界面

```bash
# 启动Web界面
./ccli --web

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
    }
  },
  "Router": {
    "default": "anthropic,claude-3-sonnet-20240229",
    "claudeCode": "anthropic,claude-3-opus-20240229"
  }
}
```

## 项目结构

```
claude-code-ccli/
├── claude_code_cli/          # Claude Code CLI核心
│   ├── ccli.py              # 主CLI程序
│   ├── main.py              # 入口文件
│   └── plugins/             # CCLi扩展插件
│       ├── model_router.py  # 智能路由插件
│       └── ui_extension.py  # UI扩展插件
├── plugins/                 # 插件系统
│   ├── router/              # 路由插件
│   │   ├── routing_engine/  # 路由引擎
│   │   └── providers/       # AI提供商支持
│   └── ui/                  # UI插件
│       ├── web_interface/   # Web界面
│       └── cli_extension/   # CLI扩展
├── config/                  # 配置文件
├── ccli                     # 全局命令脚本
└── README.md               # 项目说明
```

## 插件开发

### 路由插件扩展
1. 在 `plugins/router/providers/` 目录下添加新的AI提供商支持
2. 实现BaseProvider接口
3. 在配置文件中注册新的提供商

### UI插件扩展
1. 在 `plugins/ui/` 目录下扩展界面功能
2. 保持与Claude Code CLI核心的一致性

## 许可证

本项目采用 MIT License。