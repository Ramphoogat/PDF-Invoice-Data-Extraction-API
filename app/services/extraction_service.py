from app.services.pdf_service import is_text_based, extract_text_from_pdf, convert_pdf_to_images
from app.services.ocr_service import run_ocr, calculate_confidence
from app.services.parsers import parse_invoice, parse_resume, parse_bank_statement
from app.api.models.extraction import ExtractionResponse, GenericExtraction, InvoiceExtraction, ResumeExtraction, BankStatementExtraction
import time

async def process_document(file_content: bytes, filename: str, doc_type: str, language: str) -> ExtractionResponse:
    start_time = time.time()
    
    # 1. Determine Extraction Method
    # Use PyMuPDF to check if text based
    # A bit tricky with bytes, we need to handle it properly
    # The pdf_service functions take bytes
    
    text = ""
    is_scanned = True
    
    try:
        if filename.lower().endswith(".pdf"):
            import fitz
            doc = fitz.open(stream=file_content, filetype="pdf")
            if is_text_based(doc):
                text = extract_text_from_pdf(file_content)
                is_scanned = False
            else:
                # OCR
                images = convert_pdf_to_images(file_content)
                for img_bytes in images:
                    text += run_ocr(img_bytes, lang="eng" if language == "auto" else language) + "\n"
        else:
            # Assume image if not pdf (though requirement said PDF, validation should handle this)
            # For robustness we can try OCR directly
            text = run_ocr(file_content)
            
    except Exception as e:
        print(f"Error processing: {e}")
        # data = GenericExtraction(text="", metadata={"error": str(e)}) # Fallback
        text = ""

    # 2. Normalize Text (basic)
    text = text.strip()
    
    # 3. Parse based on document type
    data = None
    if doc_type == "invoice":
        data = parse_invoice(text)
    elif doc_type == "resume":
        data = parse_resume(text)
    elif doc_type == "bank":
        data = parse_bank_statement(text)
    else:
        # Auto detection logic would go here
        # For now, default to generic
        data = GenericExtraction(text=text, metadata={"info": "Auto detection not fully implemented"})

    processing_time = (time.time() - start_time) * 1000
    
    return ExtractionResponse(
        filename=filename,
        document_type=doc_type,
        processing_time_ms=processing_time,
        data=data
    )
