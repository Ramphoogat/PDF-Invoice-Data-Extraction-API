from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.api.models.extraction import ExtractionResponse
from app.core.security import get_api_key
from app.services.extraction_service import process_document
from app.db.session import get_db
from app.db.models import ExtractionLog
from typing import Literal

router = APIRouter()

MAX_FILE_SIZE = 10 * 1024 * 1024 # 10MB

@router.post("/extract", response_model=ExtractionResponse)
async def extract_data(
    file: UploadFile = File(...),
    document_type: Literal["invoice", "resume", "bank", "auto"] = Form("auto"),
    language: Literal["auto", "en", "hi"] = Form("auto"),
    output_format: Literal["json"] = Form("json"),
    api_key: str = Depends(get_api_key),
    db: Session = Depends(get_db)
):
    if file.content_type not in ["application/pdf", "image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and Images allowed.")
    
    # Check size (rough check, as we have to read it)
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Limit is 10MB.")
    
    status_str = "failed"
    error_msg = None
    result = None

    try:
        result = await process_document(content, file.filename, document_type, language)
        status_str = "success"
        return result
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        # Log to DB
        try:
            log_entry = ExtractionLog(
                filename=file.filename,
                document_type=document_type,
                status=status_str,
                processing_time_ms=result.processing_time_ms if result else 0.0,
                error_message=error_msg,
                meta_data=result.dict() if result else None
            )
            db.add(log_entry)
            db.commit()
        except Exception as db_e:
            print(f"Failed to log to DB: {db_e}")
