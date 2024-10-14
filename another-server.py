from flask import Flask, request, jsonify
import fitz  # PyMuPDF
import pdfplumber
import io
from supabase import create_client, Client
import re

app = Flask(__name__)

SUPABASE_URL = "https://fsbjywdcpewilwhfvnyg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZzYmp5d2RjcGV3aWx3aGZ2bnlnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjgwMDUwNTcsImV4cCI6MjA0MzU4MTA1N30.ZMsqGIEpyFSzh5DrjGwFrb0sVC9BiKYXPQGEP1w1GlU"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if a file was uploaded
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdfFile']

    # Ensure the file is valid
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Process the PDF file
    try:
        extracted_data = extract_pdf_data(file)
        return jsonify({'extracted_data': extracted_data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_pdf_data(file):
    pdf_data = file.read()
    extracted_data = {
        "codigoMatricula": None,
        "nombres": None,
        "periodoAcademico": None,
        "table_data": []
    }

    with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
        # Extract specific fields and table from the first page
        page = pdf.pages[0]
        text = page.extract_text()

        # Extract codigoMatricula, nombres, and periodoAcademico using regex
        extracted_data["codigoMatricula"] = extract_field_from_text(text, r'Código de Matrícula\s*:\s*(\S+)')
        extracted_data["nombres"] = extract_field_from_text(text, r'Nombres y Apellidos\s*:\s*(.+)')
        extracted_data["periodoAcademico"] = extract_field_from_text(text, r'Periodo Académico\s*:\s*(\S+)')
        extracted_data["plan"] = extract_field_from_text(text, r'Plan\s*:\s*(\S+)')
        extracted_data["escuela"] = extract_field_from_text(text, r'Escuela\s*:\s*\d+\s*-\s*(.+)')

        # Extract the table
        table = page.extract_table()
        if table:
            headers = ["Ciclo", "Codigo",  "Asignatura", "Creditos", "Seccion", "DocenteAsignado"]
            for row in table[1:]:  # Skip header
                row[2] = remove_line_breaks(row[2])
                row[-1] = remove_line_breaks(row[-1])
                extracted_data["table_data"].append(dict(zip(headers, row)))

    return extracted_data

def extract_field_from_text(text, regex_pattern):
    import re
    match = re.search(regex_pattern, text)
    return match.group(1) if match else None

def remove_line_breaks(text):
    """Remove line breaks from the given text."""
    return text.replace('\n', ' ').strip()

def extract_field_after_dash(text):
    # Use regex to find the pattern after the dash
    match = re.search(r'-\s*(.+)', text)
    if match:
        return match.group(1).strip()
    return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
