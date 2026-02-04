from sqlalchemy import Column, Integer, String, DateTime, Float, JSON
from sqlalchemy.sql import func
from app.db.session import Base

class ExtractionLog(Base):
    __tablename__ = "extraction_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    document_type = Column(String)
    status = Column(String) # success, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processing_time_ms = Column(Float)
    client_ip = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    # We don't store the raw document as requested, but we can store the extracted metadata result if needed.
    # The requirement says "Log only metadata (no raw document storage)"
    meta_data = Column(JSON, nullable=True) 
