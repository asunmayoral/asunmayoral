# My Stat Space

Web personal de **Asun M. Mayoral**: estadística, ciencia de datos e IA para aprender y enseñar.
Hecha con [Quarto](https://quarto.org) y publicada en GitHub Pages.

## Trabajar en local

```bash
quarto preview      # vista previa con recarga automática
quarto render       # genera el sitio en _site/
```

El banner de la cabecera se regenera con `python scripts/hero_cluster.py` (necesita `numpy` y `scikit-learn`).

## Primera publicación en GitHub (una sola vez)

1. Crea en GitHub un repositorio llamado **`<tu-usuario>.github.io`** (público) y súbelo:
   ```bash
   git init && git add . && git commit -m "Primera versión de la web"
   git branch -M main
   git remote add origin https://github.com/<tu-usuario>/<tu-usuario>.github.io.git
   git push -u origin main
   ```
2. Crea la rama de publicación desde tu ordenador: `quarto publish gh-pages` (responde «sí»).
3. En GitHub, *Settings › Pages*: origen «Deploy from a branch», rama `gh-pages`, carpeta `/ (root)`.
4. Desde ese momento, cada `git push` a `main` publica la web sola (`.github/workflows/publish.yml`).

## Dominio asunmayoral.umh.es

Cuando la web esté lista en `https://<tu-usuario>.github.io`:

1. Pide al Servicio de Informática de la UMH un registro DNS **CNAME** de `asunmayoral.umh.es` a `<tu-usuario>.github.io`.
2. Crea un fichero `CNAME` en la raíz del repositorio con una sola línea: `asunmayoral.umh.es`, y añádelo a `resources` en `_quarto.yml`.
3. En *Settings › Pages*, escribe el dominio y activa *Enforce HTTPS*.

Las entradas antiguas del blog tienen redirecciones (`aliases`) desde sus direcciones de WordPress, así que los enlaces viejos seguirán funcionando.

## Pendiente

- [ ] Mover a `files/libros/` los PDF que hoy están en Dropbox y actualizar los enlaces en `recursos/recursos.yml`, `docencia/` y `publicaciones/`.
- [ ] Enlace propio para «Meta-análisis con R» (hoy apunta a RPubs).
- [ ] Revisar las 67 entradas migradas del blog (formato y enlaces externos antiguos).
- [ ] Decidir si se mantienen Twitter/X u otras redes en el pie.

## Cómo está organizado

Ver `CLAUDE.md`: estructura, campos de cada fichero de datos, valores permitidos y estilo.
