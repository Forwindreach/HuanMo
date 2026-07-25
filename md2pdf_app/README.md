<p align="center">
  <h1 align="center">换墨 · HuanMo</h1>
  <p align="center">Markdown → PDF · 中文字体自动适配 · 开箱即用</p>
</p>

---

## 简介

换墨是一款轻量级的 Markdown 转 PDF 本地工具。拖入 `.md` 文件，一键生成排版精美的 PDF，自动适配系统中文字体。无需联网，无需配置，一个 Python 脚本即可运行。

HuanMo is a lightweight local tool that converts Markdown files to PDF with automatic Chinese font detection. Drag in your `.md` files, click convert, and get a beautifully formatted PDF. No internet, no configuration — just a single Python script.

![screenshot](https://via.placeholder.com/800x500/f5f5f7/1d1d1f?text=HuanMo+UI)

## 特性

- **中文优先** — 自动检测 macOS / Linux / Windows 系统中的 CJK 字体
- **保留排版** — 标题层级、表格、列表、代码块、引用块完整保留
- **拖拽即用** — 浏览器界面，拖入文件即可转换
- **单文件架构** — 全部逻辑在一个 Python 脚本中，无数据库、无配置
- **完全离线** — 不依赖任何外部服务，数据不出本地

## 快速开始

### 环境要求

- Python 3.9+
- macOS / Windows / Linux

### 安装与启动

```bash
# 1. 克隆或下载本项目
git clone https://github.com/yourname/huanmo.git
cd huanmo

# 2. 安装依赖（仅首次）
pip install -r requirements.txt

# 3. 启动
python3 app.py
```

浏览器自动打开 `http://127.0.0.1:5199`，拖入 `.md` 文件即可。

**macOS 用户**也可双击 `启动.command` 一键启动。

**Windows 用户**可双击 `启动.bat`（需先安装 Python 3）。

## 使用说明

| 区域 | 功能 |
|------|------|
| 拖拽区 | 拖入 `.md` 文件或点击选择 |
| 文件列表 | 查看已选文件，点「移除」删掉不需要的 |
| 输出目录 | PDF 保存位置，默认 `~/Downloads` |
| 转换按钮 | 一键批量转换 |
| 结果列表 | 显示转换结果，点击「打开」查看 PDF |

## 常见问题

**Q: macOS 双击 `启动.command` 提示"无法打开"？**

右键点击文件 → 按住 `Option` 键 →「打开」→「打开」。只需操作一次。

**Q: PDF 里中文显示为方块？**

系统缺少中文字体。macOS / Windows 一般已自带。Linux 用户请安装：

```bash
sudo apt install fonts-wqy-zenhei
```

**Q: 端口被占用？**

编辑 `app.py`，将底部 `port = 5199` 改为其他端口号。

**Q: 需要联网吗？**

不需要。转换过程完全在本地完成，文件不会上传到任何地方。

## 项目结构

```
huanmo/
├── app.py            # 主程序（Flask + 前端 + 转换引擎）
├── requirements.txt  # Python 依赖
├── 启动.command       # macOS 一键启动
├── 启动.bat           # Windows 一键启动
└── README.md         # 本文件
```

## 技术栈

| 组件 | 用途 |
|------|------|
| [Flask](https://github.com/pallets/flask) | Web 服务 |
| [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | Markdown 解析 |
| [fpdf2](https://github.com/py-pdf/fpdf2) | PDF 生成 |
| 系统 CJK 字体 | 中文渲染（自动检测） |

## License

MIT
