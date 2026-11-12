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
| `proyectos/proyectos.yml` | Proyectos y contratos (solo datos; no hay página Proyectos). La `categoria` decide en qué página sale cada uno |
| `divulgacion/index.qmd` | Divulgación: proyectos y eventos de divulgación, enlaces a los cursos de comunicación científica y entradas del blog con categoría Divulgación |
| `blog/posts/AAAA-MM-DD-slug/index.qmd` | Entradas del Blog; imágenes en la misma carpeta |
| `investigacion/index.qmd` | Perfil investigador: línea temporal, líneas de trabajo, publicaciones y entradas del blog relacionadas |
| `investigacion/investigacion.yml` | Líneas, etapas profesionales, publicaciones y tesis (los proyectos salen de `proyectos/proyectos.yml`) |
| `docencia/index.qmd` | Docencia: tarjetas de lo que imparte, línea temporal y acordeones por nivel |
| `docencia/docencia.yml` | Asignaturas, cursos y trabajos dirigidos (una entrada por cada uno) |
| `sobre-mi/` | Página fija (contacto y perfiles) |
| `404.qmd` | Página de «no encontrada» |
| `_templates/*.ejs` | Plantillas de los listados (no tocar salvo para cambiar el diseño) |
| `scripts/hero_cluster.py` | Genera `images/banner.svg` y `images/banner-suave.svg` |
| `files/` | PDFs y otros ficheros descargables (`files/libros/`: copias de los libros de Asun) |

## Tareas habituales

### Añadir un recurso
1. Lee la página del recurso para escribir título y descripción (una o dos frases, sin adjetivos de promoción).
2. Añade una entrada a `recursos/recursos.yml` en el bloque que corresponda, con estos campos:
   `title`, `description`, `path`, `date` (AAAA-MM-DD; si solo hay año, 1 de enero), `anio` (texto que se muestra), `tipo`, `temas`, `origen`, y opcionalmente `autoria` y `nota`.
3. Valores permitidos (no inventes otros sin preguntar):
   - `tipo`: Curso/Taller, Libro, Recopilatorio, Vídeo, Datos, Juego
   - `temas`: Estadística-CC Datos, IA, Bayesiana, Mejora de procesos, Innovación educativa, Comunicación científica, Competencia digital (la materia)
   - `lenguaje` (opcional): lista con R y/o Python. Tiene su propio filtro y etiqueta. Si un curso tiene materiales separados en R y en Python, una entrada por lenguaje con «(R)» o «(Python)» en el título; si están en la misma web, una entrada con `lenguaje: [R, Python]`. En Docencia, el texto del enlace lleva el lenguaje: «Web de la asignatura (R)».
   - `origen`: Propio (hecho por Asun, sola o en equipo) | Recomendado (de otras personas)
   Si `description` pasa de unos 110 caracteres, añade `resumen` (una frase corta): es lo que muestra la tarjeta; la descripción completa sigue sirviendo al buscador y la información detallada está en el destino del enlace.
4. Libros: van en el catálogo con `tipo: Libro`; campos opcionales `portada` (imagen pequeña en `images/libros/`, ruta `/images/libros/...`) y `mas` / `mas_texto` (enlace extra, p. ej. Google Play). La antigua página Publicaciones ya no existe: redirige a Recursos.
   Copias de los libros: los PDF están en `files/libros/` (nombres en minúscula, sin espacios ni tildes, con guiones). En `recursos.yml`, `path` apunta a la Editorial UMH si el libro está allí (es prioritaria) y el campo `pdf: /files/libros/<fichero>.pdf` añade el enlace «Copia en PDF»; si no hay página de la editorial, `path` apunta directamente al PDF. En `docencia.yml` se enlaza igual: editorial si existe, si no la copia. Para sustituir un libro, Asun reemplaza el PDF con el mismo nombre y sube el cambio; los enlaces no cambian. GitHub rechaza ficheros de más de 100 MB.
5. Campo opcional `serie`: colección o proyecto al que pertenece (p. ej. `Unidigital-Prodigital`); se muestra como etiqueta y como filtro «Colección».
6. Las tres entradas con `date` más reciente aparecen en la portada.

### Cursos Unidigital-Prodigital
- Entrada del blog: `blog/posts/2026-11-07-cursos-unidigital-prodigital/` (un acordeón por curso, fichas de módulo con PDF, vídeo, cuestionario, infografía y ficha en RediUMH, y buscador).
- Los datos salen de la hoja de cálculo del proyecto, guardada en `fuentes/CURSOS_Y_RECURSOS.xlsx` (excluida de git porque tiene columnas internas).
- Tras cambiar la hoja: `python scripts/prodigital_desde_excel.py`. Los resúmenes de las tarjetas están en el diccionario `RESUMENES` del script. Regenera `cursos.yml` de la entrada y `recursos/recursos-prodigital.yml` (las 7 fichas del catálogo). No se editan a mano.
- Se enlaza desde Recursos (filtro Colección), Docencia › Formación continua y el proyecto Unidigital-Prodigital.

