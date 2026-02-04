import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
from app.core.config import get_settings

settings = get_settings()

# Set tesseract cmd
pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD

def run_ocr(image_bytes: bytes, lang: str = "eng") -> str:
    """
    Run OCR on an image byte stream.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        # Pre-processing with OpenCV (optional, to improve accuracy)
        # Convert PIL to cv2
        open_cv_image = np.array(image) 
        # Convert RGB to BGR 
        open_cv_image = open_cv_image[:, :, ::-1].copy() 
        
        # Convert to gray
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Convert back to PIL for Tesseract
        image = Image.fromarray(gray)
        
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""

def calculate_confidence(image_bytes: bytes) -> int:
    """
    Calculate mean confidence of OCR result.
    """
    try:
        image = Image.open(io.BytesIO(image_bytes))
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        confidences = [int(conf) for conf in data['conf'] if conf != '-1']
        if not confidences:
            return 0
        return sum(confidences) / len(confidences)
    except:
        return 0
