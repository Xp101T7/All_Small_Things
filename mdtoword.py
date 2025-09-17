# -*- coding: utf-8 -*-
"""
Convert a Markdown file to DOCX on Windows.
Requires: pip install pypandoc
Also install pandoc from https://github.com/jgm/pandoc/releases
"""

import sys
from pathlib import Path
import pypandoc

def md_to_docx(md_path: str, docx_path: str | None = None) -> str:
    """
    Convert a Markdown file to DOCX.
    - md_path: path to .md
    - docx_path: optional output path; defaults to same name with .docx
    """
    src = Path(md_path).expanduser().resolve()
    if not src.is_file():
        raise FileNotFoundError(f"Markdown file not found: {src}")

    dest = Path(docx_path).expanduser().resolve() if docx_path else src.with_suffix(".docx")

    # Convert text → docx using pandoc; ensure standalone metadata
    pypandoc.convert_text(
        src.read_text(encoding="utf-8"),
        "docx",
        format="md",
        outputfile=str(dest),
        extra_args=["--standalone"],
    )

    size = dest.stat().st_size
    if size <= 0:
        raise RuntimeError(f"Conversion produced empty file: {dest}")

    return f"✅ Converted: {src}  →  {dest}  ({size} bytes)"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_docx.py <markdown-file> [output-docx]")
        sys.exit(1)

    md_file = sys.argv[1]
    out_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        print(md_to_docx(md_file, out_file))
    except Exception as e:
        sys.stderr.write(f"❌ Error: {e}\n")
        sys.exit(2)