### Escribir una entrada del blog
- Carpeta nueva `blog/posts/AAAA-MM-DD-slug-corto/` con `index.qmd`.
- Cabecera: `title`, `date`, `categories` (de: Divulgación, Docencia, Estadística, IA, Innovación, Investigación, Opinión, Publicación, Recursos), `image` (opcional, fichero de la misma carpeta), `description` (una frase).
- Si lo redacta Claude a partir de notas, añade `draft: true` hasta que Asun lo revise.
- Las entradas con código R o Python se ejecutan en local (`execute: freeze: auto`); hay que hacer `quarto render` antes de subir para que se guarde `_freeze/`.

### Añadir o actualizar un proyecto
Entrada en `proyectos/proyectos.yml` (los campos están descritos al principio del fichero).
- `categoria` decide la página (los tres perfiles del menú: Docencia, Investigación, Divulgación):
  - `Innovación docente` y `Materiales formativos` → acordeón «Innovación docente y proyectos formativos» de `docencia/index.qmd`. `Materiales formativos` son los proyectos de generación de materiales de Unidigital UMH (fondos UE del Plan de Recuperación, 2021-2022): Prodigital (IP), IASAC y Simustat. IA4legos es un programa de cursos y está en Docencia › Formación continua (2023-2025).
  - `Divulgación` (concursos, ferias, jornadas, congresos de estudiantes) → `divulgacion/index.qmd`.
  - `Investigación` y `Contratos` → `investigacion/index.qmd`, dentro de su `linea` (sin `linea` van a «Otras ayudas»).
  - Un proyecto docente que generó publicaciones lleva además `linea`, `desde` y `hasta` y aparece también en Investigación (ADAS, PIC, TFGi).
- Regla general: cada cosa tiene **una sola casa** y desde las demás se enlaza, no se duplica. Los cursos sobre comunicación científica son docencia: viven en Docencia y Divulgación solo los enlaza (bloque «Enseñar a comunicar ciencia»).
- `/proyectos/` redirige a Investigación (`aliases`).
- `estado: Activo` añade la etiqueta «En marcha» y lo muestra en la portada. Si termina, cambia a `Histórico`.
- `orden`: año de inicio (ordena de más reciente a más antiguo dentro de cada categoría).
- Fuente de datos para completar: el CVN de Asun (no se sube nunca al repositorio: contiene datos personales).
- IP = quien figura como «Director» en el CVN (si es Asun, «IP: A. M. Mayoral»). No se usa otra figura de dirección.
- No se publican cuantías ni importes de proyectos o contratos.

### Investigación
La página `investigacion/index.qmd` no se edita para añadir contenido: se genera con tres plantillas (`_templates/investigacion-*.ejs`) a partir de los datos.
- **Publicación nueva**: entrada `clase: publicacion` en `investigacion/investigacion.yml` (`title`, `autores`, `fuente`, `anio`, `tipo`, `linea`, y opcionales `path` con el DOI y `blog` con la entrada relacionada). Aparece sola en la línea temporal y en la lista de su línea.
- **Proyecto o contrato**: se añade en `proyectos/proyectos.yml`; si lleva `linea`, `desde` y `hasta` sale también en Investigación.
- Cada línea es un acordeón (`details.acordeon.inv-linea`), cerrado por defecto; se abre al llegar desde la línea temporal.
- **Líneas** (`clase: linea`): bayes, ambiente, salud, educacion, ia, sociedad. Una línea nueva necesita además su color en `styles/mystat.scss` (clase `.l-<id>`). `activa: true` la prolonga hasta hoy.
- **Blog**: las entradas con categoría Investigación o Publicación se listan al final de la página (las ocho más recientes).
- El texto de presentación sale del resumen del CVN; el CVN no se sube nunca (`CVN*.pdf` está en `.gitignore`).

