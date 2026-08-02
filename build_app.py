#!/usr/bin/env python3
"""Build a standalone HuanMo app with PyInstaller (macOS .app / Windows .exe)."""

import platform
import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP = ROOT / "md2pdf_app" / "app.py"


def main() -> int:
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name",
        "HuanMo",
        "--collect-all",
        "pypdfium2",
        str(APP),
    ]
    if platform.system() == "Darwin":
        cmd += ["--onedir", "--windowed"]
    else:
        cmd += ["--onefile", "--windowed"]

    # Keep pypdfium2_raw Python modules next to pdfium.dll so the frozen app
    # can resolve the native library without relying on the working directory.
    try:
        import pypdfium2_raw
        raw_dir = Path(pypdfium2_raw.__file__).resolve().parent
        sep = ";" if os.name == "nt" else ":"
        cmd += ["--add-data", f"{raw_dir}{sep}pypdfium2_raw"]
    except ImportError:
        pass

    print("Running:", " ".join(cmd))
    return subprocess.call(cmd, cwd=ROOT)


if __name__ == "__main__":
    raise SystemExit(main())
