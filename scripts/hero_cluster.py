"""Genera los banners de cabecera de la web:
  images/banner.svg        banner panorámico de la portada
  images/banner-suave.svg  versión atenuada para la cabecera de las páginas interiores
Datos simulados con tendencia cúbica, tres grupos de un análisis cluster (k-means)
y curva de suavizado LOWESS. Uso: python scripts/hero_cluster.py (numpy + scikit-learn)."""
import numpy as np
from sklearn.cluster import KMeans

DEEP = ["#A8472A", "#2F6E50", "#7B2D63"]      # melocotón, menta, ciruela (tonos profundos)
PASTEL = ["#F8D5C2", "#CFE9DA", "#EBD3E4"]
INK, BG = "#2F2A36", "#FFFBF2"


def datos(seed=1997, n_por_grupo=26):
    rng = np.random.default_rng(seed)
    x = np.r_[rng.normal(1.6, 0.6, n_por_grupo), rng.normal(5, 0.65, n_por_grupo),
              rng.normal(8.4, 0.6, n_por_grupo)].clip(0.2, 9.8)
    x = np.sort(x)
    y = 0.12 * (x - 5) ** 3 - 2.0 * (x - 5) + 5 + rng.normal(0, 0.45, len(x))
    z = np.c_[x, y]; z = (z - z.mean(0)) / z.std(0) * [2.0, 1.0]   # más peso al eje x
    km = KMeans(n_clusters=3, n_init=20, random_state=1).fit(z)
    orden = list(np.argsort([x[km.labels_ == k].mean() for k in range(3)]))
    lab = np.array([orden.index(l) for l in km.labels_])
    return x, y, lab


def lowess(x, y, frac=0.4, it=2):
    n = len(x); r = int(np.ceil(frac * n)); yh = np.zeros(n); w_rob = np.ones(n)
    for _ in range(it + 1):
        for i in range(n):
            d = np.abs(x - x[i]); h = np.sort(d)[r]
            w = np.clip(1 - (d / h) ** 3, 0, 1) ** 3 * w_rob
            A = np.c_[np.ones(n), x - x[i]]; W = np.diag(w)
            yh[i] = np.linalg.solve(A.T @ W @ A, A.T @ W @ y)[0]
        res = y - yh; s = np.median(np.abs(res))
        w_rob = np.clip(1 - (res / (6 * s)) ** 2, 0, 1) ** 2
    return yh


def elipses(x, y, lab, X, Y):
    out = []
    for g in range(3):
        pts = np.c_[X(x[lab == g]), Y(y[lab == g])]
        c = pts.mean(0); cov = np.cov(pts.T) + np.eye(2) * 25
        vals, vecs = np.linalg.eigh(cov)
        ang = np.degrees(np.arctan2(vecs[1, 1], vecs[0, 1]))
        m = np.sqrt(np.einsum('ij,jk,ik->i', pts - c, np.linalg.inv(cov), pts - c)).max() * 1.04
        rx, ry = m * np.sqrt(vals[1]), m * np.sqrt(vals[0])
        t = np.radians(ang)
        hh = np.sqrt((rx * np.sin(t)) ** 2 + (ry * np.cos(t)) ** 2)   # semialtura de la elipse girada
        hw = np.sqrt((rx * np.cos(t)) ** 2 + (ry * np.sin(t)) ** 2)
        out.append((g, c, rx, ry, ang, hh, hw))
    return out


def svg(x, y, lab, W, H, padx, pady, opacidad=1.0, fondo=True, r=6.0):
    ys = lowess(x, y)
    ylo, yhi = y.min() - 0.5, y.max() + 0.5
    while True:                                   # ajusta márgenes hasta que las elipses quepan
        X = lambda v, padx=padx: padx + v / 10 * (W - 2 * padx)
        Y = lambda v, pady=pady: H - pady - (v - ylo) / (yhi - ylo) * (H - 2 * pady)
        E = elipses(x, y, lab, X, Y)
        if all(c[1] - hh >= 6 and c[1] + hh <= H - 6 for _, c, _, _, _, hh, _ in E) or pady > H / 3:
            break
        pady += 4
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'preserveAspectRatio="xMidYMid slice" role="img" '
         'aria-label="Diagrama de dispersión con tendencia cúbica, tres grupos y curva de suavizado">']
    if fondo:
        o.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    o.append(f'<g opacity="{opacidad}">')
    for g, c, rx, ry, ang, _, _ in E:
        o.append(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                 f'transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" fill="{PASTEL[g]}" fill-opacity="0.85" '
                 f'stroke="{DEEP[g]}" stroke-width="1.25" stroke-dasharray="5 5"/>')
    xg = np.linspace(x.min(), x.max(), 200); yg = np.interp(xg, x, ys)
    d = "M" + " L".join(f"{X(a):.1f} {Y(b):.1f}" for a, b in zip(xg, yg))
    o.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    for a, b, g in zip(x, y, lab):
        o.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="{r}" fill="{DEEP[g]}" stroke="{BG}" stroke-width="1.5"/>')
    o.append("</g></svg>")
    return "\n".join(o)


if __name__ == "__main__":
    x, y, lab = datos()
    open("images/banner.svg", "w").write(svg(x, y, lab, 1600, 300, 150, 30))
    open("images/banner-suave.svg", "w").write(svg(x, y, lab, 1600, 220, 150, 22, opacidad=0.5, r=5))
    print("grupos:", np.bincount(lab))
