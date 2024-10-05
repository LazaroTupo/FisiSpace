import fitz  # PyMuPDF
import re

# Función para extraer texto del PDF y organizarlo por página
def extract_text_by_page(pdf_path):
    doc = fitz.open(pdf_path)
    pages_text = []

    # Lista de cadenas a eliminar
    filter_phrases = [
        "Asignatura", "Créd.", "Sec.", "Docente", "Tope", "Matri.", "Aula", "Día", "Horas", "Clase",
        "© Copyright", "Proyecto realizado", "Página",
        "REPORTE DE PROGRAMACIÓN DE ASIGNATURAS", "Código de Matrícula", "22200277",
        "Nombres y Apellidos", "LORENZO RAMOS DANIEL DAVID", "Facultad", "20 - INGENIERÍA DE SISTEMAS E INFORMÁTICA",
        "Escuela", "2 - E.P. De Ingeniería De Software", "Especialidad", "0 - Estudios Generales",
        "Plan", "2018 - Plan De Estudios 2018", "Periodo Académico", "2024-2",
        "Fecha Impresión", "Tuesday, 1 October de 2024 19:54:48 PM"
    ]

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text("text")

        cleaned_lines = []
        for line in text.splitlines():
            line = line.strip()  # Limpiar espacios en blanco

            # Eliminar ":" repetidos al inicio de la línea
            while line.startswith(":"):
                line = line[1:].strip()

            # Verificar si alguna de las frases está contenida en la línea
            if any(phrase in line for phrase in filter_phrases):
                continue  # Ignorar esta línea

            if line:  # Agregar solo si la línea no está vacía
                cleaned_lines.append(line)

        # Unir las líneas limpias en un solo texto
        cleaned_text = " ".join(cleaned_lines)
        pages_text.append(cleaned_text)

    return pages_text


# Función para procesar y estructurar la información
def process_course_data(text):
    # Expresión regular para identificar códigos de curso y la palabra "CICLO"
    course_code_pattern = re.compile(r'\b[A-Z]{3}\d{3}\b|\b[0-9]{3}W[0-9]{4}\b')
    ciclo_pattern = re.compile(r'\bCICLO\b')

    lines = []
    current_line = []

    for word in text.split():
        if course_code_pattern.match(word) or ciclo_pattern.match(word):
            if current_line:
                lines.append(" ".join(current_line))
                current_line = []
            current_line.append(word)
        else:
            current_line.append(word)

    if current_line:
        lines.append(" ".join(current_line))

    return lines

# Función para extraer código de docente y nombre del texto
def extraer_datos_docente(texto):
    regex = r"(.*?(?P<codigo_docente>\w+)\s*-\s*(?P<docente>[A-Za-zÁÉÍÓÚáéíóúñÑ\s,]*?)\s*(?=\d+|--|$))|.*?(?P<solo_guion>--)"
    match = re.search(regex, texto)
    if match:
        codigo_docente = match.group('codigo_docente')
        docente = match.group('docente')
        solo_guion = match.group('solo_guion')
        
        if codigo_docente and docente:
            return codigo_docente, docente.strip()
        elif solo_guion:
            return solo_guion, solo_guion
    return "--", "--"  # Valor por defecto si no se encuentra coincidencia

# Función para procesar un texto completo
def procesar_texto(texto, ciclo):
    # Patrón de regex para capturar los componentes del curso
    patron = re.compile(r"""(?P<codigo_curso>\w+)\s+-\s+(?P<nombre_curso>[A-Za-zÁÉÍÓÚáéíóúñÑ,\s]+)\s+(?P<creditos>\d+\.\d+)\s+(?P<seccion>\d+)\s+(?P<datos_entre_seccion_y_tope>.+?)\s+(?P<tope>\d+)\s+(?P<matriculados>\d+)\s+--\s+(?P<dia_teoria>LUNES|MARTES|MIERCOLES|JUEVES|VIERNES|SABADO)\s+(?P<horario_teoria>[\d:]+ - [\d:]+)(?:\s+--\s+(?P<dia_laboratorio>LUNES|MARTES|MIERCOLES|JUEVES|VIERNES|SABADO)\s+(?P<horario_laboratorio>[\d:]+ - [\d:]+))?""")

    # Encontrar todas las coincidencias en el texto
    coincidencias = patron.findall(texto)
    
    # Procesar las coincidencias y armar los resultados
    resultados = []
    for coincidencia in coincidencias:
        codigo_docente, docente = extraer_datos_docente(coincidencia[4])
        curso = {
            'ciclo': ciclo,
            'codigo': coincidencia[0],
            'nombre': coincidencia[1].strip(),
            'creditos': coincidencia[2],
            'seccion': coincidencia[3],
            'codigo_docente': codigo_docente,
            'docente': docente,
            'tope': coincidencia[5],
            'matriculados': coincidencia[6],
            'dia_teoria': coincidencia[7],
            'horario_teoria': coincidencia[8],
            'dia_laboratorio': coincidencia[9],
            'horario_laboratorio': coincidencia[10]
        }
        resultados.append(curso)
    return resultados

# Función principal para ejecutar la extracción, procesamiento y visualización
def main(pdf_path):
    pages_text = extract_text_by_page(pdf_path)
    all_courses = []
    ciclo_actual = 0

    for page in pages_text:
        courses = process_course_data(page)
        
        for line in courses:
            result = procesar_texto(line, str(ciclo_actual))
            if result == []:
                ciclo_actual += 1
            else:
                all_courses.extend(result)

    for course in all_courses:
        print(course)  # Imprimir todos los cursos concatenados
    return all_courses


if __name__ == "__main__":
    pdf_file_path = "D:\\Programacion_Asignaturas.pdf"  # Ruta proporcionada para tu archivo PDF
    main(pdf_file_path)
