<p align="center">
  <h1 align="center">换墨 · HuanMo</h1>
  <p align="center">Markdown / TXT / DOCX → PDF · PDF 合并 · 中文字体自动适配 · 开箱即用</p>
</p>

---

## 简介

换墨是一款轻量级的文档处理本地工具。支持 Markdown、TXT、Word 文档转 PDF，也支持把多个 PDF 按顺序合并成一个文件。拖入即转，自动适配系统中文字体。无需联网，无需配置，一个 Python 脚本即可运行。

## 支持格式

| 输入格式 | 说明 |
|----------|------|
| `.md` `.markdown` | Markdown 文档，保留标题、表格、代码块、引用 |
| `.txt` `.text` | 纯文本文件，保留原始排版 |
| `.docx` | Word 文档，保留标题层级、粗体斜体、表格 |
| `.pdf` | 多个 PDF 文件可逐页预览、删除不需要的页面、拖拽调整顺序后合并 |

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

## 独立程序（免安装 Python）

不想安装 Python 的用户可以直接到 GitHub Releases 下载成品，双击即可运行：

- macOS：下载 `HuanMo-macOS.zip`，解压后打开 `HuanMo.app`
- Windows：下载 `HuanMo-Windows.exe`，双击运行

每次推送 `v1.0.0` 这类 tag，GitHub Actions 会自动打包两个平台的成品并附到 Release。

如果想在自己电脑上手动打包：

```bash
pip install -r md2pdf_app/requirements.txt pyinstaller
python build_app.py
```

macOS 输出在 `dist/HuanMo.app`，Windows 输出在 `dist/HuanMo.exe`。

## 使用说明

| 区域 | 功能 |
|------|------|
| 模式切换 | 「文档转 PDF」转换文档，「合并 PDF」合并多个 PDF |
| 拖拽区 | 按当前模式拖入对应文件，或点击选择 |
| 文件列表 | 查看已选文件，点「移除」删掉不需要的 |
| 页面编辑器 | 合并模式下列出所有 PDF 页面，点击放大浏览，点 × 删除，拖拽调整顺序 |
| 输出目录 | PDF 保存位置，默认 `~/Downloads` |
| 转换按钮 | 文档模式批量转换，PDF 模式一键合并 |
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

**Q: PDF 合并失败？**

加密的 PDF 需要先解除密码保护，无法直接合并；请确保选择的是普通可阅读的 PDF。

**Q: PDF 页面没有预览图？**

预览渲染依赖 `pypdfium2`。启动脚本会自动安装，如果手动启动，请先执行 `pip install pypdfium2`。没有预览时仍可正常合并，只是看不到页面缩略图。

**Q: 我不想安装 Python，能直接用吗？**

可以。到 GitHub Releases 下载对应系统的成品（macOS 的 `.app` 或 Windows 的 `.exe`），双击即可运行，无需安装任何环境。

**Q: macOS 打开成品提示“无法验证开发者”？**

成品尚未做 Apple 签名，首次打开时请右键点击 `HuanMo.app` → 选择「打开」→ 再次点击「打开」即可。

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
| [pypdf](https://github.com/py-pdf/pypdf) | PDF 合并 |
| [pypdfium2](https://github.com/pypdfium2-team/pypdfium2) | PDF 页面预览渲染 |
| 系统 CJK 字体 | 中文渲染（自动检测） |

## License

MIT