### Docencia
La página `docencia/index.qmd` no se edita para añadir contenido: se genera con tres plantillas (`_templates/docencia-*.ejs`).
- Grado, licenciaturas y másteres de la UMH están confirmados por Asun con el CVN de docencia (nov. 2026); no se añaden asignaturas UMH que no estén ahí sin preguntar.
- **TFG y TFM dirigidos**: la fuente es `fuentes/TFG_TFM_dirigidos.xlsx` (excluida de git: tiene notas). Pestañas TFG y TFM; las columnas «Título (web)» y «Estudiante (web)» son lo que se publica. Tras cambiar la hoja: `python3 scripts/trabajos_desde_excel.py`, que regenera `docencia/trabajos.yml` (no se edita a mano). Se publica: TFG con título, estudiante, curso, codirección y enlace a RediUMH (columna «Repositorio (RediUMH)»); TFM solo resumidos por especialidad y con la lista de títulos por curso, sin nombres. Nunca se publican notas. En la línea temporal salen como puntos (TFG rellenos, TFM huecos).
- **Tesis doctorales dirigidas**: no van en Docencia, sino en `investigacion/investigacion.yml` (`clase: tesis`, `autores: "Nombre (tesis dirigida)"`); el acordeón de TFG enlaza a Investigación.
- **Asignatura o curso nuevo**: una entrada en `docencia/docencia.yml` (los campos están descritos al principio del fichero): `title`, `bloque` (grado | licenciatura | postgrado | continua | profesorado | direccion), `desde`, `hasta`, `detalle`, `enlaces`.
- Sin `hasta` (o con `hasta` posterior al año actual) la entrada está **en curso**: barra de tono fuerte en la línea temporal y etiqueta «En curso». Cuando deja de impartirse, se añade `hasta`.
- `tarjeta: true` la muestra además en «Asignaturas que imparto» (no la marca como actual: eso depende solo de `hasta`). La tarjeta pone arriba la titulación (el `detalle` hasta el primer punto) y debajo el resto; el título enlaza a `path` o, si no hay, al primer enlace.
- Formato homogéneo de `detalle`: «Titulación o entidad. Resto (horas, papel, código…)», sin punto final.
- La docencia oficial en la UMH se ajusta al CVN de docencia. Lo retirado y la versión anterior de lo corregido están en `docencia/docencia-retiradas.yml`, que ninguna página lee. La formación fuera de la UMH y en títulos propios no se contrasta con el CVN.
- Del Máster de Formación del Profesorado solo se muestra «TICs para la docencia y el aprendizaje».
- `docencia/docencia-cvn.yml` es la docencia tal como figura en el CVN de docencia UMH, con el mismo esquema más `en_web` y `cvn` (datos de ayuda). Sirve para revisar; ninguna página lo lee. Se regenera con `scripts/cvn_docencia.py` (instrucciones al principio del script).
- Un programa que agrupa varios cursos (IA4legos) lleva `cursos` (lista de `anio`, `title`, `horas`).
- Un curso con varias ediciones lleva `ediciones` (lista de `anio`, `programa`, `universidad`) y sale con su tabla.
- `corto` es el nombre abreviado de la barra; `id` fija el ancla si otra página enlaza a la entrada (Divulgación enlaza a `comunicacion-cientifica` y `comunicacion-web`).
- El orden de las listas es automático (en curso primero; luego de lo más reciente a lo más antiguo).
- El acordeón «Innovación docente y proyectos formativos» y su fila de la línea temporal salen de `proyectos/proyectos.yml` (necesitan `desde` y `hasta`).
- La organización de eventos está en `divulgacion/index.qmd`.
- El script `_templates/acordeon.html` (incluido en todas las páginas desde `_quarto.yml`) abre el acordeón al que apunta un enlace `#ancla`.

## Estilo
- Castellano, tono cercano y claro; primera persona cuando habla Asun.
- Paleta: fondo crema `#FFFBF2`, tinta `#2F2A36`. Pastel solo para fondos y etiquetas; el texto siempre en tinta o en el tono profundo de cada color:
  melocotón `#F8D5C2/#A8472A` (Docencia), menta `#CFE9DA/#2F6E50` (Recursos), mantequilla `#FBE8AE/#8A6200` (Divulgación), ciruela `#EBD3E4/#7B2D63` (Blog), cielo `#D3E7F4/#2C628A` (Investigación, cursos Unidigital-Prodigital).
- Tipografías: Fraunces (títulos), Atkinson Hyperlegible (texto), JetBrains Mono (código), Limelight solo en el logotipo.
- Nada de datos inventados: si falta un dato, se pregunta.

## Publicar
- `quarto preview` para ver los cambios en local.
- Asun sube los cambios con **GitHub Desktop** (*Commit to main* › *Push origin*); cada push a `main` publica la web con GitHub Actions (`.github/workflows/publish.yml`).
- Claude edita los ficheros de la carpeta y propone el resumen del commit, pero no hace push: la credencial del Terminal no tiene permiso `workflow`.
- Mensajes de commit en castellano y descriptivos («Añade recurso: Simulación de procesos»).
