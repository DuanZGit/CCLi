# CCLi - Claude Code CLI

智能模型路由与中文UI界面的AI系统

## 项目简介

CCLi (Claude Code CLI) 是一个专注于Claude Code集成的AI系统，提供简化的命令行界面，直接进入代码开发模式。

## 核心理念

**简化操作，专注开发**：
- 只需输入 `ccli` 即可直接进入Claude Code模式
- 无需复杂的命令或参数
- 专注于代码分析、文档生成、任务规划等核心功能

## 安装与使用

### 快速安装

```bash
# 克隆项目
git clone https://github.com/DuanZGit/CCLi.git
cd CCLi

# 运行安装脚本
./install.sh
```

### 使用方法

安装完成后，只需输入以下命令即可直接进入Claude Code模式：

```bash
ccli
```

这将直接启动Claude Code集成环境，您可以使用以下命令：

- `analyze` - 分析当前代码库结构
- `plan` - 制定实施计划
- `doc` - 生成项目文档
- `test` - 生成测试代码
- `review` - 执行代码审查
- `help` - 显示帮助信息
- `exit` - 退出程序

### 示例

```bash
# 启动CCLi
ccli

# 进入交互界面后，直接输入命令
ccli> analyze
ccli> plan
ccli> doc
ccli> exit
```

## 核心功能

### Claude Code集成
- **代码库分析**：自动分析项目结构和文件组成
- **文档生成**：自动生成README、API文档等
- **任务规划**：制定详细的实施计划
- **代码生成**：根据描述生成代码实现
- **测试生成**：为现有代码生成单元测试
- **代码审查**：提供代码质量分析和改进建议

## 配置说明

配置文件位于 `~/.ccli/config.json`，主要配置项包括：

- 模型提供商API密钥
- 路由规则

示例配置文件：
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
    "claudeCode": "anthropic,claude-3-opus-20240229"
  }
}
```

## 开发指南

### 运行测试
```bash
# 运行所有测试
python -m pytest tests/
```

## 许可证

本项目采用 MIT License，详情请查看 [LICENSE](LICENSE) 文件。