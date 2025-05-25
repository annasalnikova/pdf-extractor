from pdf2image import convert_from_path
import pytesseract
import tempfile
import os
from PyPDF2 import PdfReader
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Anna\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def extract_text_from_scanned_pdf(pdf_path):
    with tempfile.TemporaryDirectory() as path:
        images = convert_from_path(pdf_path, poppler_path=r'C:\Program Files\poppler-24.08.0\Library\bin')

        full_text = ""
        for image in images:
            text = pytesseract.image_to_string(image, lang='eng+fra+deu+rus')
            full_text += text + "\n\n"

    return full_text

def is_scanned_pdf(filepath):
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            if page.extract_text():
                return False
        return True
    except:
        return True  # If something went wrong, consider it a scan