"""
PDF Processing Service using PyMuPDF (fitz).

Extracts text from uploaded PDF documents in-memory.
Validates file header, enforces size limits, and cleans extracted text.
Does not store uploaded files permanently.
"""

import io
import fitz  # PyMuPDF

MAX_FILE_SIZE_BYTES = 15 * 1024 * 1024  # 15 MB limit


def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extract text content page-by-page from in-memory PDF bytes.

    Parameters
    ----------
    pdf_bytes : bytes
        Raw bytes of the uploaded PDF file.

    Returns
    -------
    str
        Extracted and cleaned plain text.

    Raises
    ------
    ValueError
        If file exceeds size limit, is invalid PDF, or contains no extractable text.
    """
    if not pdf_bytes:
        raise ValueError("Uploaded file is empty.")

    if len(pdf_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError(
            f"File size exceeds maximum limit of {MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
        )

    # Validate PDF magic header
    if not pdf_bytes.startswith(b"%PDF"):
        raise ValueError("Invalid file format. Only valid PDF documents are supported.")

    try:
        # Open PDF document from memory stream
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as err:
        raise ValueError("Failed to parse PDF file. The file may be corrupted.") from err

    extracted_pages = []
    try:
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text and text.strip():
                extracted_pages.append(text.strip())
    finally:
        doc.close()

    full_text = "\n\n".join(extracted_pages).strip()

    if not full_text:
        raise ValueError("PDF contains no extractable text. OCR support will be added later.")

    return full_text
