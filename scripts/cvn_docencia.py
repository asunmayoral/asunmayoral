import re, sys, unicodedata, collections, yaml

# Uso: pdftotext -layout files/CVN140_docencia_umh.pdf /tmp/cvn.txt
#      python3 scripts/cvn_docencia.py /tmp/cvn.txt docencia/docencia.yml docencia/docencia-cvn.yml
# Lee el texto del CVN de docencia y escribe un yml alternativo con el esquema de docencia.yml.
src, actual, out = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src, encoding='utf-8').read()
# quitar pies de página (número + huella)
t = re.sub(r'\n[ \t]*\d{1,3}[ \t]*\n(?:[ \t]*\n)*[ \t]*[0-9a-f]{32}[ \t]*\n', '\n', t)
a = t.index('Formación académica impartida'); b = t.index('Dirección de tesis doctorales'); c = t.index('Publicaciones docentes')
docencia, direccion = t[a:b], t[b:c]

KEYS = ['Tipo de docencia', 'Nombre de la asignatura/curso', 'Tipo de programa', 'Titulación universitaria',
        'Frecuencia de la actividad', 'Fecha de inicio', 'Fecha de finalización', 'Tipo de horas/créditos ECTS',
        'Nº de horas/créditos ECTS', 'Entidad de realización', 'Tipo de entidad', 'Facultad, instituto, centro', 'Departamento',
        'Título del trabajo', 'Tipo de proyecto', 'Alumno/a', 'Calificación obtenida', 'Fecha de defensa']
kre = re.compile('(' + '|'.join(re.escape(k) for k in KEYS) + r'):')

def registros(sec):
    partes = re.split(r'\n[ \t]{0,4}\d{1,3}[ \t]+(?=Tipo de docencia:|Título del trabajo:)', '\n' + sec)
    for p in partes[1:]:
        campos = collections.defaultdict(list); last = None
        for line in p.split('\n'):
            line = line.strip()
            if not line: continue
            ms = list(kre.finditer(line))
            if not ms:
                if last: campos[last][-1] += ' ' + line
                continue
            if ms[0].start() > 0 and last: campos[last][-1] += ' ' + line[:ms[0].start()].strip()
            for i, m in enumerate(ms):
                fin = ms[i + 1].start() if i + 1 < len(ms) else len(line)
                last = m.group(1); campos[last].append(line[m.end():fin].strip())
        yield {k: [re.sub(r'\s+', ' ', x).strip() for x in v] for k, v in campos.items()}

PEQ = set('de del la las el los y e a en para con por al o u'.split())
ACENTOS = {'tecnicas': 'técnicas', 'investigacion': 'investigación', 'analisis': 'análisis', 'estadistica': 'estadística',
           'estadistico': 'estadístico', 'metodos': 'métodos', 'regresion': 'regresión', 'teoria': 'teoría',
           'introduccion': 'introducción', 'econometria': 'econometría', 'ingenieria': 'ingeniería', 'matematica': 'matemática'}
SIGLAS = {'eso', 'fp', 'ei', 'tic', 'tics', 'ade', 'umh'}
def tc(s):
    ws = s.lower().split(); r = []
    for i, w in enumerate(ws):
        w = ACENTOS.get(w, w)
        if w.strip('(),.') in SIGLAS: w = w.upper()
        elif i and w in PEQ: pass
        else: w = w[:1].upper() + w[1:]
        r.append(w)
    return ' '.join(r).replace(' Ii', ' II')
def norm(s): return re.sub(r'[^a-z0-9 ]', ' ', ''.join(ch for ch in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(ch) != 'Mn'))
def titulacion(s):
    s = re.sub(r'\s*\((P\d+)\)', '', s).strip()
    if s.startswith('Máster Universitario en Formación del Profesorado'):
        return 'Máster Universitario en Formación del Profesorado de ESO, Bachillerato, FP y Enseñanza de Idiomas'
    if s.startswith('Máster Universitario en Investigación en Medicina Clínica'):
        return 'Máster Universitario en Investigación en Medicina Clínica'
    return s
