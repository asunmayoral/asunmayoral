# My Stat Space

Web personal de **Asun M. Mayoral**: estadística, ciencia de datos e IA para aprender y enseñar.
Hecha con [Quarto](https://quarto.org) y publicada en GitHub Pages.

## Trabajar en local

```bash
quarto preview
quarto render
```

`quarto preview` abre una vista previa que se recarga sola; `quarto render` genera el sitio en `_site/`.

El banner de la cabecera se regenera con `python scripts/hero_cluster.py` (necesita `numpy` y `scikit-learn`).

## Repositorio

**github.com/asunmayoral/asunmayoral.github.io** (público). Mientras no se active el dominio,
la web se ve en `https://asunmayoral.github.io/`.

La carpeta local `~/Claude/Projects/asunmayoral` ya está conectada a ese repositorio y añadida a
GitHub Desktop. Los cambios se suben con **GitHub Desktop**: se identifica con la cuenta de GitHub y tiene
los permisos necesarios, incluido el de los ficheros de GitHub Actions (`.github/workflows/`).

## Publicar cambios con GitHub Desktop

1. Haz los cambios en la carpeta (a mano o pidiéndoselo a Claude) y, si quieres, compruébalos con `quarto preview`.
2. Abre GitHub Desktop. En la columna izquierda, pestaña *Changes*, aparecen los ficheros modificados.
3. Escribe un resumen en *Summary* (por ejemplo «Añade recurso: Simulación de procesos») y pulsa **Commit to main**.
4. Pulsa **Push origin** en la barra superior.
5. GitHub publica la web sola en uno o dos minutos. El progreso se ve en la pestaña *Actions* del
   repositorio (*Repository › View on GitHub*).

Si se ha editado algo directamente en github.com, pulsa antes **Fetch origin** y luego **Pull origin**
para traer esos cambios a la carpeta.

## Activar la publicación (una sola vez)

La web la construye y publica GitHub con la última versión de Quarto (`.github/workflows/publish.yml`),
así que no depende de la versión instalada en el ordenador.

1. En GitHub, *Settings › Pages* › *Build and deployment* › *Source*: elige **GitHub Actions**.
2. Haz *Push origin* desde GitHub Desktop (o, en la pestaña *Actions*, abre «Publicar en GitHub Pages»
   y pulsa *Run workflow*).
3. En uno o dos minutos la web aparece en `https://asunmayoral.github.io/`. Desde ese momento, cada
   *Push origin* la vuelve a publicar.

Para ver los cambios en local con `quarto preview` conviene tener Quarto 1.4 o posterior
(instalador en quarto.org › Get Started).

## Si alguna vez falla una subida

- **«refusing to allow … without `workflow` scope»** al subir desde el Terminal: la credencial guardada en el
  Llavero de macOS no tiene permiso para GitHub Actions. Sube desde GitHub Desktop.
- **«RPC failed; HTTP 400»** desde el Terminal: amplía el búfer con
  `git config http.postBuffer 524288000` y vuelve a intentarlo.
- En el Terminal de Mac, no copies comentarios (`# …`) en la misma línea que un comando: zsh no los ignora.

## Dominio asunmayoral.umh.es

Cuando la web esté lista en `https://asunmayoral.github.io/`:

1. Pide al Servicio de Informática de la UMH un registro DNS **CNAME** de `asunmayoral.umh.es` a `asunmayoral.github.io`.
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
