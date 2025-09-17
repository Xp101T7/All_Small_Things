from markdown import markdown
from docx import Document
from bs4 import BeautifulSoup  # pip install beautifulsoup4

def md_to_docx(md_file, out_file):
    # Read the markdown file
    text = open(md_file, encoding="utf-8").read()

    # Convert markdown -> HTML
    html = markdown(text)

    # Parse HTML so we can keep headings, paragraphs, lists, etc.
    soup = BeautifulSoup(html, "html.parser")

    doc = Document()

    for element in soup.children:
        if element.name == "h1":
            doc.add_heading(element.get_text(), level=1)
        elif element.name == "h2":
            doc.add_heading(element.get_text(), level=2)
        elif element.name == "ul":
            for li in element.find_all("li"):
                doc.add_paragraph(li.get_text(), style="List Bullet")
        elif element.name == "ol":
            for li in element.find_all("li"):
                doc.add_paragraph(li.get_text(), style="List Number")
        else:
            doc.add_paragraph(element.get_text())

    doc.save(out_file)
    print(f"Saved DOCX to: {out_file}")

# Usage:
# pip install markdown python-docx beautifulsoup4
# python script.py