import fitz
import pytest
from app.services.pdf import extract_text_from_pdf_bytes


def create_sample_pdf_bytes(text: str) -> bytes:
    """Helper to generate in-memory PDF bytes with text."""
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), text)
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes


def test_valid_pdf_extraction():
    """Test extracting text from a valid PDF document."""
    sample_text = "Merit Cum Means Scholarship 2026. Minimum GPA 3.5."
    pdf_bytes = create_sample_pdf_bytes(sample_text)
    
    extracted = extract_text_from_pdf_bytes(pdf_bytes)
    assert "Merit Cum Means Scholarship 2026" in extracted
    assert "Minimum GPA 3.5" in extracted


def test_empty_pdf_handling():
    """Test error handling when PDF contains no text."""
    doc = fitz.open()
    doc.new_page()  # Blank page with no text
    pdf_bytes = doc.tobytes()
    doc.close()

    with pytest.raises(ValueError, match="PDF contains no extractable text"):
        extract_text_from_pdf_bytes(pdf_bytes)


def test_invalid_file_handling():
    """Test error handling when non-PDF file bytes are passed."""
    invalid_bytes = b"This is not a PDF file content."

    with pytest.raises(ValueError, match="Invalid file format"):
        extract_text_from_pdf_bytes(invalid_bytes)
