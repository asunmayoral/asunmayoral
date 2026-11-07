# My Stat Space · guía para Claude

Web personal de Asun M. Mayoral (Estadística e Investigación Operativa, UMH), hecha con Quarto y publicada en GitHub Pages. Este fichero fija las convenciones para que cualquier sesión mantenga la web coherente.

## Estructura

| Carpeta / fichero | Qué contiene |
| --- | --- |
| `_quarto.yml` | Menú, pie, buscador, tema, ancho de página |
| `styles/mystat.scss` | Paleta, tipografías y componentes (tarjetas, puertas, etiquetas, chips) |
| `index.qmd` | Portada: banner, presentación, puertas, novedades, proyectos activos, últimas entradas |
| `recursos/recursos.yml` | **Catálogo de recursos.** Una entrada por recurso |
| `recursos/<tema>/index.qmd` | Páginas propias de recursos alojados aquí (p. ej. `bayesiana/`) |
| `proyectos/proyectos.yml` | Proyectos y contratos, con `categoria`, `estado` (Activo/Histórico) y `orden` |
| `blog/posts/AAAA-MM-DD-slug/index.qmd` | Entradas del Blog; imágenes en la misma carpeta |
| `docencia/`, `sobre-mi/` | Páginas fijas (contacto y perfiles de investigación están en Sobre mí) |
| `404.qmd` | Página de «no encontrada» |
| `_templates/*.ejs` | Plantillas de los listados (no tocar salvo para cambiar el diseño) |
| `scripts/hero_cluster.py` | Genera `images/banner.svg` y `images/banner-suave.svg` |
| `files/` | PDFs y otros ficheros descargables |

## Tareas habituales

### Añadir un recurso
1. Lee la página del recurso para escribir título y descripción (una o dos frases, sin adjetivos de promoción).
2. Añade una entrada a `recursos/recursos.yml` en el bloque que corresponda, con estos campos:
   `title`, `description`, `path`, `date` (AAAA-MM-DD; si solo hay año, 1 de enero), `anio` (texto que se muestra), `tipo`, `temas`, `origen`, y opcionalmente `autoria` y `nota`.
3. Valores permitidos (no inventes otros sin preguntar):
   - `tipo`: Asignatura, Curso, Taller, Libro, Apuntes y prácticas, Recopilatorio, Vídeo, Datos, Juego
   - `temas`: Estadística, Ciencia de datos, IA, Python, R, Bayesiana, Mejora de procesos, Innovación educativa, Comunicación científica, Competencia digital
   - `origen`: Propio (hecho por Asun, sola o en equipo) | Recomendado (de otras personas)
4. Libros: van en el catálogo con `tipo: Libro`; campos opcionales `portada` (imagen pequeña en `images/libros/`, ruta `/images/libros/...`) y `mas` / `mas_texto` (enlace extra, p. ej. Google Play). La antigua página Publicaciones ya no existe: redirige a Recursos.
5. Campo opcional `serie`: colección o proyecto al que pertenece (p. ej. `Unidigital-Prodigital`); se muestra como etiqueta y como filtro «Colección».
6. Las tres entradas con `date` más reciente aparecen en la portada.

### Cursos Unidigital-Prodigital
- Entrada del blog: `blog/posts/2026-11-07-cursos-unidigital-prodigital/` (un acordeón por curso, fichas de módulo con PDF, vídeo, cuestionario, infografía y ficha en RediUMH, y buscador).
- Los datos salen de la hoja de cálculo del proyecto, guardada en `fuentes/CURSOS_Y_RECURSOS.xlsx` (excluida de git porque tiene columnas internas).
- Tras cambiar la hoja: `python scripts/prodigital_desde_excel.py`. Regenera `cursos.yml` de la entrada y `recursos/recursos-prodigital.yml` (las 7 fichas del catálogo). No se editan a mano.
- Se enlaza desde Recursos (filtro Colección), Docencia › Formación continua y el proyecto Unidigital-Prodigital.

### Escribir una entrada del blog
- Carpeta nueva `blog/posts/AAAA-MM-DD-slug-corto/` con `index.qmd`.
- Cabecera: `title`, `date`, `categories` (de: Divulgación, Docencia, Estadística, IA, Innovación, Investigación, Opinión, Publicación, Recursos), `image` (opcional, fichero de la misma carpeta), `description` (una frase).
- Si lo redacta Claude a partir de notas, añade `draft: true` hasta que Asun lo revise.
- Las entradas con código R o Python se ejecutan en local (`execute: freeze: auto`); hay que hacer `quarto render` antes de subir para que se guarde `_freeze/`.

### Añadir o actualizar un proyecto
Entrada en `proyectos/proyectos.yml` (los campos están descritos al principio del fichero).
- `categoria`: Competencia digital | Innovación docente | Investigación | Contratos. Cada una es un acordeón en `proyectos/index.qmd`.
- `estado: Activo` añade la etiqueta «En marcha» y lo muestra en la portada. Si termina, cambia a `Histórico`.
- `orden`: año de inicio (ordena de más reciente a más antiguo dentro de cada categoría).
- Fuente de datos para completar: el CVN de Asun (no se sube nunca al repositorio: contiene datos personales).
- IP = quien figura como «Director» en el CVN (si es Asun, «IP: A. M. Mayoral»). No se usa otra figura de dirección.
- No se publican cuantías ni importes de proyectos o contratos.

### Docencia
Edita `docencia/index.qmd`. Está organizada en cuatro acordeones (`<details class="acordeon">`: Grado, Postgrado, Formación continua, Formación del profesorado); solo Grado se abre por defecto (`open`). En Grado, las asignaturas actuales van como tarjetas en «Asignaturas que imparto» y las demás en «Asignaturas anteriores». Cada línea usa el bloque `::: {.asig}` con `[años]{.anio}`; lo más reciente arriba. Un curso con varias ediciones (como Comunicación científica) va en un solo bloque con su tabla de ediciones (`::: {.ediciones}`), ordenada del año más reciente al más antiguo. La organización de eventos está en `sobre-mi/index.qmd`, tras la trayectoria.

## Estilo
- Castellano, tono cercano y claro; primera persona cuando habla Asun.
- Paleta: fondo crema `#FFFBF2`, tinta `#2F2A36`. Pastel solo para fondos y etiquetas; el texto siempre en tinta o en el tono profundo de cada color:
  melocotón `#F8D5C2/#A8472A` (Docencia), menta `#CFE9DA/#2F6E50` (Recursos), mantequilla `#FBE8AE/#8A6200` (Proyectos), ciruela `#EBD3E4/#7B2D63` (Blog), cielo `#D3E7F4/#2C628A` (cursos Unidigital-Prodigital).
- Tipografías: Fraunces (títulos), Atkinson Hyperlegible (texto), JetBrains Mono (código), Limelight solo en el logotipo.
- Nada de datos inventados: si falta un dato, se pregunta.

## Publicar
- `quarto preview` para ver los cambios en local.
- Asun sube los cambios con **GitHub Desktop** (*Commit to main* › *Push origin*); cada push a `main` publica la web con GitHub Actions (`.github/workflows/publish.yml`).
- Claude edita los ficheros de la carpeta y propone el resumen del commit, pero no hace push: la credencial del Terminal no tiene permiso `workflow`.
- Mensajes de commit en castellano y descriptivos («Añade recurso: Simulación de procesos»).
