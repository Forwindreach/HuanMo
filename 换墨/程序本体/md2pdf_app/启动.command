#!/bin/bash
# md2pdf 一键启动脚本 (macOS)
# 双击此文件即可启动

cd "$(dirname "$0")"

echo "=============================="
echo "  md2pdf — Markdown → PDF"
echo "=============================="
echo ""

# 检查 Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 python3，请先安装 Python 3"
    echo "   下载地址: https://www.python.org/downloads/"
    read -p "按任意键退出..."
    exit 1
fi

# 安装依赖（如果需要）
echo "📦 检查依赖..."
python3 -m pip install -q flask markdown-it-py fpdf2 2>/dev/null

# 启动
echo "🚀 启动中..."
python3 app.py
