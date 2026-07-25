# md2pdf — Markdown → PDF 转换器

拖拽 `.md` 文件 → 点转换 → 得到排版精美的 PDF。中文字体自动适配。

---

## 使用方法

### 🖥 对方也是 Mac

将整个 `md2pdf_app` 文件夹发给对方，对方：

1. **双击 `启动.command`**（首次可能需右键 → 打开）
2. 首次运行会自动安装依赖（需要网络，约 10 秒）
3. 浏览器自动打开界面
4. 拖入 `.md` 文件，点「开始转换」

### 🪟 对方是 Windows

1. 安装 [Python 3](https://www.python.org/downloads/)（勾选 "Add to PATH"）
2. **双击 `启动.bat`**
3. 浏览器自动打开界面

### 🐧 对方是 Linux

```bash
cd md2pdf_app
pip install -r requirements.txt
python3 app.py
```

---

## 分发方式

### 方式一：直接发文件夹（推荐）

把 `md2pdf_app` 文件夹压缩成 zip 发给对方，对方解压后双击启动。

### 方式二：GitHub 下载

如果放在 GitHub 上，对方 clone 后：

```bash
cd md2pdf_app
pip install -r requirements.txt
python3 app.py
```

### 方式三：U 盘 / 内网共享

整个文件夹拷贝即可，无需安装任何东西（除了 Python 3）。

---

## 界面说明

| 区域 | 功能 |
|------|------|
| 拖拽区 | 拖入 `.md` 文件或点击选择 |
| 文件列表 | 查看已选文件，点「移除」删掉不要的 |
| 输出目录 | PDF 保存位置，默认 `~/Downloads` |
| 转换按钮 | 一键批量转换 |
| 结果列表 | 显示每个文件的转换结果 + 打开按钮 |

---

## 常见问题

**Q: 双击 `启动.command` 提示"无法打开"？**
A: 右键点击 → 按住 Option 键 → 「打开」→ 「打开」。只需一次，之后正常双击即可。

**Q: 中文在 PDF 里显示为方块？**
A: 系统缺少中文字体。Mac/Windows 一般都有，Linux 需安装：
```bash
sudo apt install fonts-wqy-zenhei
```

**Q: 如何改端口？**
A: 编辑 `app.py`，找到 `port = 5199` 改成别的数字。

---

## 技术栈

| 组件 | 用途 |
|------|------|
| Flask | Web 服务 |
| markdown-it-py | Markdown 解析 |
| fpdf2 | PDF 生成 |
| 系统字体 | 中文渲染（自动检测） |