def asignatura(s):
    n = norm(s)
    if n.startswith('tecnologias de') and 'informacion y comunicacion aplicadas' in n:
        return 'TECNOLOGÍAS DE LA INFORMACIÓN Y COMUNICACIÓN APLICADAS A DOCENCIA Y APRENDIZAJE'
    if n.startswith('sociedad familia y educacion'):
        return 'SOCIEDAD, FAMILIA Y EDUCACIÓN'
    return s
BLOQUE = {'Grado': 'grado', 'Licenciatura': 'licenciatura', 'Diplomatura': 'licenciatura', 'Máster oficial': 'postgrado'}
def g(r, k, i=0):
    v = r.get(k, []); return v[i] if len(v) > i else ''
def anio(s):
    m = re.search(r'(\d{4})', s or ''); return int(m.group(1)) if m else None

grupos = collections.OrderedDict(); n = 0
for r in registros(docencia):
    n += 1
    prog = g(r, 'Tipo de programa'); tit = titulacion(g(r, 'Titulación universitaria'))
    nom = g(r, 'Nombre de la asignatura/curso') or tit
    nom = asignatura(nom)
    key = (norm(nom), norm(tit))
    e = grupos.setdefault(key, {'nom': nom, 'tit': tit, 'prog': prog, 'oficial': g(r, 'Tipo de docencia', 0),
                                'ent': g(r, 'Entidad de realización').replace(' Tipo de entidad:', '').strip(),
                                'centros': [], 'tipos': [], 'periodos': [], 'cred': 0.0, 'horas': 0.0, 'n': 0})
    e['n'] += 1
    d, h = anio(g(r, 'Fecha de inicio')), anio(g(r, 'Fecha de finalización'))
    h = h or d
    if d: e['periodos'].append((d, h))
    tipo = g(r, 'Tipo de docencia', 1)
    if tipo and tipo not in e['tipos']: e['tipos'].append(tipo)
    cen = g(r, 'Facultad, instituto, centro')
    if cen and cen not in e['centros']: e['centros'].append(cen)
    try:
        v = float(g(r, 'Nº de horas/créditos ECTS').replace('.', '').replace(',', '.'))
        if g(r, 'Tipo de horas/créditos ECTS').lower().startswith('cr'): e['cred'] += v
        else: e['horas'] += v
    except ValueError: pass

# ¿está ya en docencia.yml?
web = yaml.safe_load(open(actual, encoding='utf-8'))
webtxt = [norm(x['title'] + ' ' + str(x.get('detalle', ''))) for x in web]
def en_web(nom):
    w = [x for x in norm(nom).split() if x not in PEQ and len(x) > 2]
    if not w: return False
    return any(all(x in wt.split() for x in w) for wt in webtxt)

ORD = ['grado', 'licenciatura', 'postgrado', 'continua', 'profesorado', 'direccion']
entradas = []
for e in grupos.values():
    ds = [p[0] for p in e['periodos']]; hs = [p[1] for p in e['periodos']]
    bloque = BLOQUE.get(e['prog'], 'postgrado')
    titulo = tc(e['nom']) if e['nom'] != e['tit'] else e['tit'].title().replace(' En ', ' en ').replace(' De ', ' de ')
    det = e['tit'] if e['nom'] != e['tit'] else e['prog'] + ' (título propio)'
    x = {'title': titulo, 'bloque': bloque}
    if ds: x['desde'] = min(ds); x['hasta'] = max(hs)
    x['detalle'] = det
    x['en_web'] = en_web(titulo)
    cvn = {'docencia': e['oficial'], 'programa': e['prog'], 'registros': e['n'],
           'periodos': sorted({f'{a}–{b}' if a != b else str(a) for a, b in e['periodos']})}
    if e['tipos']: cvn['tipos'] = e['tipos']
    if e['cred']: cvn['creditos'] = round(e['cred'], 2)
    if e['horas']: cvn['horas'] = round(e['horas'], 1)
    if e['centros']: cvn['centro'] = '; '.join(e['centros'])
    x['cvn'] = cvn
    entradas.append(x)

