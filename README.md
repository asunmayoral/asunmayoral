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

Repositorio: **github.com/asunmayoral/asunmayoral.github.io** (público). Mientras no se active el dominio,
la web se verá en `https://asunmayoral.github.io/`.

Antes de empezar, con cualquiera de las dos opciones: si dentro de esta carpeta hay una subcarpeta
`asunmayoral/` (una copia clonada del repositorio), sácala de aquí (por ejemplo, arrástrala al Escritorio).
No debe formar parte del proyecto.

### Opción A · Desde el Terminal

```bash
cd ~/Claude/Projects/asunmayoral
git rm --cached asunmayoral          # solo si la subcarpeta llegó a guardarse en un commit
git add .
git commit -m "Quita la carpeta anidada y ajusta rutas para GitHub Pages"
git remote add origin https://github.com/asunmayoral/asunmayoral.github.io.git
# (si el remoto ya existía con otro nombre: git remote set-url origin https://github.com/asunmayoral/asunmayoral.github.io.git)
git pull origin main --allow-unrelated-histories --no-edit   # integra el commit inicial creado en GitHub
git push -u origin main
```

Al hacer `push`, como contraseña se usa un *token* personal de GitHub
(*Settings › Developer settings › Personal access tokens*), no la contraseña de la cuenta.

### Opción B · Con GitHub Desktop

GitHub Desktop no sabe unir la carpeta local con un repositorio de GitHub que ya tiene su propio
commit inicial (el `.gitattributes` que se crea al hacer el repositorio). Lo más sencillo es dejar
que sea GitHub Desktop quien cree el repositorio:

1. **Vacía el sitio en GitHub.** En github.com, abre `asunmayoral.github.io` ›
   *Settings* › *Danger Zone* › *Delete this repository*. Solo contiene ese fichero inicial; no se pierde nada.
2. **Abre la carpeta en GitHub Desktop.** *File › Add Local Repository…* › elige
   `~/Claude/Projects/asunmayoral` › *Add Repository*.
3. **Guarda los cambios pendientes.** En la pestaña *Changes* verás los últimos ajustes
   (y, si estaba guardada, la subcarpeta `asunmayoral` marcada como eliminada). Escribe un resumen
   en *Summary* (p. ej. «Ajusta rutas para GitHub Pages») y pulsa *Commit to main*.
4. **Publica.** Pulsa *Publish repository* (barra superior):
   - *Name*: `asunmayoral.github.io`
   - Desmarca *Keep this code private*
   - *Publish repository*
5. A partir de aquí, el ciclo diario es: editar → *Commit to main* → *Push origin*.

Si prefieres conservar el repositorio que ya existe en GitHub, haz los pasos 2 y 3, después
*Repository › Repository Settings… › Remote* con la dirección
`https://github.com/asunmayoral/asunmayoral.github.io.git`, y ejecuta una sola vez en el Terminal
`git pull origin main --allow-unrelated-histories --no-edit`. Luego, *Push origin* en GitHub Desktop.

### Después, con cualquiera de las dos opciones

1. Crea la rama de publicación: en el Terminal (o en el terminal de RStudio/Positron), dentro de la carpeta,
   ejecuta `quarto publish gh-pages` y responde «sí».
2. En GitHub, *Settings › Pages*: origen «Deploy from a branch», rama `gh-pages`, carpeta `/ (root)`.
3. Desde ese momento, cada *push* a `main` publica la web sola (`.github/workflows/publish.yml`):
   tarda uno o dos minutos y se puede seguir en la pestaña *Actions* del repositorio.

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
