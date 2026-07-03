import sys
from pathlib import Path
from PyPDF2 import PdfReader

def extract_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    text = []
    for page_num, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text()
        if page_text:
            text.append(f"--- Page {page_num} ---\n{page_text}\n")
    return "\n".join(text)

def main():
    pdf_file = Path('T1-M1-3.pdf')
    if not pdf_file.exists():
        print(f"PDF not found: {pdf_file}")
        sys.exit(1)
    content = extract_text(pdf_file)
    output_file = Path('T1-M1-3_extracted.txt')
    output_file.write_text(content, encoding='utf-8')
    print(f"Extracted text saved to {output_file}")

if __name__ == '__main__':
    main()
