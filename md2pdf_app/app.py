#!/usr/bin/env python3
"""
换墨 — 文档格式转换器
支持 Markdown / TXT / DOCX → PDF
启动后自动打开浏览器，拖拽文件即可转换。
"""

from __future__ import annotations

import base64
import logging
import os
import re
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

# ── Dependencies ──────────────────────────────────────────────
try:
    from flask import Flask, request, jsonify, send_file, render_template_string
except ImportError:
    sys.exit("需要 Flask: pip install flask")

try:
    from markdown_it import MarkdownIt
except ImportError:
    sys.exit("需要 markdown-it-py: pip install markdown-it-py")

try:
    from fpdf import FPDF, TextStyle
except ImportError:
    sys.exit("需要 fpdf2: pip install fpdf2")

# ── Logging ───────────────────────────────────────────────────
logging.getLogger("fpdf").setLevel(logging.ERROR)
logging.getLogger("fontTools").setLevel(logging.ERROR)
logging.getLogger("fontTools.subset").setLevel(logging.ERROR)
logging.getLogger("werkzeug").setLevel(logging.WARNING)

log = logging.getLogger("md2pdf-web")

# ── Cross-platform CJK font detection ─────────────────────────
FONT_CANDIDATES: dict[str, list[str]] = {
    "darwin": [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/PingFang.ttc",
    ],
    "linux": [
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
        "/usr/share/fonts/truetype/arphic/uming.ttc",
    ],
    "win32": [
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/mingliu.ttc",
    ],
}

_FPDF_FONT_NAME = "CJK"
_md_parser = MarkdownIt()


def detect_cjk_font() -> str | None:
    for path in FONT_CANDIDATES.get(sys.platform, []):
        if os.path.isfile(path):
            return path
    return None


def md_to_clean_html(text: str) -> str:
    html = _md_parser.render(text)
    html = re.sub(r"</?thead>", "", html)
    html = re.sub(r"</?tbody>", "", html)
    html = re.sub(r"<pre><code>", "<pre>", html)
    html = re.sub(r"</code></pre>", "</pre>", html)
    html = html.replace("<table>", '<table border="1">')
    return html


def convert_md_to_pdf_bytes(md_text: str, title: str, font_path: str) -> bytes:
    """Convert markdown text to PDF, return bytes."""
    html_body = md_to_clean_html(md_text)
    full_html = f"<h1>{title}</h1><hr>{html_body}"

    pdf = FPDF()
    pdf.add_font(_FPDF_FONT_NAME, style="", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="B", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="I", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="BI", fname=font_path)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.add_page()

    # Suppress fonttools noise
    import io as _io
    _stderr_ctx = (
        __import__("contextlib").redirect_stderr(_io.StringIO())
        if not os.environ.get("MD2PDF_DEBUG")
        else __import__("contextlib").nullcontext()
    )
    with _stderr_ctx:
        pdf.write_html(
            full_html,
            font_family=_FPDF_FONT_NAME,
            tag_styles={
                "pre": TextStyle(font_family=_FPDF_FONT_NAME, font_size_pt=10),
                "code": TextStyle(font_family=_FPDF_FONT_NAME, font_size_pt=10),
            },
        )

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    try:
        pdf.output(tmp.name)
        tmp.close()
        return Path(tmp.name).read_bytes()
    finally:
        os.unlink(tmp.name)


def convert_txt_to_pdf_bytes(text: str, title: str, font_path: str) -> bytes:
    """Convert plain text to PDF, preserving whitespace."""
    escaped = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    full_html = f"<h1>{title}</h1><hr><pre>{escaped}</pre>"

    pdf = FPDF()
    pdf.add_font(_FPDF_FONT_NAME, style="", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="B", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="I", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="BI", fname=font_path)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.add_page()

    import io as _io
    _stderr_ctx = (
        __import__("contextlib").redirect_stderr(_io.StringIO())
        if not os.environ.get("MD2PDF_DEBUG")
        else __import__("contextlib").nullcontext()
    )
    with _stderr_ctx:
        pdf.write_html(
            full_html,
            font_family=_FPDF_FONT_NAME,
            tag_styles={
                "pre": TextStyle(font_family=_FPDF_FONT_NAME, font_size_pt=11),
            },
        )

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    try:
        pdf.output(tmp.name)
        tmp.close()
        return Path(tmp.name).read_bytes()
    finally:
        os.unlink(tmp.name)


