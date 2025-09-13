# CCLi 一键部署脚本 (Windows)
# 作者: CCLi Team
# 日期: 2025年9月13日

# 检查 PowerShell 版本
$PSVersion = $PSVersionTable.PSVersion.Major
if ($PSVersion -lt 5) {
    Write-Host "错误: 需要 PowerShell 5.0 或更高版本"
    Write-Host "请从 https://docs.microsoft.com/en-us/powershell/scripting/windows-powershell/install/installing-windows-powershell 升级 PowerShell"
    exit 1
}

Write-Host "========================================"
Write-Host "        CCLi 一键部署脚本 (Windows)"
Write-Host "========================================"
Write-Host ""

# 检查必要工具
Write-Host "检查必要工具..."

# 检查 Git
$gitPath = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitPath) {
    Write-Host "错误: 未安装 Git"
    Write-Host "请从 https://git-scm.com/download/win 下载并安装 Git"
    exit 1
}

# 检查 Python
$pythonPath = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonPath) {
    Write-Host "错误: 未安装 Python"
    Write-Host "请从 https://www.python.org/downloads/ 下载并安装 Python 3.8 或更高版本"
    exit 1
}

Write-Host "所有必要工具已安装"

# 创建安装目录
$INSTALL_DIR = "$env:USERPROFILE\ccli"
Write-Host "创建安装目录: $INSTALL_DIR"
New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
Set-Location $INSTALL_DIR

# 克隆项目
Write-Host "克隆 CCLi 项目..."
if (Test-Path ".git") {
    Write-Host "项目已存在，正在更新..."
    git pull
} else {
    git clone https://github.com/your-username/ccli.git .
}

# 创建虚拟环境
Write-Host "创建 Python 虚拟环境..."
python -m venv venv
.\venv\Scripts\Activate.ps1

# 升级 pip
Write-Host "升级 pip..."
python -m pip install --upgrade pip

# 安装依赖
Write-Host "安装项目依赖..."
pip install -r requirements.txt

# 创建配置目录
Write-Host "创建配置目录..."
$CONFIG_DIR = "$env:USERPROFILE\.ccli"
New-Item -ItemType Directory -Path $CONFIG_DIR -Force | Out-Null

# 创建默认配置文件
Write-Host "创建默认配置文件..."
$CONFIG_CONTENT = @{
    "Providers" = @{
        "openai" = @{
            "name" = "openai"
            "api_base_url" = "https://api.openai.com/v1"
            "api_key" = "sk-xxx"
            "models" = @("gpt-3.5-turbo", "gpt-4")
        }
        "anthropic" = @{
            "name" = "anthropic"
            "api_base_url" = "https://api.anthropic.com/v1"
            "api_key" = "sk-xxx"
            "models" = @("claude-3-haiku-20240307", "claude-3-sonnet-20240229")
        }
        "openrouter" = @{
            "name" = "openrouter"
            "api_base_url" = "https://openrouter.ai/api/v1"
            "api_key" = "sk-xxx"
            "models" = @("openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet")
        }
        "deepseek" = @{
            "name" = "deepseek"
            "api_base_url" = "https://api.deepseek.com/v1"
            "api_key" = "sk-xxx"
            "models" = @("deepseek-chat", "deepseek-coder")
        }
        "ollama" = @{
            "name" = "ollama"
            "api_base_url" = "http://localhost:11434/api"
            "api_key" = ""
            "models" = @("llama3", "codellama")
        }
        "gemini" = @{
            "name" = "gemini"
            "api_base_url" = "https://generativelanguage.googleapis.com/v1beta"
            "api_key" = "sk-xxx"
            "models" = @("gemini-pro", "gemini-1.5-pro")
        }
    }
    "Router" = @{
        "default" = "openai,gpt-3.5-turbo"
        "background" = "ollama,llama3"
        "think" = "anthropic,claude-3-sonnet-20240229"
        "longContext" = "gemini,gemini-1.5-pro"
        "coding" = "deepseek,deepseek-coder"
        "claudeCode" = "anthropic,claude-3-opus-20240229"
    }
}

$CONFIG_CONTENT | ConvertTo-Json -Depth 10 | Out-File -FilePath "$CONFIG_DIR\config.json" -Encoding UTF8

# 运行测试
Write-Host "运行测试..."
python -m pytest tests/ -v

# 创建启动脚本
Write-Host "创建启动脚本..."
@"
cd $INSTALL_DIR
.\venv\Scripts\Activate.ps1
python main.py
"@ | Out-File -FilePath "$INSTALL_DIR\start.bat" -Encoding ASCII

@"
cd $INSTALL_DIR
.\venv\Scripts\Activate.ps1
python ui/web/app.py
"@ | Out-File -FilePath "$INSTALL_DIR\start-web.bat" -Encoding ASCII

# 完成信息
Write-Host ""
Write-Host "========================================"
Write-Host "        CCLi 部署完成!"
Write-Host "========================================"
Write-Host ""
Write-Host "项目已安装到: $INSTALL_DIR"
Write-Host "配置文件位置: $CONFIG_DIR\config.json"
Write-Host ""
Write-Host "启动 CLI:"
Write-Host "  $INSTALL_DIR\start.bat"
Write-Host ""
Write-Host "启动 Web UI:"
Write-Host "  $INSTALL_DIR\start-web.bat"
Write-Host "  然后在浏览器中访问 http://localhost:8000"
Write-Host ""
Write-Host "请编辑 $CONFIG_DIR\config.json 文件添加您的 API 密钥"
Write-Host ""
Write-Host "查看帮助信息:"
Write-Host "  $INSTALL_DIR\venv\Scripts\python.exe ui/cli/ccli.py --help"
Write-Host ""