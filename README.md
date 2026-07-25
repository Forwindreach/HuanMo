<p align="center">
  <h1 align="center">换墨 · HuanMo</h1>
  <p align="center">Markdown / TXT / DOCX → PDF · 中文字体自动适配 · 开箱即用</p>
</p>

---

## 简介

换墨是一款轻量级的文档转 PDF 本地工具。支持 Markdown、TXT、Word 文档，拖入即转，自动适配系统中文字体。无需联网，无需配置，一个 Python 脚本即可运行。

## 支持格式

| 输入格式 | 说明 |
|----------|------|
| `.md` `.markdown` | Markdown 文档，保留标题、表格、代码块、引用 |
| `.txt` `.text` | 纯文本文件，保留原始排版 |
| `.docx` | Word 文档，保留标题层级、粗体斜体、表格 |

## 快速开始

### 环境要求

- Python 3.9+（macOS 已自带，Windows 需从 [python.org](https://www.python.org) 下载）

### 安装与启动

```bash
# 1. 下载项目
https://github.com/Forwindreach/HuanMo.git
cd 文件路径（复制你自己电脑上的文件路径）

# 2. 启动
python3 app.py
```

> `requirements.txt` 列出了项目用到的第三方 Python 库（Flask、fpdf2 等）。
> 这些库的代码不在本项目里，需要用 pip 从网络下载安装。只需装一次。

浏览器自动打开 `http://127.0.0.1:5199`，拖入文件即可。

**macOS 用户**也可双击 `启动.command` 一键启动（首次会自动安装依赖）。

**Windows 用户**可双击 `启动.bat`（需先安装 Python 3，启动时会自动装依赖）。

## 使用说明

| 区域 | 功能 |
|------|------|
| 拖拽区 | 拖入 `.md` / `.txt` / `.docx` 文件或点击选择 |
| 文件列表 | 查看已选文件，点「移除」删掉不需要的 |
| 输出目录 | PDF 保存位置，默认 `~/Downloads` |
| 转换按钮 | 一键批量转换 |
| 结果列表 | 显示转换结果，点击「打开」查看 PDF |

## 常见问题

**Q: `pip install` 是什么？为什么不直接把依赖放在项目里？**

换墨依赖了几个开源 Python 库（Flask 做网页、fpdf2 生成 PDF 等）。`requirements.txt` 是购物清单，`pip install -r requirements.txt` 就是照单采购。不把这些库的代码打包进项目是因为：
- 保持项目体积小（只有自己的代码）
- 依赖库各自独立更新，有问题可以单独升级

**Q: macOS 双击 `启动.command` 提示"无法打开"？**

右键点击文件 → 按住 `Option` 键 →「打开」→「打开」。只需操作一次。

**Q: PDF 里中文显示为方块？**

系统缺少中文字体。macOS / Windows 一般已自带。Linux 用户请安装：

```bash
sudo apt install fonts-wqy-zenhei
```

**Q: 端口被占用？**

编辑 `app.py`，将底部 `port = 5199` 改为其他端口号。

**Q: DOCX 转换后格式不对？**

python-docx 对复杂表格（合并单元格等）和图片不支持。简单文档可正常转换。

## 项目结构

```
huanmo/
├── README.md
└── md2pdf_app/
    ├── app.py            # 主程序（Flask + 前端 + 转换引擎，约 700 行）
    ├── requirements.txt  # Python 依赖清单
    ├── 启动.command       # macOS 一键启动
    └── 启动.bat           # Windows 一键启动
```

## 技术栈

| 组件 | 用途 |
|------|------|
| [Flask](https://github.com/pallets/flask) | Web 服务 |
| [markdown-it-py](https://github.com/executablebooks/markdown-it-py) | Markdown 解析 |
| [python-docx](https://github.com/python-openxml/python-docx) | DOCX 解析 |
| [fpdf2](https://github.com/py-pdf/fpdf2) | PDF 生成 |
| 系统 CJK 字体 | 中文渲染（自动检测） |

## License

MIT
