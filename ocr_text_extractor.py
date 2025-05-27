# ocr_text_extractor.py

from PIL import Image
import pytesseract

def extract_ocr_text(image_path):
    """
    Extracts text from an image using OCR.
    
    Returns:
        text (str): The text found in the image, or an error message if it fails.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
    except Exception as e:
        text = f"Error extracting OCR: {str(e)}"
    
    return text.strip()