def convert_docx_to_pdf_bytes(docx_bytes: bytes, title: str, font_path: str) -> bytes:
    """Convert a .docx file to PDF via python-docx → HTML."""
    from io import BytesIO
    from docx import Document

    doc = Document(BytesIO(docx_bytes))

    html_parts = [f"<h1>{title}</h1><hr>"]

    for para in doc.paragraphs:
        text = para.text
        if not text.strip():
            html_parts.append("<br>")
            continue

        # Detect heading style
        style_name = para.style.name if para.style else ""
        if style_name.startswith("Heading"):
            level = style_name.replace("Heading", "").strip()
            try:
                lv = int(level)
            except ValueError:
                lv = 2
            lv = max(1, min(6, lv))
            html_parts.append(f"<h{lv}>{_escape_html(text)}</h{lv}>")
            continue

        # Inline formatting
        runs_html = []
        for run in para.runs:
            t = _escape_html(run.text)
            if not t:
                continue
            if run.bold:
                t = f"<b>{t}</b>"
            if run.italic:
                t = f"<i>{t}</i>"
            runs_html.append(t)
        para_html = "".join(runs_html) if runs_html else _escape_html(text)
        html_parts.append(f"<p>{para_html}</p>")

    # Tables
    for table in doc.tables:
        html_parts.append('<table border="1">')
        for row in table.rows:
            html_parts.append("<tr>")
            for cell in row.cells:
                html_parts.append(f"<td>{_escape_html(cell.text)}</td>")
            html_parts.append("</tr>")
        html_parts.append("</table>")
        html_parts.append("<br>")

    full_html = "".join(html_parts)

    pdf = FPDF()
    pdf.add_font(_FPDF_FONT_NAME, style="", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="B", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="I", fname=font_path)
    pdf.add_font(_FPDF_FONT_NAME, style="BI", fname=font_path)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_left_margin(25)
    pdf.set_right_margin(25)
    pdf.add_page()

    import io as _io
    _stderr_ctx = (
        __import__("contextlib").redirect_stderr(_io.StringIO())
        if not os.environ.get("MD2PDF_DEBUG")
        else __import__("contextlib").nullcontext()
    )
    with _stderr_ctx:
        pdf.write_html(
            full_html,
            font_family=_FPDF_FONT_NAME,
            tag_styles={
                "pre": TextStyle(font_family=_FPDF_FONT_NAME, font_size_pt=11),
            },
        )

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    try:
        pdf.output(tmp.name)
        tmp.close()
        return Path(tmp.name).read_bytes()
    finally:
        os.unlink(tmp.name)


def _escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── Flask App ─────────────────────────────────────────────────
app = Flask(__name__)

