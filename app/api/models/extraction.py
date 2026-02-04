from pydantic import BaseModel
from typing import List, Optional, Union, Literal
from datetime import date

# Shared Models
class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

class Transaction(BaseModel):
    date: Optional[date] = None
    description: str
    amount: float
    type: Literal["debit", "credit", "unknown"]

# Response Models
class InvoiceExtraction(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    seller_name: Optional[str] = None
    buyer_name: Optional[str] = None
    gst_or_tax_id: Optional[str] = None
    line_items: List[LineItem] = []
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    grand_total: Optional[float] = None
    currency: str = "INR"
    confidence_score: float

class ResumeExtraction(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[str] = []

class BankStatementExtraction(BaseModel):
    account_holder: Optional[str] = None
    account_number_last4: Optional[str] = None
    transactions: List[Transaction] = []

class GenericExtraction(BaseModel):
    text: str
    metadata: dict = {}

class ExtractionResponse(BaseModel):
    filename: str
    document_type: str
    processing_time_ms: float
    data: Union[InvoiceExtraction, ResumeExtraction, BankStatementExtraction, GenericExtraction]
