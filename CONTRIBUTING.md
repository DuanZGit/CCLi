# 贡献指南

感谢您对 CCLi 项目的兴趣！我们欢迎各种形式的贡献。

## 如何贡献

### 报告 Bug

如果您发现了 Bug，请在 GitHub Issues 中报告，并包含以下信息：
- 清晰的标题和描述
- 复现步骤
- 预期行为和实际行为
- 环境信息（操作系统、Python 版本等）
- 相关的日志或错误信息

### 提交功能请求

如果您有新的功能想法，请在 GitHub Issues 中提交，并描述：
- 功能的详细描述
- 解决的问题或满足的需求
- 可能的实现方案

### 提交代码

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

### 编码规范

- 遵循 PEP 8 编码规范
- 编写清晰的注释和文档
- 添加相应的测试用例
- 确保所有测试通过

### 测试

在提交代码前，请确保：
- 所有现有测试通过
- 新增功能有相应的测试用例
- 运行 `python -m pytest tests/` 检查测试结果

## 开发环境设置

1. Fork 并克隆项目
2. 创建虚拟环境
3. 安装依赖 `pip install -r requirements.txt`
4. 运行测试确保环境正常

## 代码结构

- `core/` - 核心模块
- `agents/` - 智能代理模块
- `integrations/` - 第三方集成模块
- `ui/` - 用户界面模块
- `tests/` - 测试文件
- `docs/` - 文档

## 问题和讨论

如果您有任何问题或建议，欢迎在 GitHub Issues 中讨论。

再次感谢您的贡献！