# Output directory – persisted in memory during session
OUTPUT_DIR = str(Path.home() / "Downloads")

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>换墨</title>
<style>
  :root {
    --bg: #f5f5f7;
    --card: #ffffff;
    --text: #1d1d1f;
    --secondary: #86868b;
    --accent: #0071e3;
    --border: #d2d2d7;
    --hover: #f0f0f2;
    --radius: 12px;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "PingFang SC", "Helvetica Neue", sans-serif;
    background: var(--bg);
    color: var(--text);
    display: flex; justify-content: center;
    min-height: 100vh; padding: 40px 20px;
    -webkit-font-smoothing: antialiased;
  }
  .container { width: 100%; max-width: 600px; }
  h1 {
    font-size: 28px; font-weight: 700;
    text-align: center; margin-bottom: 4px;
    letter-spacing: -0.5px;
  }
  .subtitle { text-align: center; color: var(--secondary); font-size: 14px; margin-bottom: 32px; }

  /* Drop zone */
  .drop-zone {
    background: var(--card);
    border: 2px dashed var(--border);
    border-radius: var(--radius);
    padding: 48px 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    margin-bottom: 20px;
  }
  .drop-zone:hover, .drop-zone.drag-over {
    border-color: var(--accent);
    background: #f0f4ff;
  }
  .drop-zone .icon { font-size: 40px; margin-bottom: 12px; }
  .drop-zone p { color: var(--secondary); font-size: 15px; }
  .drop-zone .browse { color: var(--accent); font-weight: 500; }

  /* File list */
  .file-list {
    background: var(--card);
    border-radius: var(--radius);
    overflow: hidden;
    margin-bottom: 20px;
    display: none;
  }
  .file-list.has-files { display: block; }
  .file-list-header {
    font-size: 13px; font-weight: 600;
    color: var(--secondary); text-transform: uppercase;
    padding: 14px 20px 8px;
  }
  .file-item {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 20px; border-top: 1px solid #f0f0f0;
    font-size: 15px;
  }
  .file-item .name { display: flex; align-items: center; gap: 10px; overflow: hidden; }
  .file-item .name span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .file-item .remove {
    background: none; border: none; color: #ff3b30;
    cursor: pointer; font-size: 14px; padding: 4px 8px;
    border-radius: 6px; opacity: 0.6; transition: all 0.15s;
  }
  .file-item .remove:hover { opacity: 1; background: #fff0f0; }

  /* Output dir */
  .output-row {
    display: flex; gap: 10px; align-items: center;
    margin-bottom: 20px;
  }
  .output-row label { font-size: 14px; font-weight: 500; white-space: nowrap; }
  .output-row input {
    flex: 1; padding: 10px 14px;
    border: 1px solid var(--border); border-radius: 8px;
    font-size: 14px; background: var(--card);
    font-family: "SF Mono", "Menlo", "Consolas", monospace;
  }
  .output-row input:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px rgba(0,113,227,0.15); }
  .btn-outline {
    padding: 10px 16px;
    border: 1px solid var(--border); border-radius: 8px;
    background: var(--card); font-size: 14px;
    cursor: pointer; white-space: nowrap;
    transition: all 0.15s;
  }
  .btn-outline:hover { background: var(--hover); }

  /* Convert button */
  .btn-convert {
    width: 100%; padding: 14px;
    background: var(--accent); color: #fff;
    border: none; border-radius: 10px;
    font-size: 17px; font-weight: 600;
    cursor: pointer; transition: all 0.15s;
    letter-spacing: -0.2px;
  }
  .btn-convert:hover { opacity: 0.92; }
  .btn-convert:disabled { opacity: 0.4; cursor: not-allowed; }
  .btn-convert .spinner { display: none; }
  .btn-convert.loading .spinner { display: inline-block; margin-right: 8px; animation: spin 0.8s linear infinite; }
  .btn-convert.loading .btn-text { display: none; }
  @keyframes spin { to { transform: rotate(360deg); } }

  /* Results */
  .results { margin-top: 24px; display: none; }
  .results.has-results { display: block; }
  .results-header {
    font-size: 13px; font-weight: 600;
    color: var(--secondary); text-transform: uppercase;
    margin-bottom: 8px;
  }
  .result-item {
    display: flex; align-items: center; justify-content: space-between;
    background: var(--card); border-radius: 10px;
    padding: 14px 20px; margin-bottom: 8px;
    font-size: 15px;
  }
  .result-item .status { font-size: 18px; margin-right: 10px; }
  .result-item .info { flex: 1; }
  .result-item .info .filename { font-weight: 500; }
  .result-item .info .size { font-size: 13px; color: var(--secondary); }
  .result-item .open-btn {
    padding: 8px 16px; background: var(--accent); color: #fff;
    border: none; border-radius: 6px; font-size: 14px;
    cursor: pointer; text-decoration: none; transition: all 0.15s;
  }
  .result-item .open-btn:hover { opacity: 0.9; }
  .result-item.error .status { color: #ff3b30; }
  .result-item.error .info { color: #ff3b30; }

  /* Footer */
  .footer {
    text-align: center; color: var(--secondary);
    font-size: 12px; margin-top: 40px;
  }

  input[type="file"] { display: none; }
</style>
</head>
<body>
<div class="container">
  <h1>换墨</h1>
  <p class="subtitle">Markdown / TXT / DOCX → PDF · 中文字体自动检测</p>

  <!-- Drop zone -->
  <div class="drop-zone" id="dropZone">
    <div class="icon"><svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#86868b" stroke-width="1.5" stroke-linecap="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="12" y1="18" x2="12" y2="12"/><polyline points="9 15 12 18 15 15"/></svg></div>
    <p>拖拽 <strong>.md / .txt / .docx 文件</strong> 到此处<br>或 <span class="browse">点击浏览</span></p>
  </div>
  <input type="file" id="fileInput" accept=".md,.markdown,.txt,.text,.docx" multiple>

  <!-- File list -->
  <div class="file-list" id="fileList">
    <div class="file-list-header">已选文件 (<span id="fileCount">0</span>)</div>
    <div id="fileItems"></div>
  </div>

  <!-- Output dir -->
  <div class="output-row">
    <label for="outputDir">输出到</label>
    <input type="text" id="outputDir" value="{{ output_dir }}">
    <button class="btn-outline" id="pickOutput">选择…</button>
  </div>

  <!-- Convert -->
  <button class="btn-convert" id="btnConvert" disabled>
    <span class="spinner">···</span>
    <span class="btn-text">开始转换</span>
  </button>

  <!-- Results -->
  <div class="results" id="results">
    <div class="results-header">转换结果</div>
    <div id="resultItems"></div>
  </div>

  <p class="footer">换墨 · macOS / Linux / Windows</p>
</div>

<script>
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileList = document.getElementById('fileList');
const fileCount = document.getElementById('fileCount');
const fileItems = document.getElementById('fileItems');
const btnConvert = document.getElementById('btnConvert');
const outputDir = document.getElementById('outputDir');
const results = document.getElementById('results');
const resultItems = document.getElementById('resultItems');

let files = new Map(); // name -> content (base64)

// ── File handling ─────────────────────────────────────────
dropZone.addEventListener('click', () => fileInput.click());

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('drag-over');
  addFiles(e.dataTransfer.files);
});

