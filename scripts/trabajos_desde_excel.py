"""Genera docencia/trabajos.yml (TFG y TFM dirigidos) a partir de la hoja de cálculo.

Uso:
    python3 scripts/trabajos_desde_excel.py [ruta/al/TFG_TFM_dirigidos.xlsx]

Por defecto lee fuentes/TFG_TFM_dirigidos.xlsx (carpeta excluida de git: tiene notas de estudiantes).
Pestañas TFG y TFM, con la fila 1 de cabeceras. Se publican solo:
  TFG: título (columna «Título (web)»), estudiante («Estudiante (web)»), titulación, curso, codirección y enlace al repositorio.
  TFM: título («Título (web)»), estudiante («Estudiante (web)»), curso y especialidad. Nunca notas.
Requiere: openpyxl y pyyaml.
"""
import sys, datetime as dt
import openpyxl, yaml

FUENTE = sys.argv[1] if len(sys.argv) > 1 else "fuentes/TFG_TFM_dirigidos.xlsx"
SALIDA = "docencia/trabajos.yml"

def filas(ws):
    cab = [str(c.value or '').strip() for c in ws[1]]
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not any(r): continue
        yield dict(zip(cab, r))

def fecha(v):
    if isinstance(v, dt.datetime): return v
    return dt.datetime.strptime(str(v).strip(), "%d/%m/%Y")

def curso(f):
    a = f.year if f.month >= 9 else f.year - 1
    return f"{a}/{a + 1}"

def bonito(t):  # por si falta el título revisado
    t = str(t or '').strip()
    return t[:1].upper() + t[1:].lower() if t.isupper() else t

wb = openpyxl.load_workbook(FUENTE, data_only=True)
out = []
for x in filas(wb["TFG"]):
    f = fecha(x["Fecha de evaluación"])
    est = x.get("Estudiante (web)") or x["Estudiante"]
    e = {"clase": "tfg", "bloque": "direccion", "title": x.get("Título (web)") or bonito(x["Título"]),
         "estudiante": est, "titulacion": x.get("Titulación") or "", "curso": curso(f), "desde": f.year, "hasta": f.year, "fecha": f.strftime("%Y-%m-%d")}
    if str(x.get("Dirección") or "").lower().startswith("codirig"): e["codirigido"] = True
    if x.get("Repositorio (RediUMH)"): e["repositorio"] = str(x["Repositorio (RediUMH)"]).strip()
    out.append(e)
for x in filas(wb["TFM"]):
    f = fecha(x["Fecha de evaluación"])
    c = str(x.get("Curso académico") or curso(f))
    out.append({"clase": "tfm", "bloque": "direccion", "title": x.get("Título (web)") or bonito(x["Título"]),
                "especialidad": x["Especialidad"], "estudiante": x.get("Estudiante (web)") or "", "curso": c, "id": "tfm-" + c.replace("/", "-"),
                "desde": f.year, "hasta": f.year, "fecha": f.strftime("%Y-%m-%d")})
out.sort(key=lambda e: e["fecha"], reverse=True)

with open(SALIDA, "w", encoding="utf-8") as fh:
    fh.write("# Generado por scripts/trabajos_desde_excel.py a partir de fuentes/TFG_TFM_dirigidos.xlsx.\n"
             "# No editar a mano: corrige la hoja de cálculo y vuelve a ejecutar el script.\n")
    yaml.safe_dump(out, fh, allow_unicode=True, sort_keys=False, width=1000)
n = {k: sum(e["clase"] == k for e in out) for k in ("tfg", "tfm")}
print(f"{n['tfg']} TFG y {n['tfm']} TFM -> {SALIDA}")
