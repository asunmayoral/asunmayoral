"""Genera el banner «pizarra de cristal asistida por IA» de la portada.

Paneles translúcidos repartidos a distintas profundidades (los del fondo, desenfocados),
con gráficos, fórmulas, modelos, código e informes, y una capa de anotaciones de un
asistente de IA. Todo vectorial; datos simulados con semilla fija.

Uso:
  python scripts/pizarra_ia.py              -> images/banner.svg (tema «pantalla») e images/banner-suave.svg
  python scripts/pizarra_ia.py noche dia    -> images/banner-<tema>.svg, para probar los otros temas
Para cambiar el contenido, edita la lista PANELES (posición, tamaño, giro, profundidad, elemento, título)
y ANOTA (etiquetas del asistente). Requiere numpy.
"""
import sys
import math
import numpy as np

W, H = 1600, 300
SANS = "Atkinson Hyperlegible, Helvetica Neue, Arial, sans-serif"
MONO = "JetBrains Mono, Menlo, Consolas, monospace"
SERIF = "Fraunces, Georgia, serif"

PASTEL = dict(melo="#F8D5C2", menta="#CFE9DA", mante="#FBE8AE", ciru="#EBD3E4", cielo="#D3E7F4")
PROF = dict(melo="#A8472A", menta="#2F6E50", mante="#8A6200", ciru="#7B2D63", cielo="#2C628A")

TEMAS = {
    "noche": dict(fondo=("#17141D", "#2F2A36"), panel="#FFFFFF", panel_op=0.055, borde="#FFFFFF", borde_op=0.22,
                  texto="#FFFBF2", tenue=0.55, col=PASTEL, halo=0.35, red=False),
    "dia": dict(fondo=("#FFFBF2", "#F6EEDF"), panel="#FFFFFF", panel_op=0.62, borde="#2F2A36", borde_op=0.14,
                texto="#2F2A36", tenue=0.55, col=PROF, halo=0.55, red=False, manchas=PASTEL),
    "pantalla": None,   # se completa abajo: «dia» con una pantalla de cristal oscuro en el centro
    "constelacion": dict(fondo=("#1B2330", "#2F2A36"), panel="#FFFFFF", panel_op=0.045, borde="#D3E7F4", borde_op=0.28,
                         texto="#F4F7FB", tenue=0.5, col=PASTEL, halo=0.3, red=True),
}

TEMAS["pantalla"] = dict(TEMAS["dia"], pantalla=True)
del TEMAS["constelacion"]
PANTALLA = [(300, 8), (1302, 8), (1250, 292), (270, 292)]   # paralelogramo inclinado

rng = np.random.default_rng(2026)
ANCLAS = {}   # puntos que señala el asistente, en coordenadas del panel


def f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def txt(x, y, s, size=10, fam=SANS, color="#000", op=1.0, anchor="start", weight=400, italic=False):
    st = ' font-style="italic"' if italic else ""
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (f'<text x="{f(x)}" y="{f(y)}" font-family="{fam}" font-size="{size}" fill="{color}" '
            f'fill-opacity="{op}" text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')


