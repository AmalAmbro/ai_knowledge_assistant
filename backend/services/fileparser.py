from fastapi import UploadFile
from typing import Union
import io

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return _extract_pdf(file)
    elif filename.endswith(".docx"):
        return _extract_docx(file)
    elif filename.endswith(".txt"):
        return _extract_txt(file)
    else:
        raise ValueError("Unsupported file type")


def _extract_pdf(file: UploadFile) -> str:
    reader = PdfReader(io.BytesIO(file.file.read()))
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def _extract_docx(file: UploadFile) -> str:
    doc = Document(io.BytesIO(file.file.read()))
    return "\n".join(p.text for p in doc.paragraphs)


def _extract_txt(file: UploadFile) -> str:
    return file.file.read().decode("utf-8", errors="ignore")