fileInput.addEventListener('change', () => {
  addFiles(fileInput.files);
  fileInput.value = '';
});

function addFiles(fileList) {
  for (const f of fileList) {
    if (!f.name.endsWith('.md') && !f.name.endsWith('.markdown') && !f.name.endsWith('.txt') && !f.name.endsWith('.text') && !f.name.endsWith('.docx')) continue;
    const reader = new FileReader();
    reader.onload = () => {
      files.set(f.name, reader.result.split(',')[1]); // base64 content
      renderFileList();
    };
    reader.readAsDataURL(f);
  }
}

function renderFileList() {
  fileItems.innerHTML = '';
  let i = 0;
  for (const [name] of files) {
    const div = document.createElement('div');
    div.className = 'file-item';
    div.innerHTML = `
      <div class="name"><span>${esc(name)}</span></div>
      <button class="remove" data-name="${esc(name)}">移除</button>
    `;
    fileItems.appendChild(div);
    i++;
  }
  fileCount.textContent = files.size;
  if (files.size > 0) {
    fileList.classList.add('has-files');
    btnConvert.disabled = false;
  } else {
    fileList.classList.remove('has-files');
    btnConvert.disabled = true;
  }

  // Bind remove buttons
  fileItems.querySelectorAll('.remove').forEach(btn => {
    btn.addEventListener('click', () => {
      files.delete(btn.dataset.name);
      renderFileList();
    });
  });
}

// ── Convert ────────────────────────────────────────────────
btnConvert.addEventListener('click', async () => {
  if (files.size === 0) return;

  btnConvert.classList.add('loading');
  btnConvert.disabled = true;
  results.classList.remove('has-results');
  resultItems.innerHTML = '';

  const dir = outputDir.value.trim() || '{{ output_dir }}';

  for (const [name, b64] of files) {
    const itemDiv = document.createElement('div');
    itemDiv.className = 'result-item';
    itemDiv.innerHTML = `<span class="status">·</span><div class="info"><div class="filename">${esc(name)}</div><div class="size">转换中…</div></div>`;
    resultItems.appendChild(itemDiv);

    try {
      const resp = await fetch('/convert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, content: b64, output_dir: dir }),
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.error || '未知错误');
      }

      const data = await resp.json();
      itemDiv.innerHTML = `
        <span class="status">&#10003;</span>
        <div class="info"><div class="filename">${esc(data.filename)}</div><div class="size">${data.size_kb} KB</div></div>
        <a class="open-btn" href="/download/${encodeURIComponent(data.token)}" target="_blank">打开</a>
      `;
    } catch (err) {
      itemDiv.classList.add('error');
      itemDiv.innerHTML = `
        <span class="status">&#10007;</span>
        <div class="info"><div class="filename">${esc(name)}</div><div class="size">${esc(err.message)}</div></div>
      `;
    }
  }

  results.classList.add('has-results');
  btnConvert.classList.remove('loading');
  btnConvert.disabled = false;
});