ndir = 0
for r in registros(direccion):
    ndir += 1
    tit = g(r, 'Título del trabajo'); prog = ''
    m = re.search(r'\.?\s*Dentro del Programa\s*:\s*(.*)$', tit)
    if m: prog = m.group(1).strip(); tit = tit[:m.start()].strip(' .')
    if tit.isupper():
        tit = re.sub(r'(^|\. )(\w)', lambda m: m.group(1) + m.group(2).upper(), tit.lower())
        for v, nv in [('ods', 'ODS'), ('educación secundaria', 'Educación Secundaria'), ('comunidad valenciana', 'Comunidad Valenciana'), ('españa', 'España')]:
            tit = re.sub(r'\b' + v + r'\b', nv, tit)
    tipo = g(r, 'Tipo de proyecto'); al = g(r, 'Alumno/a')
    if ',' in al: ap, nm = [s.strip() for s in al.split(',', 1)]; al = tc(nm) + ' ' + tc(ap)
    tipo_txt = {'Tesis Doctoral': 'Tesis doctoral', 'Proyecto Final de Carrera': 'Trabajo fin de estudios'}.get(tipo, tipo)
    det = f'{tipo_txt} de {al}'
    if prog: det += ', ' + prog
    if g(r, 'Entidad de realización') and not prog: det += ', ' + g(r, 'Entidad de realización')
    if g(r, 'Calificación obtenida'): det += f' ({g(r, "Calificación obtenida").lower()})'
    y = anio(g(r, 'Fecha de defensa'))
    entradas.append({'title': tit, 'bloque': 'direccion', 'desde': y, 'hasta': y, 'detalle': det,
                     'en_web': en_web(tit), 'cvn': {'defensa': g(r, 'Fecha de defensa')}})

entradas.sort(key=lambda x: (ORD.index(x['bloque']), -(x.get('hasta') or 0), -(x.get('desde') or 0), x['title']))

cab = f'''# Docencia según el CVN de docencia UMH (files/CVN140_docencia_umh.pdf, generado el 11/11/2026).
# Fichero ALTERNATIVO para revisar y depurar: ninguna página lo lee. Generado por
# scripts/cvn_docencia.py a partir de {n} registros de «Formación académica impartida»
# y {ndir} de «Dirección de tesis doctorales y/o proyectos fin de carrera».
#
# Mismo esquema que docencia.yml (title, bloque, desde, hasta, detalle) más dos campos de ayuda:
#   en_web   true si ya hay una entrada equivalente en docencia.yml (comparación por palabras; revísalo)
#   cvn      datos del CVN agregados: tipo de docencia, nº de registros, periodos, tipos de clase,
#            créditos u horas sumados y centro. Se quita al pasar la entrada a docencia.yml.
#            Los créditos son la suma de lo que declara cada registro; un registro puede abarcar varios cursos
#            (p. ej. 2013–2026), así que sirven para comparar pesos, no como total exacto.
# Una entrada por asignatura y titulación. Se unifican los dos planes del Máster de Profesorado
# y las dos grafías de la asignatura de TIC. Los nombres van con mayúscula inicial y con las tildes
# que faltan en el CVN (Técnicas, Investigación, Análisis...).
# desde/hasta: primer año de inicio y último año de finalización que da el CVN (2025–2026 = curso 2025-26).
'''
with open(out, 'w', encoding='utf-8') as f:
    f.write(cab)
    actual_b = None
    for x in entradas:
        if x['bloque'] != actual_b:
            actual_b = x['bloque']
            nom = {'grado': 'Grado', 'licenciatura': 'Licenciaturas y diplomaturas', 'postgrado': 'Postgrado (másteres oficiales y títulos propios)', 'direccion': 'Dirección de tesis y trabajos fin de estudios'}[actual_b]
            f.write(f'\n# =================== {nom} ===================\n')
        f.write('\n' + yaml.dump([x], allow_unicode=True, sort_keys=False, width=200, default_flow_style=None))
print(n, ndir, len(entradas), collections.Counter(x['bloque'] for x in entradas), sum(x['en_web'] for x in entradas))
