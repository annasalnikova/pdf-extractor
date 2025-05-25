from pdfminer.high_level import extract_text as pdf_extract

def extract_text(filepath):
    return pdf_extract(filepath)