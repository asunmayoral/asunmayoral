"""Genera la tabla de cursos de la entrada «Cursos Unidigital-Prodigital» del blog a partir de la hoja de cálculo del proyecto Unidigital-Prodigital.

Uso:
    python scripts/prodigital_desde_excel.py [ruta/al/CURSOS_Y_RECURSOS.xlsx]

Por defecto lee fuentes/CURSOS_Y_RECURSOS.xlsx (carpeta excluida de git).
Solo se publican las columnas pensadas para el público: descripción, objetivos, contenidos,
duración, PDF y ficha en RediUMH, vídeo de YouTube, cuestionario e infografía.
Requiere: openpyxl y pyyaml.
"""
import re
import sys
from collections import OrderedDict

import openpyxl
import yaml

FUENTE = sys.argv[1] if len(sys.argv) > 1 else "fuentes/CURSOS_Y_RECURSOS.xlsx"
ENTRADA = "blog/posts/2026-11-07-cursos-unidigital-prodigital"
SALIDA = f"{ENTRADA}/cursos.yml"
CATALOGO = "recursos/recursos-prodigital.yml"

# Títulos de curso en minúscula de frase (la hoja los tiene en mayúsculas)
TITULOS = {
    "CDC2.1": "Interacción digital",
    "CDC2.2": "Compartir en la red",
    "CDC2.3": "Identidad digital, participación ciudadana y comportamiento en la red",
    "CDC2.4": "Creación colaborativa en la red",
    "CDCE2.1": "Búsqueda y selección de contenidos digitales",
    "CDCE2.2": "Creación y modificación de contenidos digitales",
    "CDCE2.3": "Protección, gestión y compartición de contenidos digitales",
}
MARCOS = {"DIGCOMP": "DigComp", "DIGCOMPEDU": "DigCompEdu"}
# Resumen corto para la tarjeta del catálogo de Recursos (la descripción completa queda en la entrada del blog)
RESUMENES = {
    "Interacción digital": "Cómo comunicarse de forma eficaz y saludable en redes sociales, mensajería y videoconferencia.",
    "Compartir en la red": "Herramientas web para almacenar, organizar y compartir contenidos digitales.",
    "Identidad digital, participación ciudadana y comportamiento en la red": "Identidad, huella y reputación digital, trámites en línea con la Administración y navegación segura.",
    "Creación colaborativa en la red": "Colaboración virtual eficaz: planificación de proyectos, herramientas de cocreación y Wikipedia.",
    "Búsqueda y selección de contenidos digitales": "Estrategias de búsqueda, criterios de selección de contenidos fiables y repositorios para docencia e investigación.",
    "Creación y modificación de contenidos digitales": "Herramientas para crear y modificar contenidos educativos digitales en formatos diversos.",
    "Protección, gestión y compartición de contenidos digitales": "Licencias y Creative Commons, catalogación y pautas para gestionar y compartir contenidos educativos.",
}


def limpio(v):
    if v is None:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    return s or None


def url(v):
    s = limpio(v)
    if not s or not s.startswith("http"):
        return None
    return s.replace("http://dspace.umh.es", "https://dspace.umh.es")


def horas(v):
    h = float(v)
    return f"{h:g}".replace(".", ",") + " h"


def ancla(id_curso):
    return id_curso.lower().replace(".", "-")


wb = openpyxl.load_workbook(FUENTE, data_only=True)

# Cursos en el Campus UMH (acceso identificado) y lista de vídeos de YouTube
campus, lista_youtube = {}, None
for fila in wb["cursos campus"].iter_rows(min_row=2, values_only=True):
    if fila[0] and fila[2]:
        campus[str(fila[0]).strip()] = limpio(fila[2])
    elif fila[1] and "youtube.com/playlist" in str(fila[1]):
        lista_youtube = limpio(fila[1])

ws = wb["cursos y recursos"]
cab = [c.value for c in ws[1]]
filas = [dict(zip(cab, r)) for r in ws.iter_rows(min_row=2, values_only=True) if r[1]]

