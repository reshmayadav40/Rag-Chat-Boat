from pathlib import Path
from pypdf import PdfReader


def load_pdf(pdf_path: str):
    """
    Read a PDF page by page and return text
    with source file and page number.
    """

    pdf_path = Path(pdf_path)

    reader = PdfReader(pdf_path)

    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        if text and text.strip():
            documents.append({
                "text": text.strip(),
                "metadata": {
                    "source": pdf_path.name,
                    "page": page_number
                }
            })

    return documents