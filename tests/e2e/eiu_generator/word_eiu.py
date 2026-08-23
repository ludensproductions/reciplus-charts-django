import json
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

from utils.eiu_generator_utils import format_image_path

with open("images/elements_data.json", "r", encoding="utf-8") as json_file:
    elements_data = json.load(json_file)

doc = Document()

for url, data in elements_data.items():
    doc.add_heading(f"URL: {url}", level=2)

    style = doc.styles["Normal"]
    font = style.font
    font.name = "Montserrat"
    font.size = Pt(10)

    rPr = style._element.get_or_add_rPr()
    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:eastAsia"), "Montserrat")
    rPr.append(rFonts)

    formatted_url = format_image_path(url)
    print(formatted_url)
    print(url)
    doc.add_picture(formatted_url, width=Inches(6))

    # Añadir encabezado para descripción de elementos
    doc.add_heading("Descripción de elementos", level=1)
    table_elementos = doc.add_table(rows=1, cols=2)
    table_elementos.style = "Table Grid"

    # Añadir encabezado para descripción de campos
    doc.add_heading("Descripción de campos", level=1)
    table = doc.add_table(rows=1, cols=7)
    table.style = "Table Grid"

    # Configurar encabezados para la tabla de elementos
    hdr_cells_elementos = table_elementos.rows[0].cells
    headers_elementos = ["Elemento", "Descripción"]
    for idx, header in enumerate(headers_elementos):
        run = hdr_cells_elementos[idx].paragraphs[0].add_run(header)
        run.bold = True  # Aplicar negrita

    # Configurar encabezados para la tabla de campos
    hdr_cells = table.rows[0].cells
    headers = [
        "Elemento",
        "Tipo",
        "Longitud",
        "Nivel de Acceso (L, E, S)",
        "Descripción del campo",
        "Fórmulas",
        "Precisiones",
    ]
    for idx, header in enumerate(headers):
        run = hdr_cells[idx].paragraphs[0].add_run(header)
        run.bold = True  # Aplicar negrita

    # Añadir los datos a la tabla de campos
    for element in data.get("campos", []):
        row_cells = table.add_row().cells
        row_cells[0].text = element.get("Elemento", "N/A")
        row_cells[1].text = element.get("Tipo", "N/A")
        row_cells[2].text = element.get("Longitud", "N/A")
        row_cells[3].text = element.get("Nivel de acceso", "N/A")
        row_cells[4].text = element.get("Descripción del campo", "N/A")
        row_cells[5].text = element.get("Fórmulas", "N/A")
        row_cells[6].text = element.get("Precisiones", "N/A")

        # Añadir datos a la tabla de elementos
        row_cells_elementos = table_elementos.add_row().cells
        row_cells_elementos[0].text = element.get("Elemento", "N/A")
        row_cells_elementos[1].text = element.get("Descripción del campo", "N/A")

        # Añadir un espacio antes de la siguiente URL
        doc.add_paragraph()

output_dir = Path("eiu_word")
output_dir.mkdir(parents=True, exist_ok=True)

doc.save(output_dir / "generated_eiu.docx")