def poly(pts, color, w=1.4, op=1.0, fill="none", fop=0, dash=None):
    d = " ".join(f"{f(x)},{f(y)}" for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return (f'<polyline points="{d}" fill="{fill}" fill-opacity="{fop}" stroke="{color}" stroke-width="{w}" '
            f'stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"{da}/>')


def ejes(w, h, T, m=10):
    c = T["texto"]
    return poly([(m, m), (m, h - m), (w - m, h - m)], c, 0.8, 0.35)


# ---------------------------------------------------------------- elementos (coordenadas locales w x h)

def e_dispersion(w, h, T, C):
    m = 12; n = 34
    x = np.sort(rng.uniform(0, 1, n)); y = 0.15 + 0.65 * x + rng.normal(0, 0.08, n)
    X = m + x * (w - 2 * m); Y = h - m - y * (h - 2 * m)
    s = ejes(w, h, T)
    xs = np.linspace(0, 1, 30); se = 0.04 + 0.06 * (xs - 0.5) ** 2 * 4
    up = [(m + a * (w - 2 * m), h - m - (0.15 + 0.65 * a + b) * (h - 2 * m)) for a, b in zip(xs, se)]
    lo = [(m + a * (w - 2 * m), h - m - (0.15 + 0.65 * a - b) * (h - 2 * m)) for a, b in zip(xs[::-1], se[::-1])]
    s += poly(up + lo, C["cielo"], 0, 0, C["cielo"], 0.18)
    s += "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="2.1" fill="{C["melo"]}" fill-opacity="0.9"/>' for a, b in zip(X, Y))
    s += poly([(m, h - m - 0.15 * (h - 2 * m)), (w - m, h - m - 0.8 * (h - 2 * m))], C["cielo"], 1.6)
    return s


def e_histograma(w, h, T, C):
    m = 10; z = rng.normal(0, 1, 400); cnt, bordes = np.histogram(z, bins=13, range=(-3.2, 3.2))
    bw = (w - 2 * m) / len(cnt); top = cnt.max()
    s = ejes(w, h, T)
    for i, c in enumerate(cnt):
        hh = c / top * (h - 2 * m - 6)
        s += (f'<rect x="{f(m + i * bw + 1)}" y="{f(h - m - hh)}" width="{f(bw - 2)}" height="{f(hh)}" '
              f'fill="{C["menta"]}" fill-opacity="0.45" stroke="{C["menta"]}" stroke-width="0.8"/>')
    xs = np.linspace(-3.2, 3.2, 60); d = np.exp(-xs ** 2 / 2)
    s += poly([(m + (a + 3.2) / 6.4 * (w - 2 * m), h - m - b * (h - 2 * m - 6)) for a, b in zip(xs, d)], C["melo"], 1.6)
    return s


def e_cajas(w, h, T, C):
    m = 10; s = ejes(w, h, T); cols = [C["melo"], C["menta"], C["ciru"], C["cielo"]]
    for i, cc in enumerate(cols):
        cx = m + (i + 0.5) * (w - 2 * m) / 4; q = np.quantile(rng.normal(0.45 + 0.08 * math.sin(i * 1.7), 0.11, 80), [0.03, 0.25, 0.5, 0.75, 0.97])
        Y = [h - m - v * (h - 2 * m) for v in (q[0] - .08, q[1], q[2], q[3], q[4] + .08)]
        s += poly([(cx, Y[0]), (cx, Y[1])], cc, 1) + poly([(cx, Y[3]), (cx, Y[4])], cc, 1)
        s += (f'<rect x="{f(cx - 8)}" y="{f(Y[3])}" width="16" height="{f(Y[1] - Y[3])}" fill="{cc}" '
              f'fill-opacity="0.3" stroke="{cc}" stroke-width="1.1" rx="1.5"/>')
        s += poly([(cx - 8, Y[2]), (cx + 8, Y[2])], cc, 1.8)
        if i == 2:
            ANCLAS["atipico"] = (cx, Y[4] - 9)
            s += f'<circle cx="{f(cx)}" cy="{f(Y[4] - 9)}" r="2" fill="none" stroke="{cc}" stroke-width="1"/>'
    return s


def e_roc(w, h, T, C):
    m = 12; s = ejes(w, h, T)
    s += poly([(m, h - m), (w - m, m)], T["texto"], 0.8, 0.3, dash="3 3")
    t = np.linspace(0, 1, 40); fpr = t; tpr = 1 - (1 - t) ** 3.2
    s += poly([(m + a * (w - 2 * m), h - m - b * (h - 2 * m)) for a, b in zip(fpr, tpr)], C["ciru"], 1.8)
    k = int(np.argmax(tpr - fpr)); ANCLAS["roc"] = (m + fpr[k] * (w - 2 * m), h - m - tpr[k] * (h - 2 * m))
    s += f'<circle cx="{f(ANCLAS["roc"][0])}" cy="{f(ANCLAS["roc"][1])}" r="2.4" fill="{C["ciru"]}"/>'
    s += txt(w - m - 2, h - m - 6, "AUC = 0,91", 9, MONO, T["texto"], 0.8, "end")
    return s


def e_confusion(w, h, T, C):
    m = 14; cw = (w - 2 * m) / 2; ch = (h - 2 * m - 10) / 2; vals = [[86, 9], [7, 98]]
    s = txt(w / 2, 11, "Predicción", 8, SANS, T["texto"], T["tenue"], "middle")
    for i in range(2):
        for j in range(2):
            v = vals[i][j]; op = 0.15 + 0.55 * v / 100; cc = C["menta"] if i == j else C["melo"]
            s += (f'<rect x="{f(m + j * cw)}" y="{f(m + 4 + i * ch)}" width="{f(cw - 3)}" height="{f(ch - 3)}" rx="2" '
                  f'fill="{cc}" fill-opacity="{f(op)}"/>')
            s += txt(m + j * cw + cw / 2 - 1.5, m + 4 + i * ch + ch / 2 + 4, str(v), 11, MONO, T["texto"], 0.9, "middle")
    return s


def e_red(w, h, T, C):
    capas = [3, 5, 5, 2]; m = 12
    pos = [[(m + k * (w - 2 * m) / (len(capas) - 1), m + (i + 0.5) * (h - 2 * m) / n) for i in range(n)]
           for k, n in enumerate(capas)]
    s = ""
    for a, b in zip(pos, pos[1:]):
        for p in a:
            for q in b:
                s += poly([p, q], C["cielo"], 0.6, 0.35)
    cols = [C["melo"], C["cielo"], C["cielo"], C["menta"]]
    for k, capa in enumerate(pos):
        for x, y in capa:
            s += f'<circle cx="{f(x)}" cy="{f(y)}" r="3.6" fill="{cols[k]}" fill-opacity="0.85"/>'
    return s


def e_arbol(w, h, T, C):
    nodos = {0: (w / 2, 14, "x₁ < 2,5"), 1: (w * 0.27, h * 0.5, "x₂ < 0,8"), 2: (w * 0.73, h * 0.5, "sí"),
             3: (w * 0.13, h - 14, "A"), 4: (w * 0.41, h - 14, "B")}
    s = ""
    for a, b in [(0, 1), (0, 2), (1, 3), (1, 4)]:
        (x1, y1, _), (x2, y2, _) = nodos[a], nodos[b]
        s += poly([(x1, y1 + 7.5), (x2, y2 - 8)], T["texto"], 0.9, 0.4)
    for k, (x, y, lab) in nodos.items():
        hoja = k in (2, 3, 4); cc = C["menta"] if hoja else C["mante"]
        ww = 22 if hoja else 52
        s += (f'<rect x="{f(x - ww / 2)}" y="{f(y - 8)}" width="{ww}" height="15" rx="7.5" fill="{cc}" '
              f'fill-opacity="0.28" stroke="{cc}" stroke-width="0.9"/>')
        s += txt(x, y + 3.3, lab, 8, MONO, T["texto"], 0.9, "middle")
    return s


def e_serie(w, h, T, C):
    m = 10; n = 60; t = np.arange(n)
    y = 0.5 + 0.18 * np.sin(t / 5) + 0.004 * t + rng.normal(0, 0.035, n)
    corte = 44; X = m + t / (n - 1) * (w - 2 * m); Y = h - m - y * (h - 2 * m) * 0.85
    s = ejes(w, h, T)
    k = np.arange(corte, n); sd = 0.02 + 0.006 * (k - corte)
    up = [(X[i], Y[i] - sd[j] * (h - 2 * m) * 3) for j, i in enumerate(k)]
    lo = [(X[i], Y[i] + sd[j] * (h - 2 * m) * 3) for j, i in list(enumerate(k))[::-1]]
    s += poly(up + lo, C["mante"], 0, 0, C["mante"], 0.22)
    s += poly(list(zip(X[:corte + 1], Y[:corte + 1])), C["cielo"], 1.4)
    s += poly(list(zip(X[corte:], Y[corte:])), C["mante"], 1.4, dash="3 2")
    s += poly([(X[corte], m), (X[corte], h - m)], T["texto"], 0.6, 0.3, dash="2 3")
    return s


def e_calor(w, h, T, C):
    k = 6; m = 8; cw = (w - 2 * m) / k; ch = (h - 2 * m) / k
    A = rng.normal(0, 1, (40, k)); A[:, 1] += A[:, 0] * 1.2; A[:, 4] -= A[:, 3]; R = np.corrcoef(A.T)
    s = ""
    for i in range(k):
        for j in range(k):
            r = R[i, j]; cc = C["cielo"] if r > 0 else C["melo"]
            s += (f'<rect x="{f(m + j * cw)}" y="{f(m + i * ch)}" width="{f(cw - 1.5)}" height="{f(ch - 1.5)}" '
                  f'rx="1.5" fill="{cc}" fill-opacity="{f(0.08 + 0.75 * abs(r))}"/>')
    return s


def e_kmedias(w, h, T, C):
    m = 10; cent = [(0.25, 0.7), (0.7, 0.75), (0.55, 0.25)]; cols = [C["melo"], C["menta"], C["ciru"]]
    s = ""
    for (cx, cy), cc in zip(cent, cols):
        p = rng.normal(0, 0.08, (14, 2)) + [cx, cy]
        X = m + p[:, 0] * (w - 2 * m); Y = h - m - p[:, 1] * (h - 2 * m)
        s += (f'<ellipse cx="{f(m + cx * (w - 2 * m))}" cy="{f(h - m - cy * (h - 2 * m))}" rx="{f((w - 2 * m) * 0.17)}" '
              f'ry="{f((h - 2 * m) * 0.21)}" fill="{cc}" fill-opacity="0.12" stroke="{cc}" stroke-width="0.8" stroke-dasharray="3 3"/>')
        s += "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="1.9" fill="{cc}"/>' for a, b in zip(X, Y))
        x0, y0 = m + cx * (w - 2 * m), h - m - cy * (h - 2 * m)
        s += poly([(x0 - 4, y0 - 4), (x0 + 4, y0 + 4)], T["texto"], 1.3, 0.8) + poly([(x0 - 4, y0 + 4), (x0 + 4, y0 - 4)], T["texto"], 1.3, 0.8)
    return s


def e_qq(w, h, T, C):
    m = 12; n = 30; q = np.sort(rng.standard_t(6, n)).clip(-2.8, 2.8); teo = np.sort(rng.normal(0, 1, 2000))[np.linspace(30, 1970, n).astype(int)]
    sc = lambda v: (v + 3) / 6
    s = ejes(w, h, T) + poly([(m, h - m), (w - m, m)], C["melo"], 1.1, 0.8)
    s += "".join(f'<circle cx="{f(m + sc(a) * (w - 2 * m))}" cy="{f(h - m - sc(b) * (h - 2 * m))}" r="1.9" fill="none" '
                 f'stroke="{C["cielo"]}" stroke-width="1"/>' for a, b in zip(teo, q))
    return s


def e_campana(w, h, T, C):
    m = 10; xs = np.linspace(-3.5, 3.5, 80); d = np.exp(-xs ** 2 / 2)
    P = [(m + (a + 3.5) / 7 * (w - 2 * m), h - m - b * (h - 2 * m - 8)) for a, b in zip(xs, d)]
    cola = [p for a, p in zip(xs, P) if a >= 1.85]
    s = poly(cola + [(cola[-1][0], h - m), (cola[0][0], h - m)], C["melo"], 0, 0, C["melo"], 0.45)
    s += poly(P, C["mante"], 1.6) + poly([(m, h - m), (w - m, h - m)], T["texto"], 0.8, 0.35)
    s += txt(w - m, 14, "p = 0,032", 9, MONO, T["texto"], 0.85, "end")
    return s


def e_control(w, h, T, C):
    m = 10; n = 26; y = rng.normal(0, 1, n); y[19] = 3.4
    X = m + np.arange(n) / (n - 1) * (w - 2 * m - 22); sc = lambda v: h / 2 - v / 4.2 * (h / 2 - m)
    s = ""
    for v, lab in [(3, "LCS"), (0, "LC"), (-3, "LCI")]:
        s += poly([(m, sc(v)), (w - m - 22, sc(v))], C["melo"] if v else T["texto"], 0.8, 0.6 if v else 0.35, dash="4 3" if v else None)
        s += txt(w - m, sc(v) + 3, lab, 7, MONO, T["texto"], T["tenue"], "end")
    s += poly(list(zip(X, sc(y))), C["cielo"], 1.2)
    ANCLAS["control"] = (X[19], sc(y[19]))
    s += "".join(f'<circle cx="{f(a)}" cy="{f(b)}" r="{2.8 if i == 19 else 1.6}" fill="{C["melo"] if i == 19 else C["cielo"]}"/>'
                 for i, (a, b) in enumerate(zip(X, sc(y))))
    return s


def e_barras(w, h, T, C):
    m = 10; v = [0.42, 0.68, 0.55, 0.9, 0.74]; cols = [C["cielo"], C["menta"], C["mante"], C["melo"], C["ciru"]]
    bw = (w - 2 * m) / len(v); s = ejes(w, h, T)
    for i, (a, cc) in enumerate(zip(v, cols)):
        hh = a * (h - 2 * m - 4)
        s += f'<rect x="{f(m + i * bw + 3)}" y="{f(h - m - hh)}" width="{f(bw - 6)}" height="{f(hh)}" rx="2" fill="{cc}" fill-opacity="0.55"/>'
    return s


def e_pca(w, h, T, C):
    cx, cy = w / 2, h / 2; s = ""
    p = rng.multivariate_normal([0, 0], [[1, 0.6], [0.6, 0.8]], 40) * min(w, h) * 0.17
    s += "".join(f'<circle cx="{f(cx + a)}" cy="{f(cy - b)}" r="1.5" fill="{T["texto"]}" fill-opacity="0.45"/>' for a, b in p)
    for ang, l, lab in [(20, 0.42, "x₁"), (75, 0.36, "x₂"), (150, 0.3, "x₃"), (-30, 0.33, "x₄")]:
        ex = cx + math.cos(math.radians(ang)) * w * l; ey = cy - math.sin(math.radians(ang)) * h * l
        s += poly([(cx, cy), (ex, ey)], C["ciru"], 1.3)
        s += f'<circle cx="{f(ex)}" cy="{f(ey)}" r="2" fill="{C["ciru"]}"/>' + txt(ex + 3, ey - 2, lab, 8, MONO, T["texto"], 0.75)
    return s


def e_dag(w, h, T, C):
    N = {"X": (16, h / 2), "M": (w / 2, 16), "Z": (w / 2, h - 14), "Y": (w - 16, h / 2)}
    s = '<defs><marker id="fl" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="5" markerHeight="5" orient="auto">' \
        f'<path d="M0,0 L6,3 L0,6 z" fill="{T["texto"]}" fill-opacity="0.6"/></marker></defs>'
    for a, b in [("X", "M"), ("M", "Y"), ("Z", "X"), ("Z", "Y"), ("X", "Y")]:
        (x1, y1), (x2, y2) = N[a], N[b]; d = math.hypot(x2 - x1, y2 - y1); ux, uy = (x2 - x1) / d, (y2 - y1) / d
        s += (f'<line x1="{f(x1 + ux * 9)}" y1="{f(y1 + uy * 9)}" x2="{f(x2 - ux * 10)}" y2="{f(y2 - uy * 10)}" '
              f'stroke="{T["texto"]}" stroke-opacity="0.5" stroke-width="0.9" marker-end="url(#fl)"/>')
    for k, (x, y) in N.items():
        cc = C["mante"] if k in "XY" else C["cielo"]
        s += f'<circle cx="{f(x)}" cy="{f(y)}" r="8" fill="{cc}" fill-opacity="0.3" stroke="{cc}"/>'
        s += txt(x, y + 3.5, k, 9, SERIF, T["texto"], 0.9, "middle", italic=True)
    return s


def e_tabla(w, h, T, C):
    cab = ["id", "edad", "grupo", "ŷ"]; filas = [["01", "34", "A", "0,82"], ["02", "51", "B", "0,17"],
                                              ["03", "27", "A", "0,64"], ["04", "45", "C", "0,39"]]
    m = 8; cw = (w - 2 * m) / 4; rh = (h - 2 * m) / 5
    s = f'<rect x="{m}" y="{m}" width="{f(w - 2 * m)}" height="{f(rh)}" rx="2" fill="{C["mante"]}" fill-opacity="0.3"/>'
    for j, c in enumerate(cab):
        s += txt(m + j * cw + 5, m + rh * 0.7, c, 8.5, MONO, T["texto"], 0.95, weight=700)
    for i, fila in enumerate(filas, 1):
        for j, c in enumerate(fila):
            s += txt(m + j * cw + 5, m + i * rh + rh * 0.7, c, 8.5, MONO, T["texto"], 0.75)
        s += poly([(m, m + (i + 1) * rh), (w - m, m + (i + 1) * rh)], T["texto"], 0.5, 0.15)
    return s


def e_informe(w, h, T, C):
    s = (f'<rect x="10" y="8" width="{f(w - 20)}" height="{f(h - 16)}" rx="3" fill="{T["texto"]}" fill-opacity="0.08" '
         f'stroke="{T["texto"]}" stroke-opacity="0.35" stroke-width="0.8"/>')
    s += txt(17, 22, "Informe", 9, SERIF, T["texto"], 0.9, weight=600)
    for i, l in enumerate([0.8, 0.65, 0.75]):
        s += poly([(17, 31 + i * 6), (17 + (w - 34) * l, 31 + i * 6)], T["texto"], 1.6, 0.25)
    bx = 17; by = h - 14
    for i, a in enumerate([10, 18, 14, 24, 20]):
        s += f'<rect x="{f(bx + i * 8)}" y="{f(by - a)}" width="5" height="{a}" fill="{C["menta"]}" fill-opacity="0.65"/>'
    s += poly([(w - 50, by - 6), (w - 40, by - 16), (w - 30, by - 11), (w - 18, by - 24)], C["melo"], 1.4)
    return s


def e_formula(s_, size=13):
    def g(w, h, T, C):
        return txt(w / 2, h / 2 + size * 0.35, s_, size, SERIF, T["texto"], 0.92, "middle", italic=False)
    return g


def e_codigo(lineas, etiqueta):
    def g(w, h, T, C):
        s = txt(10, 15, etiqueta, 8, MONO, C["mante"], 0.9, weight=700)
        for i, (l, c) in enumerate(lineas):
            s += txt(10, 30 + i * 13, l, 9, MONO, C[c] if c else T["texto"], 0.88)
        return s
    return g


def e_ia(w, h, T, C):
    # burbuja de asistente: pregunta + respuesta
    s = estrella(14, 14, 6, C["cielo"])
    s += txt(25, 18, "Asistente", 8.5, SANS, T["texto"], T["tenue"], weight=700)
    s += (f'<rect x="10" y="26" width="{f(w - 34)}" height="19" rx="9.5" fill="{T["texto"]}" fill-opacity="0.09"/>')
    s += txt(19, 39, "¿Qué modelo ajusto?", 9, SANS, T["texto"], 0.8)
    s += (f'<rect x="24" y="51" width="{f(w - 34)}" height="31" rx="9.5" fill="{C["cielo"]}" fill-opacity="0.22" '
          f'stroke="{C["cielo"]}" stroke-opacity="0.6" stroke-width="0.8"/>')
    s += txt(33, 64, "GLM binomial, enlace logit;", 9, SANS, T["texto"], 0.9)
    s += txt(33, 76, "compara el AIC con un GAM.", 9, SANS, T["texto"], 0.9)
    return s


def e_metricas(w, h, T, C):
    s = ""
    for i, (k, v, cc) in enumerate([("R²", "0,87", "menta"), ("RMSE", "1,24", "cielo"), ("F1", "0,90", "ciru")]):
        x = 10 + i * (w - 20) / 3
        s += txt(x, 20, k, 8, MONO, T["texto"], T["tenue"])
        s += txt(x, 38, v, 15, SERIF, C[cc], 0.95, weight=600)
    return s


def estrella(x, y, r, color, op=1.0):
    p = []
    for i in range(8):
        a = math.pi / 4 * i; rr = r if i % 2 == 0 else r * 0.32
        p.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    d = "M" + " L".join(f"{f(a)},{f(b)}" for a, b in p) + " Z"
    return f'<path d="{d}" fill="{color}" fill-opacity="{op}"/>'


# ---------------------------------------------------------------- composición
# (x, y, w, h, giro, profundidad 0=cerca 1=lejos, elemento, etiqueta)
PANELES = [
    (22, 22, 132, 96, 2, 0.1, e_dispersion, "Regresión"),
    (150, 140, 186, 44, -2, 0.2, e_formula("P(θ | y) ∝ P(y | θ) · P(θ)", 13), None),
    (176, 196, 120, 92, 3, 0.0, e_cajas, "Diagnóstico"),
    (184, 12, 112, 84, -4, 0.75, e_calor, "Correlaciones"),
    (306, 64, 156, 112, -1.5, 0.05, e_red, "Red neuronal"),
    (318, 196, 196, 78, 1.5, 0.15, e_codigo([("modelo <- glm(y ~ x1 + x2,", None),
                                            ("      family = binomial)", "cielo"),
                                            ("summary(modelo)", "menta")], "R"), None),
    (470, 8, 120, 90, 4, 0.55, e_histograma, "Distribución"),
    (508, 108, 166, 90, -2.5, 0.0, e_ia, None),
    (530, 214, 118, 70, 2, 0.6, e_tabla, None),
    (612, 18, 168, 40, 1, 0.3, e_formula("log( p ⁄ (1 − p) ) = Xβ", 13), None),
    (688, 74, 118, 104, 3, 0.05, e_roc, "Curva ROC"),
    (664, 200, 146, 84, -3, 0.35, e_control, "Control estadístico"),
    (812, 10, 130, 92, -2, 0.7, e_pca, "Componentes"),
    (826, 118, 150, 84, 1.5, 0.0, e_arbol, "Árbol de decisión"),
    (836, 222, 160, 52, -1, 0.15, e_metricas, None),
    (958, 20, 120, 96, 3, 0.15, e_kmedias, "k-medias"),
    (998, 130, 112, 92, -2, 0.55, e_confusion, None),
    (1010, 232, 176, 40, 2, 0.4, e_formula("L(θ) = ∏ f(yᵢ | θ)", 13), None),
    (1094, 36, 196, 74, -1.5, 0.05, e_codigo([("from sklearn.ensemble import", None),
                                             ("  RandomForestClassifier", "menta"),
                                             ("rf.fit(X_train, y_train)", "melo")], "Python"), None),
    (1124, 124, 116, 94, 2.5, 0.0, e_qq, "Q-Q normal"),
    (1268, 198, 124, 88, -2, 0.2, e_campana, "Contraste"),
    (1294, 98, 106, 88, 3, 0.45, e_dag, "Causalidad"),
    (1330, 14, 120, 84, 2, 0.1, e_informe, None),
    (1390, 112, 160, 40, -2, 0.25, e_formula("Cp = (LSE − LIE) ⁄ 6σ", 12.5), None),
    (1396, 168, 150, 112, 1.5, 0.05, e_histograma, "Capacidad"),
]

# anotaciones del asistente: (panel índice, x local, y local, texto, desplazamiento etiqueta)
ANOTA = [(2, "atipico", "atípico", (-92, 44)), (11, "control", "fuera de control", (-124, 1)),
         (10, "roc", "umbral óptimo", (30, 44))]


def panel(p, T, idx, suf=""):
    x, y, w, h, giro, prof, elem, etiq = p
    global rng
    rng = np.random.default_rng(int(x * 7 + y * 13) % 100000)   # datos estables aunque se quiten paneles
    C = T["col"]
    blur = f' filter="url(#d{int(prof * 10)})"' if prof >= 0.5 else ""
    op = 1 - 0.55 * prof
    sc = 1 - 0.12 * prof
    s = (f'<g transform="translate({f(x + w / 2)} {f(y + h / 2)}) rotate({giro}) scale({f(sc)}) '
         f'translate({f(-w / 2)} {f(-h / 2)})" opacity="{f(op)}"{blur}>')
    s += (f'<rect width="{w}" height="{h}" rx="9" fill="url(#vidrio{suf})" stroke="url(#bisel{suf})" stroke-width="1"/>')
    s += f'<rect x="1" y="1" width="{w - 2}" height="{f(h * 0.42)}" rx="8" fill="url(#brillo{suf})"/>'
    s += elem(w, h, T, C)
    if etiq and y >= 14:   # pestaña de título sobre el panel
        s += txt(6, -4, etiq.upper(), 6.8, SANS, T["texto"], T["tenue"] + 0.1, "start", 700)
    s += "</g>"
    return s


def anotacion(T, tema_de=lambda i: None):
    s = ""
    for i, clave, t, (dx, dy) in ANOTA:
        T = tema_de(i) or T; C = T["col"]
        x, y, w, h, giro, prof, *_ = PANELES[i]
        lx, ly = ANCLAS[clave]; k = 1 - 0.12 * prof
        a = math.radians(giro); cx, cy = x + w / 2, y + h / 2
        lx, ly = w / 2 + (lx - w / 2) * k, h / 2 + (ly - h / 2) * k
        px = cx + (lx - w / 2) * math.cos(a) - (ly - h / 2) * math.sin(a)
        py = cy + (lx - w / 2) * math.sin(a) + (ly - h / 2) * math.cos(a)
        tx, ty = px + dx, py + dy
        ancho = 20 + len(t) * 5.6
        ex = tx - 4 + ancho if dx < 0 else tx - 4      # extremo de la etiqueta más cercano al punto
        s += f'<circle cx="{f(px)}" cy="{f(py)}" r="7" fill="none" stroke="{C["cielo"]}" stroke-width="1.2" stroke-dasharray="2 2"/>'
        d = math.hypot(ex - px, ty - py); s += poly([(px + (ex - px) * 8 / d, py + (ty - 1.5 - py) * 8 / d), (ex, ty - 1.5)], C["cielo"], 0.9, 0.8)
        s += (f'<rect x="{f(tx - 4)}" y="{f(ty - 9)}" width="{f(ancho)}" height="15" rx="7.5" fill="{C["cielo"]}" '
              f'fill-opacity="0.22" stroke="{C["cielo"]}" stroke-opacity="0.7" stroke-width="0.7"/>')
        s += estrella(tx + 4, ty - 1.5, 4, C["cielo"])
        s += txt(tx + 11, ty + 2, t, 8, SANS, T["texto"], 0.92, weight=700)
    return s


def red_constelacion(T):
    # hilos que unen paneles cercanos: la «red» que piensa
    C = T["col"]; s = ""
    cs = [(x + w / 2, y + h / 2) for x, y, w, h, *_ in PANELES]
    for i, a in enumerate(cs):
        d = sorted(((math.dist(a, b), j) for j, b in enumerate(cs) if j != i))[:2]
        for _, j in d:
            if j > i:
                b = cs[j]; mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 - 18
                s += (f'<path d="M{f(a[0])},{f(a[1])} Q{f(mx)},{f(my)} {f(b[0])},{f(b[1])}" fill="none" '
                      f'stroke="{C["cielo"]}" stroke-opacity="0.14" stroke-width="0.7"/>')
    return s


def fondo(T, nombre):
    a, b = T["fondo"]; C = T["col"]
    s = f'<rect width="{W}" height="{H}" fill="url(#fondo)"/>'
    manchas = T.get("manchas", C)
    for (cx, cy, r, k) in [(160, 80, 170, "melo"), (520, 230, 190, "menta"), (860, 60, 200, "cielo"),
                           (1180, 240, 180, "ciru"), (1480, 90, 170, "mante")]:
        s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{manchas[k]}" fill-opacity="{T["halo"]}" filter="url(#halo)"/>'
    # retícula tenue de pantalla
    pat = T["texto"]
    s += (f'<pattern id="reticula" width="24" height="24" patternUnits="userSpaceOnUse">'
          f'<path d="M24 0 L0 0 0 24" fill="none" stroke="{pat}" stroke-opacity="0.05" stroke-width="0.6"/></pattern>'
          f'<rect width="{W}" height="{H}" fill="url(#reticula)"/>')
    # reflejo diagonal del cristal
    s += f'<polygon points="380,0 560,0 300,{H} 120,{H}" fill="url(#reflejo)"/>'
    s += f'<polygon points="1020,0 1080,0 820,{H} 760,{H}" fill="url(#reflejo)"/>'
    return s


def defs_panel(T, suf=""):
    P = T["panel"]; Bc = T["borde"]
    return f"""<linearGradient id="vidrio{suf}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{P}" stop-opacity="{f(T['panel_op'] * 1.6)}"/><stop offset="1" stop-color="{P}" stop-opacity="{f(T['panel_op'] * 0.7)}"/></linearGradient>
<linearGradient id="bisel{suf}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{Bc}" stop-opacity="{f(T['borde_op'] * 1.8)}"/><stop offset="0.5" stop-color="{Bc}" stop-opacity="{f(T['borde_op'] * 0.4)}"/><stop offset="1" stop-color="{Bc}" stop-opacity="{f(T['borde_op'])}"/></linearGradient>
<linearGradient id="brillo{suf}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="{0.07 if T['texto'] != '#2F2A36' else 0.35}"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>"""


def defs(T):
    a, b = T["fondo"]; C = T["col"]
    extra = defs_panel(TEMAS["noche"], "o") if T.get("pantalla") else ""
    return f"""<defs>
<linearGradient id="fondo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>
{defs_panel(T)}{extra}
<linearGradient id="pantalla" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17141D" stop-opacity="0.93"/><stop offset="1" stop-color="#2F2A36" stop-opacity="0.88"/></linearGradient>
<linearGradient id="reflejo_o" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="0.05"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<filter id="sombra" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<clipPath id="recorte"><polygon points="{' '.join(f'{x},{y}' for x, y in PANTALLA)}"/></clipPath>
<linearGradient id="reflejo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity="{0.035 if T['texto'] != '#2F2A36' else 0.3}"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<filter id="halo" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>
<filter id="d5"><feGaussianBlur stdDeviation="0.9"/></filter>
<filter id="d6"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="d7"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="d8"><feGaussianBlur stdDeviation="1.7"/></filter>
</defs>"""


def dentro_pantalla(p):
    x, y, w, h = p[:4]; cx, cy = x + w / 2, y + h / 2
    (x0, y0), (x1, _), (x2, y2), (x3, _) = PANTALLA
    t = (cy - y0) / (y2 - y0); izq = x0 + (x3 - x0) * t; der = x1 + (x2 - x1) * t
    return izq < cx < der


def banner(nombre, suave=False):
    T = TEMAS[nombre]
    if suave:
        T = dict(T, pantalla=False)
    global rng
    rng = np.random.default_rng(2026)
    orden = sorted(range(len(PANELES)), key=lambda i: -PANELES[i][5])   # del fondo al frente
    cuerpo = fondo(T, nombre)
    if T["red"]:
        cuerpo += red_constelacion(T)
    if T.get("pantalla"):
        pts = " ".join(f"{x},{y}" for x, y in PANTALLA)
        dentro = lambda i: dentro_pantalla(PANELES[i])
        To = TEMAS["noche"]
        cuerpo += f'<polygon points="{pts}" transform="translate(0 8)" fill="#2F2A36" fill-opacity="0.35" filter="url(#sombra)"/>'
        cuerpo += f'<polygon points="{pts}" fill="url(#pantalla)"/>'
        cuerpo += (f'<g clip-path="url(#recorte)"><rect width="{W}" height="{H}" fill="url(#reticula)" opacity="0.6"/>'
                   f'<polygon points="560,0 700,0 520,{H} 380,{H}" fill="url(#reflejo_o)"/>'
                   f'<polygon points="1080,0 1120,0 940,{H} 900,{H}" fill="url(#reflejo_o)"/></g>')
        cuerpo += f'<polygon points="{pts}" fill="none" stroke="#FFFBF2" stroke-opacity="0.35" stroke-width="1.2"/>'
        cuerpo += "".join(panel(PANELES[i], To if dentro(i) else T, i, "o" if dentro(i) else "") for i in orden)
        cuerpo += anotacion(T, lambda i: To if dentro(i) else T)
    else:
        cuerpo += "".join(panel(PANELES[i], T, i) for i in orden)
        if not suave:
            cuerpo += anotacion(T)
    if suave:   # versión atenuada para la cabecera de las páginas interiores
        cuerpo = f'<rect width="{W}" height="{H}" fill="#FFFBF2"/><g opacity="0.45">{cuerpo}</g>'
    # chispas sueltas
    for (x, y, r) in [(300, 40, 4), (1085, 125, 3.5), (1385, 160, 3), (95, 135, 3)]:
        cuerpo += estrella(x, y, r, T["col"]["cielo"], 0.8)
    alt = ("Pizarra de cristal con paneles flotantes de estadística e IA: regresión, distribuciones, "
           "redes neuronales, árboles, curvas ROC, control de procesos, fórmulas y código en R y Python")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'preserveAspectRatio="xMidYMid slice" role="img" aria-label="{alt}">\n{defs(T)}\n{cuerpo}\n</svg>\n')


if __name__ == "__main__":
    import os
    salida = os.environ.get("SALIDA", "images")
    if len(sys.argv) == 1:   # lo habitual: los dos banners de la web
        for nombre, suave in [("banner", False), ("banner-suave", True)]:
            with open(f"{salida}/{nombre}.svg", "w", encoding="utf-8") as fh:
                fh.write(banner("pantalla", suave))
            print(f"{salida}/{nombre}.svg")
        sys.exit()
    for t in sys.argv[1:]:   # pruebas de otros temas
        with open(f"{salida}/banner-{t}.svg", "w", encoding="utf-8") as fh:
            fh.write(banner(t))
        print(f"{salida}/banner-{t}.svg")
