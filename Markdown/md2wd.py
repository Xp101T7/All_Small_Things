#!/usr/bin/env python3
# md2docx.py — Convert Markdown (.md) to Word (.docx) WITHOUT pandoc.
# deps: pip install markdown htmldocx python-docx beautifulsoup4

import argparse
from pathlib import Path
from markdown import markdown
from docx import Document
from htmldocx import HtmlToDocx

def md_to_docx(md_file: str, out_file: str) -> None:
    md_text = Path(md_file).read_text(encoding="utf-8")
    # 'extra' bundles tables, fenced_code, etc.; add 'toc' for headings-based TOC ids
    html = markdown(md_text, extensions=["extra", "toc"])
    doc = Document()
    HtmlToDocx().add_html_to_document(html, doc)
    out_path = Path(out_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_path))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Convert Markdown to DOCX without pandoc")
    ap.add_argument("input_md", help="Path to input .md file")
    ap.add_argument("-o", "--output", help="Path to output .docx (default: input name with .docx)")
    args = ap.parse_args()

    output = args.output or str(Path(args.input_md).with_suffix(".docx"))
    md_to_docx(args.input_md, output)
    print(f"Wrote: {output}")
