from docx import Document
from io import BytesIO


def generar_informe(datos):

    # 1. Abrir la plantilla del documento
    try:
        doc = Document('asuntosParticulares/utils/PlantillaResolucion.docx')
    except Exception as e:
        print(f"Error al abrir la plantilla: {e}")
        exit()
        
    
    for para in doc.paragraphs:
        for key, value in datos.items():
            if key in para.text:
                # Usamos .replace() en cada 'run'. Un 'run' es un trozo
                # de texto con el mismo formato.
                for run in para.runs:
                    if key in run.text:
                        run.text = run.text.replace(key, value)
                        run.font.bold = True
                        if key == "{{selloTiempo}}":
                            run.font.name = "Courier New"

    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
