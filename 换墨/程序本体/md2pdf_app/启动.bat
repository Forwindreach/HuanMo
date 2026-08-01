@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ==============================
echo   md2pdf — Markdown → PDF
echo ==============================
echo.

:: 检查 Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 未找到 Python，请先安装 Python 3
    echo    https://www.python.org/downloads/
    pause
    exit /b 1
)

:: 安装依赖
echo 📦 检查依赖...
python -m pip install -q flask markdown-it-py fpdf2 2>nul

:: 启动
echo 🚀 启动中...
python app.py
pause
