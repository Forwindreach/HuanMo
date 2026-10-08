<p align="center">
  <img src=".github/assets/hero.svg" alt="HuanMo — local-first document toolkit" width="100%">
</p>

<p align="center">
  <strong>English</strong> · <a href="README.md">简体中文</a>
</p>

<p align="center">
  <a href="https://github.com/Forwindreach/HuanMo/releases/latest"><img alt="GitHub Release" src="https://img.shields.io/github/v/release/Forwindreach/HuanMo?style=flat-square&color=1677ff"></a>
  <a href="https://github.com/Forwindreach/HuanMo/actions/workflows/quality.yml"><img alt="Quality" src="https://img.shields.io/github/actions/workflow/status/Forwindreach/HuanMo/quality.yml?branch=main&style=flat-square&label=quality"></a>
  <a href="LICENSE"><img alt="License" src="https://img.shields.io/github/license/Forwindreach/HuanMo?style=flat-square&color=20a66a"></a>
  <img alt="Platforms" src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows-59636e?style=flat-square">
  <img alt="Privacy" src="https://img.shields.io/badge/privacy-100%25%20local-8b5cf6?style=flat-square">
</p>

<p align="center">
  <strong>A free, open-source, local-first document toolkit.</strong><br>
  Convert documents, scan phone photos, and rearrange PDFs without uploading private files.
</p>

<p align="center">
  <a href="https://github.com/Forwindreach/HuanMo/releases/latest/download/HuanMo-macOS.zip"><strong>Download for macOS</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://github.com/Forwindreach/HuanMo/releases/latest/download/HuanMo.exe"><strong>Download for Windows</strong></a>
  &nbsp;&nbsp;·&nbsp;&nbsp;
  <a href="https://github.com/Forwindreach/HuanMo/releases/latest">All releases</a>
</p>

---

## Why HuanMo?

Online PDF tools often require sensitive uploads, while traditional desktop suites can be heavy and expensive. HuanMo keeps the workflow simple and the data on your computer.

| Convert documents | Scan documents | Merge PDF pages |
|:---:|:---:|:---:|
| Markdown, TXT, and Word to PDF | Detect paper and correct perspective | Preview, delete, and reorder pages |
| Automatic CJK font selection | Original color, enhanced color, or B&W | Combine pages across multiple files |
| Batch conversion | HEIC and common image formats | Reject encrypted PDFs safely |

### Principles

- **Privacy first** — processing happens locally; files are never uploaded.
- **Ready to use** — download the desktop build without setting up Python.
- **Preview before export** — inspect scan and merge results before writing the final file.
- **Cross-platform** — automated macOS and Windows builds.
- **Open and auditable** — MIT-licensed source with a deliberately compact architecture.

## Install

### macOS

Download [`HuanMo-macOS.zip`](https://github.com/Forwindreach/HuanMo/releases/latest/download/HuanMo-macOS.zip), unzip it, and open `HuanMo.app`.

> If macOS cannot verify the developer, right-click the app, choose **Open**, and confirm. The app is not currently code-signed by Apple.

### Windows

Download [`HuanMo.exe`](https://github.com/Forwindreach/HuanMo/releases/latest/download/HuanMo.exe) and run it.

> If SmartScreen appears, choose **More info** → **Run anyway**. Release binaries are built from the public source by GitHub Actions.

## Features

### Document conversion

Convert `.md`, `.txt`, and `.docx` files to PDF. Markdown supports headings, tables, code blocks, and quotes. Word conversion covers common text styles and simple tables.

### Mobile document scanning

Import one or more phone photos, correct perspective when a reliable page boundary is detected, and choose one of three output styles:

- **Keep original colors** — the default for IDs, colored documents, and images.
- **Color enhancement** — improves luminance and text edges while preserving hue.
- **Black and white** — a high-contrast scan for text-heavy documents.

Preview, rotate, remove, and reorder pages before exporting a single A4 PDF.

### Page-level PDF merging

Add multiple PDFs, preview every page, delete pages you do not need, drag pages across files, and export the exact order you want.

## Supported formats

| Input | Extensions | Support |
|---|---|---|
| Markdown | `.md` `.markdown` | Headings, lists, tables, code blocks, quotes |
| Plain text | `.txt` `.text` | Preserved whitespace and line breaks |
| Word | `.docx` | Headings, bold, italic, simple tables |
| Images | `.jpg` `.jpeg` `.png` `.webp` `.bmp` `.tif` `.tiff` `.heic` `.heif` | Crop, perspective correction, enhancement, ordering |
| PDF | `.pdf` | Preview, page removal, reordering, merging |

## Privacy model

```text
Your files  →  processing on 127.0.0.1  →  your chosen output folder
                         │
                         └── no upload, no account, no cloud retention
```

HuanMo listens only on the loopback address `127.0.0.1:5199`. Temporary previews are stored in the operating system's temporary directory. See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Run from source

Python 3.9 or newer is required:

```bash
git clone https://github.com/Forwindreach/HuanMo.git
cd HuanMo
python3 -m pip install -r md2pdf_app/requirements.txt
python3 md2pdf_app/app.py
```

Then open <http://127.0.0.1:5199>.

## Roadmap

- [x] Markdown / TXT / DOCX to PDF
- [x] Page-level PDF preview, deletion, ordering, and merging
- [x] Perspective correction and three scan styles
- [x] HEIC / HEIF support
- [ ] Manual scan-corner adjustment
- [ ] OCR and searchable PDFs
- [ ] Configurable page sizes and margins
- [ ] Standalone Linux build

The roadmap is directional, not a delivery commitment.

## Contributing

Bug reports, feature proposals, documentation improvements, and code contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) before getting started.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## License

Released under the [MIT License](LICENSE).

<p align="center">
  If HuanMo is useful to you, consider giving the project a ⭐ Star.
</p>
