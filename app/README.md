# PDF Table & Text Extractor

A Flask application to extract tables and full text from PDF documents, with options to export extracted data.

---

## Description

- Upload PDFs (scanned or digital)  
- Extract tables in Markdown format, preserving structure and headers  
- Extract full text from PDFs  
- Export extracted tables to CSV or Excel files  
- Export full text to a TXT file  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

2. Create and activate a virtual environment, install dependencies (example):
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Set up environment variables (e.g. API keys) as needed.

Create a `.env` file in the root directory with the following content:
GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the Flask app:
flask run

## Known Issues / Limitations

Scanned PDF OCR limitations:
OCR accuracy depends heavily on the quality of scanned documents. Text extraction may contain errors or missing parts.

Language support:
The model is configured to handle multiple languages (English, French, German, Russian), but some languages may require additional tuning or models for better results.

## Suggestions for Improvement

Use specialized table extraction libraries such as camelot, tabula-py, or pdfplumber to improve parsing of complex tables.

Post-process extracted tables with custom logic to merge split rows or fix broken cell content.

Train or fine-tune ML models specifically for table structure recognition if you want higher accuracy.

Add front-end validation and preview to help users check extracted content before downloading/exporting.

Consider supporting more file formats or adding batch processing capabilities.

## How to Contribute

Feel free to open issues if you encounter bugs or unexpected behavior. Pull requests with fixes or enhancements are always welcome!