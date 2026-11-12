# My Stat Space

Web personal de **Asun M. Mayoral**: estadística, ciencia de datos e IA para aprender y enseñar.
Hecha con [Quarto](https://quarto.org) y publicada en GitHub Pages.

| | |
| --- | --- |
| Web | <https://asunmayoral.github.io/> (después, `asunmayoral.umh.es`) |
| Repositorio | <https://github.com/asunmayoral/asunmayoral.github.io> |
| Carpeta local | `~/Claude/Projects/asunmayoral` |

## Cómo se publica

Al pulsar **Push origin** en GitHub Desktop, GitHub construye la web con la última versión de Quarto
y la publica sola (`.github/workflows/publish.yml`). No hace falta ejecutar nada en el Terminal.

## Actualizar la web con GitHub Desktop

1. **Haz los cambios** en la carpeta, a mano o pidiéndoselo a Claude.
2. **Abre GitHub Desktop.** Comprueba arriba a la izquierda que *Current repository* es
   `asunmayoral.github.io` y *Current branch* es `main`.
3. **Revisa los cambios** en la pestaña *Changes* (columna izquierda). Al pulsar cada fichero se ve qué ha cambiado.
4. **Guarda los cambios.** Abajo a la izquierda, escribe en *Summary* qué has hecho
   (por ejemplo, «Añade recurso: Simulación de procesos») y pulsa **Commit to main**.
5. **Súbelos.** Pulsa **Push origin** en la barra superior.
6. **Comprueba la publicación.** *Repository › View on GitHub* › pestaña **Actions**.
   «Publicar en GitHub Pages» tarda uno o dos minutos:
   - círculo verde: la web ya está actualizada (recarga la página del navegador);
   - cruz roja: algo ha fallado; abre la ejecución, copia el mensaje de error y pásaselo a Claude.

Si alguna vez se edita algo directamente en github.com, antes de empezar pulsa **Fetch origin**
y después **Pull origin** para traer esos cambios a la carpeta.

## Ver los cambios antes de publicarlos (opcional)

En el Terminal, o en el terminal de RStudio/Positron, dentro de la carpeta:

```bash
quarto preview
```

Se abre la web en el navegador y se recarga sola al guardar cambios. Para pararla, pulsa Ctrl + C.
Necesita Quarto 1.4 o posterior (instalador en quarto.org › Get Started); para publicar no hace falta.

El banner de la cabecera se regenera con `python scripts/hero_cluster.py` (necesita `numpy` y `scikit-learn`).

## Configuración inicial (ya hecha)

Para rehacerla en otro ordenador o en otro repositorio:

1. En GitHub Desktop: *File › Add Local Repository…* › elige la carpeta › *Add Repository*.
2. En github.com, en el repositorio: *Settings › Pages* › *Build and deployment* › *Source*: **GitHub Actions**.
3. *Push origin* y comprobar en *Actions* que la publicación termina en verde.

## Si algo falla

- **La publicación sale en rojo en *Actions*:** abre la ejecución fallida, copia el error y pásaselo a Claude.
- **Subir desde el Terminal da «refusing to allow … without `workflow` scope»:** la credencial guardada
  en el Llavero de macOS no tiene permiso para GitHub Actions. Sube desde GitHub Desktop.
- **Subir desde el Terminal da «RPC failed; HTTP 400»:** `git config http.postBuffer 524288000` y repetir.
- **`quarto preview` da «property name … is invalid»:** el Quarto del ordenador es antiguo; actualízalo.
- En el Terminal de Mac, no copies comentarios (`# …`) en la misma línea que un comando: zsh no los ignora.

## Dominio asunmayoral.umh.es

Cuando la web esté revisada en `https://asunmayoral.github.io/`:

1. Pide al Servicio de Informática de la UMH un registro DNS **CNAME** de `asunmayoral.umh.es` a `asunmayoral.github.io`.
2. En github.com: *Settings › Pages* › *Custom domain*: escribe `asunmayoral.umh.es` y pulsa *Save*.
   Cuando GitHub verifique el DNS, marca *Enforce HTTPS*.

Las entradas antiguas del blog tienen redirecciones (`aliases`) desde sus direcciones de WordPress,
así que los enlaces viejos seguirán funcionando.

## Pendiente

- [ ] Mover a `files/libros/` los PDF que hoy están en Dropbox y actualizar los enlaces en `recursos/recursos.yml` y `docencia/`.
- [ ] Enlace propio para «Meta-análisis con R» (hoy apunta a RPubs).
- [ ] Revisar las 67 entradas migradas del blog (formato y enlaces externos antiguos).
- [ ] Decidir si se mantienen Twitter/X u otras redes en el pie.

## Cómo está organizado

Ver `CLAUDE.md`: estructura, campos de cada fichero de datos, valores permitidos y estilo.

## Libros en PDF

Las copias de los libros están en `files/libros/` y se publican en `https://asunmayoral.umh.es/files/libros/<nombre>.pdf`.

- **Actualizar un libro**: sustituye el PDF por la versión nueva con el mismo nombre de fichero y sube el cambio con GitHub Desktop. Los enlaces de la web siguen funcionando.
- **Añadir un libro**: copia el PDF en `files/libros/` con un nombre en minúsculas, sin espacios ni tildes (p. ej. `modelos-de-regresion.pdf`) y pide a Claude que lo añada al catálogo de Recursos.
- GitHub no admite ficheros de más de 100 MB; por encima de 50 MB avisa, pero los acepta.
