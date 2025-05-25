from app.ocr_utils import extract_text_from_scanned_pdf

import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Anna\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def test_ocr():
    pdf_path = "uploads/Screenshot 2025-05-25 125626.pdf"  # Укажи путь к своему тестовому PDF
    text = extract_text_from_scanned_pdf(pdf_path)
    print("Extracted text:\n", text)

if __name__ == "__main__":
    test_ocr()