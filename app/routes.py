import os
import uuid
import io
import pandas as pd
from flask import render_template, request, send_file
from app import app
import google.generativeai as genai
from dotenv import load_dotenv
from app.ocr_utils import extract_text_from_scanned_pdf, is_scanned_pdf

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

extracted_table_text = None
extracted_full_text = None

@app.route("/", methods=["GET", "POST"])
def index():
    global extracted_table_text, extracted_full_text

    if request.method == "POST":
        pdf_file = request.files.get("pdf")
        if not pdf_file:
            return render_template("index.html", table_text="File is not selected", full_text="")

        filepath = os.path.join("uploads", pdf_file.filename)
        pdf_file.save(filepath)

        model = genai.GenerativeModel("models/gemini-1.5-flash")

        if is_scanned_pdf(filepath):
            # For scanned PDFs extract only full text
            full_text = extract_text_from_scanned_pdf(filepath)
            prompt_tables_ocr = f"""
Please extract any tables from the following text in Markdown format.
If there are no tables, return an empty string.
Do not split one table sting into different extracted strings.

Text:
{full_text}
"""
            response_tables_ocr = model.generate_content([prompt_tables_ocr])
            table_text = response_tables_ocr.text
        else:
            file_info = genai.upload_file(filepath)

            # Extracting tables (as it was)
            prompt_tables = """
Please extract all tables from the PDF in Markdown format.
Keep headers in multiple languages. Reconstruct broken tables. Do not summarize.
"""
            response_tables = model.generate_content([prompt_tables, file_info])
            table_text = response_tables.text

            # Extracting full text additionally
            prompt_full = """
Please extract the full text from the PDF without summarizing.
"""
            response_full = model.generate_content([prompt_full, file_info])
            full_text = response_full.text

        extracted_table_text = table_text
        extracted_full_text = full_text

        return render_template("index.html", table_text=table_text, full_text=full_text)

    # GET - show the last result, if any
    return render_template("index.html", table_text=extracted_table_text, full_text=extracted_full_text)

@app.route("/export/<fmt>")
def export_table(fmt):
    global extracted_table_text

    if not extracted_table_text:
        return "No data to export"

    try:
        lines = [line for line in extracted_table_text.splitlines() if '|' in line and not line.strip().startswith('|--')]
        table_text = "\n".join(lines)
        df = pd.read_csv(io.StringIO(table_text), sep='|', engine='python', skipinitialspace=True)
        df = df.dropna(axis=1, how='all')  # delete empty columns

        # Path to the exports folder relative to the current file
        export_dir = os.path.join(os.path.dirname(__file__), "exports")

        # If there is no folder, create one
        os.makedirs(export_dir, exist_ok=True)

        filename = f"table_export_{uuid.uuid4()}.{fmt}"
        path = os.path.join(export_dir, filename)

        if fmt == "csv":
            df.to_csv(path, index=False)
        elif fmt == "xlsx":
            df.to_excel(path, index=False)
        else:
            return "Unsupported format"

        return send_file(path, as_attachment=True)

    except Exception as e:
        return f"Export error: {str(e)}"
    
@app.route("/export_text")
def export_text():
    global extracted_full_text

    if not extracted_full_text:
        return "No text to export"

    try:
        export_dir = os.path.join(os.path.dirname(__file__), "exports")
        os.makedirs(export_dir, exist_ok=True)

        filename = f"full_text_export_{uuid.uuid4()}.txt"
        path = os.path.join(export_dir, filename)

        # Writing text to a file
        with open(path, "w", encoding="utf-8") as f:
            f.write(extracted_full_text)

        return send_file(path, as_attachment=True)

    except Exception as e:
        return f"Text export error: {str(e)}"