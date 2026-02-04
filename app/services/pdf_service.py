import fitz  # PyMuPDF
from typing import List, Tuple, Union
import pymupdf

def is_text_based(doc: fitz.Document, threshold: float = 0.05) -> bool:
    """
    Detect if a PDF is text-based or scanned.
    Returns True if text coverage > threshold.
    """
    total_page_area = 0.0
    total_text_area = 0.0

    for page in doc:
        total_page_area += page.rect.get_area()
        text_area = 0.0
        for block in page.get_text("blocks"):
            # block rect: (x0, y0, x1, y1)
            r = fitz.Rect(block[:4])
            text_area += r.get_area()
        total_text_area += text_area

    if total_page_area == 0:
        return False
        
    return (total_text_area / total_page_area) > threshold

def extract_text_from_pdf(content: bytes) -> str:
    """
    Extract text from a text-based PDF using PyMuPDF.
    """
    doc = fitz.open(stream=content, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    return text

def convert_pdf_to_images(content: bytes) -> List[bytes]:
    """
    Convert PDF pages to images (PNG bytes) for OCR.
    """
    doc = fitz.open(stream=content, filetype="pdf")
    images = []
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        images.append(pix.tobytes("png"))
    return images