// ── Output picker ─────────────────────────────────────────
document.getElementById('pickOutput').addEventListener('click', async () => {
  try {
    const resp = await fetch('/pick-folder', { method: 'POST' });
    const data = await resp.json();
    if (data.path) outputDir.value = data.path;
  } catch (err) {
    alert('选择目录出错，请手动输入路径');
  }
});

outputDir.addEventListener('change', () => updateOutputDir());
function updateOutputDir() {
  fetch('/set-output-dir', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path: outputDir.value.trim() }),
  });
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
</script>
</body>
</html>"""

# ── Routes ────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, output_dir=OUTPUT_DIR)


@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    name = data.get("name", "untitled.md")
    b64_content = data.get("content", "")
    output_dir = data.get("output_dir", OUTPUT_DIR)

    ext = Path(name).suffix.lower()

    # Decode base64 — text for md/txt, binary for docx
    try:
        raw_bytes = base64.b64decode(b64_content)
        if ext == ".docx":
            text = None  # binary, handled separately
        else:
            text = raw_bytes.decode("utf-8")
    except Exception as e:
        return jsonify({"error": f"文件解码失败: {e}"}), 400

    # Font
    font = detect_cjk_font()
    if not font:
        return jsonify({"error": "未检测到中文字体，请安装字体后重试"}), 500

    # Output dir
    out_path = Path(output_dir)
    try:
        out_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return jsonify({"error": f"无法创建输出目录: {e}"}), 400

    # Determine file type and convert
    title = Path(name).stem.replace("_", " ")

    try:
        if ext == ".txt":
            pdf_bytes = convert_txt_to_pdf_bytes(text, title, font)
        elif ext == ".docx":
            pdf_bytes = convert_docx_to_pdf_bytes(raw_bytes, title, font)
        else:
            pdf_bytes = convert_md_to_pdf_bytes(text, title, font)
    except Exception as e:
        return jsonify({"error": f"转换失败: {e}"}), 500

    # Save to output dir
    pdf_name = Path(name).with_suffix(".pdf").name
    pdf_path = out_path / pdf_name
    try:
        pdf_path.write_bytes(pdf_bytes)
    except OSError as e:
        return jsonify({"error": f"写入文件失败: {e}"}), 500

    # Store in a simple in-memory registry for /download
    token = base64.urlsafe_b64encode(str(pdf_path).encode()).decode()
    _downloads[token] = str(pdf_path)

    return jsonify({
        "filename": pdf_name,
        "size_kb": round(len(pdf_bytes) / 1024),
        "token": token,
    })


_downloads: dict[str, str] = {}


@app.route("/download/<token>")
def download(token):
    path = _downloads.get(token)
    if not path or not os.path.isfile(path):
        return "文件不存在或已过期", 404
    return send_file(path, as_attachment=True)


@app.route("/set-output-dir", methods=["POST"])
def set_output_dir():
    global OUTPUT_DIR
    data = request.get_json()
    p = data.get("path", "").strip()
    if p and os.path.isdir(os.path.dirname(p) if not os.path.isdir(p) else p):
        OUTPUT_DIR = p
    return jsonify({"ok": True})


@app.route("/pick-folder", methods=["POST"])
def pick_folder():
    """Use AppleScript on macOS to open a folder picker dialog."""
    global OUTPUT_DIR
    if sys.platform != "darwin":
        return jsonify({"path": OUTPUT_DIR})
    import subprocess
    script = '''
        tell application "System Events"
            activate
            set f to choose folder with prompt "选择 PDF 输出目录:" default location path to downloads folder
            POSIX path of f
        end tell
    '''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=30,
        )
        path = result.stdout.strip()
        if path:
            OUTPUT_DIR = path
            return jsonify({"path": path})
    except Exception:
        pass
    return jsonify({"path": OUTPUT_DIR})


# ── Main ──────────────────────────────────────────────────────

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    port = 5199
    url = f"http://127.0.0.1:{port}"

    print("╔══════════════════════════════════════╗")
    print("║       换墨 — Markdown → PDF          ║")
    print("╠══════════════════════════════════════╣")
    print(f"║  浏览器地址: {url}          ║")
    print("║  按 Ctrl+C 停止服务                  ║")
    print("╚══════════════════════════════════════╝")

    # Auto-open browser after a short delay
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()

    app.run(host="127.0.0.1", port=port, debug=False)


if __name__ == "__main__":
    main()