cursos = OrderedDict()
for f in filas:
    idc = f["id_CURSO"]
    c = cursos.setdefault(idc, {"modulos": []})
    if str(f["ID_MODULO"]).endswith("CURSO"):
        c.update({
            "id": idc,
            "ancla": ancla(idc),
            "marco": MARCOS[f["MARCO DE REFERENCIA"]],
            "title": TITULOS.get(idc, limpio(f["TÍTULO"]).capitalize()),
            "competencia": limpio(f["Competencia"]),
            "area": limpio(f["Área"]).rstrip("."),
            "nivel": limpio(f["NIVEL DEL CURSO "]),
            "horas": horas(f["DURACIÓN (HORAS)"]),
            "description": limpio(f["descripcion_modulo"]),
            "objetivos": limpio(f["OBJETIVOS"]),
            "contenidos": limpio(f["CONTENIDOS"]),
            "evaluacion": limpio(f["SISTEMA DE EVALUACIÓN"]),
            "profesorado": limpio(f["PROFESORADO"]),
            "coleccion": url(f["ENLACES_HANDLE"]),
            "campus": campus.get(idc[1:]),
        })
    else:
        titulo = limpio(f["TÍTULO"])
        num, _, resto = titulo.partition(" ")
        c["modulos"].append({
            "id": f["ID_MODULO"],
            "num": num,
            "titulo": resto.rstrip(". ").strip(),
            "competencia": limpio(f["Competencia"]),
            "horas": horas(f["DURACIÓN (HORAS)"]),
            "descripcion": limpio(f["descripcion_modulo"]),
            "objetivos": limpio(f["OBJETIVOS"]),
            "contenidos": limpio(f["CONTENIDOS"]),
            "pdf": url(f["ENLACES_HANDLE"]),
            "ficha": url(f["HANDLE REPOS UMH"]),
            "video": url(f["YOUTUBE URL"]),
            "cuestionario": url(f["FORMULARIO EVALUACIÓN"]),
            "infografia": url(f["INFOGRAFÍA"]),
        })

salida = []
for orden, (idc, c) in enumerate(cursos.items()):
    c["orden"] = orden
    c["n_modulos"] = len(c["modulos"])
    c["modulos"] = [{k: v for k, v in m.items() if v} for m in c["modulos"]]
    salida.append({k: v for k, v in c.items() if v is not None})

cabecera = ("# Generado por scripts/prodigital_desde_excel.py a partir de la hoja de cálculo del proyecto.\n"
            "# No editar a mano: corrige la hoja y vuelve a ejecutar el script.\n")
with open(SALIDA, "w", encoding="utf-8") as fh:
    fh.write(cabecera)
    yaml.safe_dump(salida, fh, allow_unicode=True, sort_keys=False, width=1000)

# Entradas del catálogo de Recursos: una por curso, agrupadas en la colección Unidigital-Prodigital
catalogo = []
for c in salida:
    temas = ["Competencia digital"] + (["Innovación educativa"] if c["marco"] == "DigCompEdu" else [])
    catalogo.append({
        "title": c["title"],
        "description": f"{c['description']} {c['n_modulos']} módulos, {c['horas']}.",
        **({"resumen": f"{RESUMENES[c['title']]} {c['n_modulos']} módulos, {c['horas']}."} if c["title"] in RESUMENES else {}),
        "path": f"/{ENTRADA}/index.html#{c['ancla']}",
        "date": "2022-06-01",
        "anio": f"{c['marco']} · 2021-22",
        "tipo": "Curso/Taller",
        "temas": temas,
        "origen": "Propio",
        "serie": "Unidigital-Prodigital",
        "autoria": "Con F. J. Montiel, F. J. Amérigo y F. Botella",
    })
with open(CATALOGO, "w", encoding="utf-8") as fh:
    fh.write(cabecera)
    yaml.safe_dump(catalogo, fh, allow_unicode=True, sort_keys=False, width=1000)
if lista_youtube:
    print("Lista de vídeos de YouTube:", lista_youtube)

print(f"{len(salida)} cursos, {sum(c['n_modulos'] for c in salida)} módulos -> {SALIDA}")
