# PDF & Invoice Data Extraction API

A production-ready API for extracting structured data from PDFs, invoices, resumes, and bank statements using OCR and text parsing.

## Features

- **Multi-Format Support**: Invoices, Resumes, Bank Statements, and Generic Documents.
- **Smart Parsing**: Hybrid approach using Text Extraction (PyMuPDF) and OCR (Tesseract).
- **Security**: API Key authentication and input validation.
- **Performance**: Async processing, aimed at < 2s response time for standard documents.
- **Deployment**: Docker-ready.

## Tech Stack

- **Framework**: FastAPI (Python)
- **PDF Core**: PyMuPDF (fitz)
- **OCR Engine**: Tesseract
- **Image Proc**: OpenCV
- **Storage**: PostgreSQL (for logging metadata)

## Setup & Installation

### Local Development (Virtual Env)

1. **Clone & Setup**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

2. **Environment**
   Update `.env` with your configuration.
   Ensure Tesseract OCR is installed on your system.
   - Windows: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki)
   - Update `TESSERACT_CMD` in `.env` to point to your `tesseract.exe`.

3. **Run Server**
   ```bash
   uvicorn app.main:app --reload
   ```

### Docker

```bash
docker build -t pdf-extractor .
docker run -p 8000:8000 pdf-extractor
```

## API Usage

**Base URL**: `http://localhost:8000`

### Authentication
Include the `x-api-key` header in all requests. Default key: `change_this_to_a_super_secret_key`

### Extract Endpoint

**POST** `/api/v1/extract`

**Curl Example**:
```bash
curl -X POST "http://localhost:8000/api/v1/extract" \
  -H "accept: application/json" \
  -H "x-api-key: change_this_to_a_super_secret_key" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/invoice.pdf" \
  -F "document_type=invoice" \
  -F "language=en"
```

**Parameters**:
- `file`: PDF or Image file (max 10MB).
- `document_type`: `invoice` | `resume` | `bank` | `auto`.
- `language`: `auto` | `en` | `hi`.
- `output_format`: `json`.

**JSON Response Example**:
```json
{
  "filename": "invoice.pdf",
  "document_type": "invoice",
  "processing_time_ms": 1250.5,
  "data": {
    "invoice_number": "INV-2024-001",
    "invoice_date": "2024-02-05",
    "seller_name": "Acme Corp",
    "buyer_name": "John Doe",
    "gst_or_tax_id": "22AAAAA0000A1Z5",
    "line_items": [
      {
        "description": "Consulting Services",
        "quantity": 10.0,
        "unit_price": 100.0,
        "total": 1000.0
      }
    ],
    "subtotal": 1000.0,
    "tax": 180.0,
    "grand_total": 1180.0,
    "currency": "INR",
    "confidence_score": 0.95
  }
}
```

## Pricing Plans

Choose the plan that fits your volume.

### Pay-Per-Use
- **Flexible**: ₹5 - ₹20 per document (volume dependent)

### Subscriptions

| Plan | Price | Includes |
| :--- | :--- | :--- |
| **Starter** | ₹999 / mo | 100 documents |
| **Business** | ₹4,999 / mo | 1,000 documents |
| **Enterprise** | Custom | High volume + SLA + Priority Support |

## Limitations

- **Complex Layouts**: Highly unstructured documents may require custom parsing logic.
- **Handwriting**: OCR accuracy on handwritten text varies.
- **PostgreSQL**: Currently configured for metadata logging only.
