import pdfplumber
import re

# Función para extraer datos del PDF
def extract_students_from_pdf(pdf_path):
    students = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            # Procesar el texto y extraer datos
            lines = text.split("\n")
            for line in lines:
                # Usar una expresión regular para extraer los campos
                match = re.match(r"(\d+)\s+(\d+)\s+([A-Z\s]+)\s+(PRE|POS)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\S+@\S+)\s+(SI|NO)\s+[A-Z]\s+[A-Z]+", line)
                if match:
                    numero, codigo, apellidos_nombres, tipo, dni, creditos, promedio, correo, tercio = match.groups()
                    estudiante = {
                        "codigo": codigo.strip(),
                        "apellidos_nombre": apellidos_nombres.strip(),
                        "dni": dni.strip(),
                        "correo": correo.strip()
                    }
                    students.append(estudiante)
    return students

# Función principal
def main(pdf_path):
    # Extraer estudiantes del PDF
    students = extract_students_from_pdf(pdf_path)
    print(f"Se encontraron {len(students)} estudiantes en el PDF.")
    # print(students)
    # Imprimir los datos de los estudiantes
    # for student in students:
    #     print(f"Código: {student['codigo']}, Apellidos y Nombres: {student['apellidos_nombre']}, DNI: {student['dni']}, Correo: {student['correo']}")
    return students

if __name__ == "__main__":
    pdf_file_path = r"D:\2023 FISI.pdf"  # Reemplaza esto con la ruta de tu archivo PDF
    main(pdf_file_path)