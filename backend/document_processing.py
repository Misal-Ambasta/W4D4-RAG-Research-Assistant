"""Document processing utilities for PDFs, including text extraction, OCR, and metadata.

This module provides a single public function `process_pdf(file: UploadFile)` that
returns a list of LangChain `Document` objects ready to be embedded and added to
our vector store.
"""

from __future__ import annotations

import io
import re
import tempfile
from datetime import datetime
from typing import List

import pdfplumber
from fastapi import UploadFile
from langchain_core.documents import Document as LCDocument
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# OCR dependencies
try:
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover
    pytesseract = None  # type: ignore
    Image = None  # type: ignore


CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def _parse_pdf_date(date_obj):
    """Safely parse PDF date strings, which may be malformed."""
    if not date_obj:
        return None

    date_str = str(date_obj)  # Works for PyPDF2's TextStringObject
    if date_str.startswith("D:"):
        date_str = date_str[2:]

    # PyPDF2 can add an apostrophe in the timezone, e.g., +05'30'
    date_str = date_str.replace("'", "")

    # Try parsing with timezone, then without.
    for fmt in ("%Y%m%d%H%M%S%z", "%Y%m%d%H%M%S"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue

    # If all parsing fails, return the original string representation
    return str(date_obj)


def _extract_metadata(reader: PdfReader) -> dict:
    """Extract metadata, bypassing PyPDF2's fragile date parsing."""
    info = reader.metadata or {}

    # For dates, we get the raw values to use our own robust parser
    # instead of calling the PyPDF2 properties that might crash.
    return {
        "title": str(info.title) if info.title else None,
        "author": str(info.author) if info.author else None,
        "creator": str(info.creator) if info.creator else None,
        "producer": str(info.producer) if info.producer else None,
        "creation_date": _parse_pdf_date(info.get("/CreationDate")),
        "mod_date": _parse_pdf_date(info.get("/ModDate")),
    }


def _ocr_page(page_image) -> str:
    """Run Tesseract OCR on a PIL.Image. If Tesseract executable is missing, gracefully fallback."""
    if pytesseract is None or Image is None:
        return ""  # OCR library not available

    try:
        return pytesseract.image_to_string(page_image)
    except (pytesseract.TesseractNotFoundError, RuntimeError, FileNotFoundError):
        # pytesseract raises TesseractNotFoundError when the binary is missing.
        # On some systems it bubbles up as a generic RuntimeError.
        # Instead of crashing the whole request, we log and continue without OCR.
        print("Warning: Tesseract not available – skipping OCR for this page")
        return ""


def _extract_text(page) -> str:
    """Extract text from a pdfplumber page, fallback to OCR if empty."""
    text = page.extract_text() or ""
    if text.strip():
        return text

    # Fallback OCR
    with io.BytesIO() as buffer:
        page.to_image(resolution=300).save(buffer, format="PNG")
        buffer.seek(0)
        if Image is None:
            return ""  # PIL not installed
        image = Image.open(buffer)
        return _ocr_page(image)


def process_pdf(upload_file: UploadFile) -> List[LCDocument]:
    """Process a PDF UploadFile and return split LangChain Documents.

    Returns
    -------
    docs : List[Document]
        Chunked documents ready to embed.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        data = upload_file.file.read()
        tmp.write(data)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    metadata = _extract_metadata(reader)

    # Extract all text with fallback OCR page by page
    pages_text: List[str] = []
    with pdfplumber.open(tmp_path) as pdf:
        for page in pdf.pages:
            pages_text.append(_extract_text(page))

    full_text = "\n".join(pages_text)

    if not full_text.strip():
        raise ValueError("No extractable text found in PDF. Ensure the document contains selectable text or install Tesseract for OCR support.")

    # Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    l_docs = splitter.create_documents([full_text])

    # Attach metadata to each
    for d in l_docs:
        d.metadata.update(metadata)
        d.metadata.update({"source": upload_file.filename})
    return l_docs
