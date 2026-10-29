# Arma la landing en portugués (/pt) y en inglés (/en) a partir de los archivos en español.
#
# Uso, desde la raíz del repo:
#   python3 i18n/armar.py            arma todo: pt/index.html, en/index.html, tablero-pt.html y tablero-en.html
#   python3 i18n/armar.py tablero    arma una sola página (index o tablero)
#
# index.html y tablero.html (en español) son las únicas fuentes que se editan a mano. Cada vez que
# cambia un texto hay que correrlo. Las traducciones están en i18n/textos.json (la landing) y en
# i18n/tablero.json (el tablero del supervisor), con estas listas:
#   textos      textos del HTML (nodos de texto, atributos, <title> y descripciones): {es, pt, en}
#   iguales     textos del HTML que no se traducen (marcas, nombres propios)
#   js          textos de los <script> de la página: {es, pt, en}. Se reemplazan tal cual y solo
#               dentro de los <script>, así que pueden llevar comillas y un poco de código alrededor
#               cuando la frase cambia de orden en otro idioma
#   js_iguales  textos de los <script> que quedan igual (nombres de clientes, calles, barrios…)
#   fragmentos  reemplazos crudos en todo el archivo, por idioma, antes de traducir
#   atributos   atributos del HTML que también se traducen, además de alt, aria-label, placeholder y title
# Si aparece un texto que no tiene traducción (en el HTML o en un <script>), o hay una traducción
# de un <script> cuyo texto ya no está en el archivo, lo lista y no escribe nada: se agrega la
# traducción y se vuelve a correr. Así las tres versiones nunca quedan desparejas.
import html
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SITIO = 'https://www.libreta.dev'
IDIOMAS = {
    'pt': {'lang': 'pt-BR', 'locale': 'pt_BR', 'formato': 'pt-BR', 'ruta': '/pt', 'bandera': 'br'},
    'en': {'lang': 'en', 'locale': 'en_US', 'formato': 'en-US', 'ruta': '/en', 'bandera': 'us'},
}
PAGINAS = {
    'index': {'fuente': 'index.html', 'textos': 'textos.json', 'salida': '{idioma}/index.html'},
    'tablero': {'fuente': 'tablero.html', 'textos': 'tablero.json', 'salida': 'tablero-{idioma}.html'},
}
ATRIBUTOS = ('alt', 'aria-label', 'placeholder', 'title')
LETRAS = 'A-Za-zÁÉÍÓÚÜáéíóúüñÑ'
AVISO = '<!-- Generado por i18n/armar.py a partir de {fuente}: no editar a mano. -->\n'
# Partes del HTML: comentarios, scripts, estilos, etiquetas y, entre medio, el texto
PARTES = re.compile(r'(<!--.*?-->|<script\b.*?</script>|<style\b.*?</style>|<[^>]+>)', re.S)

normal = lambda t: re.sub(r'\s+', ' ', t).strip()


def cargar(pagina):
    datos = json.load(open(os.path.join(AQUI, PAGINAS[pagina]['textos']), encoding='utf-8'))
    for clave in ('textos', 'iguales', 'js', 'js_iguales', 'atributos'):
        datos.setdefault(clave, [])
    datos.setdefault('fragmentos', {})
    return datos


# ------------------------------------------------------------------ strings de JavaScript

def literales(codigo):
    """Los strings de un script, como (inicio, fin, contenido), salteando comentarios y expresiones regulares."""
    res, i, n, previo, palabra = [], 0, len(codigo), '', ''
    while i < n:
        c = codigo[i]
        if c in '\'"`':
            j = i + 1
            while j < n and codigo[j] != c and (c == '`' or codigo[j] != '\n'):
                j += 2 if codigo[j] == '\\' else 1
            res.append((i, j + 1, codigo[i + 1:j]))
            i, previo = j + 1, c
            continue
        if c == '/' and codigo[i + 1:i + 2] == '/':
            j = codigo.find('\n', i)
            i = n if j < 0 else j
            continue
        if c == '/' and codigo[i + 1:i + 2] == '*':
            j = codigo.find('*/', i + 2)
            i = n if j < 0 else j + 2
            continue
        if c == '/' and (previo in ('', 'w:return', 'w:typeof', 'w:case', 'w:in', 'w:of') or (len(previo) == 1 and previo in '(,=:[!&|?{};+-*%<>~^')):
            j, clase = i + 1, False
            while j < n and codigo[j] != '\n':
                if codigo[j] == '\\':
                    j += 2
                    continue
                if codigo[j] == '[':
                    clase = True
                elif codigo[j] == ']':
                    clase = False
                elif codigo[j] == '/' and not clase:
                    break
                j += 1
            i = j + 1
            while i < n and codigo[i].isalpha():
                i += 1
            previo = '/'
            continue
        if c.isalnum() or c in '_$':
            m = re.match(r'[\w$]+', codigo[i:])
            palabra = m.group(0)
            previo = 'w:' + palabra
            i += len(palabra)
            continue
        if not c.isspace():
            previo = c
        i += 1
    return res


def limpio(s):
    """El texto que se ve de un string de JavaScript: sin etiquetas, ni pedazos de etiquetas, ni entidades."""
    t = re.sub(r'\\[nrt]', ' ', s.replace('\x00', ' '))
    if '>' in t and ('<' not in t or t.index('>') < t.index('<')):
        t = t[t.index('>') + 1:]  # el string empieza en medio de una etiqueta
    t = re.sub(r'<[^>]*>', ' ', t)
    t = re.sub(r'<[^>]*$', ' ', t)  # la etiqueta sigue en el string siguiente
    return normal(html.unescape(t))


def parece_texto(t):
    """Si un string de JavaScript es texto que se ve (y por lo tanto hay que traducir)."""
    if not re.search('[%s]' % LETRAS, t):
        return False
    if re.search(r'=\s*["\']|[\w-]+=\s*$|^["\']', t):  # pedazos de atributos
        return False
    if re.fullmatch(r'[A-Z]{1,3}[ -]?\d[\d ]*', t):  # códigos (AL-001, P-2410, A 0081311)
        return False
    return bool(re.search(r'[ÁÉÍÓÚÜáéíóúüñÑ¿¡]', t)) or ' ' in t or t[0].isupper()


def patron_js(entradas):
    """Una sola expresión con todos los textos, del más largo al más corto, para reemplazar de una pasada."""
    textos = sorted({e['es'] for e in entradas}, key=len, reverse=True)
    return re.compile('|'.join(re.escape(t) for t in textos)) if textos else None


def scripts(s):
    """Los <script> de la página que tienen código (ni externos ni JSON-LD), como (inicio, fin)."""
    res = []
    for m in re.finditer(r'(<script\b[^>]*>)(.*?)(</script>)', s, re.S):
        if ' src=' in m.group(1) or 'application/ld+json' in m.group(1):
            continue
        res.append((m.start(2), m.end(2)))
    return res


def revisar_js(fuente, datos):
    """Lo que falta en la lista js: textos del script sin traducción y traducciones que ya no se usan."""
    errores = []
    codigo = ''.join(fuente[a:b] for a, b in scripts(fuente))
    for e in datos['js']:
        for idioma in IDIOMAS:
            if not isinstance(e.get(idioma), str):
                errores.append(f'Falta «{idioma}» en la traducción js de: {e["es"]}')
        if e['es'] not in codigo:
            errores.append(f'El texto js ya no está en el script: {e["es"]}')
    patron = patron_js(datos['js'])
    # Se marcan los caracteres que ya tienen traducción y los strings se leen del código original
    # (tapar el código antes de leerlo descuadra la cuenta de comillas si un reemplazo toca una regex)
    cubierto = bytearray(len(codigo))
    for m in (patron.finditer(codigo) if patron else []):
        cubierto[m.start():m.end()] = b'\x01' * (m.end() - m.start())
    iguales = set(datos['js_iguales']) | set(datos['iguales'])
    faltan = []
    for ini, _, contenido in literales(codigo):
        t = limpio(''.join('\x00' if cubierto[ini + 1 + k] else ch for k, ch in enumerate(contenido)))
        if parece_texto(t) and t not in iguales and t not in faltan:
            faltan.append(t)
    return errores, faltan


# ------------------------------------------------------------------ traducción de una página

def absoluta(url):
    """Las rutas relativas pasan a absolutas: la página en portugués vive en /pt y la en inglés en /en."""
    if not url or re.match(r'^(https?:|mailto:|tel:|data:|#|/|javascript:)', url):
        return url
    return '/' + url


def armar(pagina, idioma, datos, fuente):
    conf = IDIOMAS[idioma]
    tabla = {normal(t['es']): t for t in datos['textos']}
    iguales = set(datos['iguales'])
    atributos = ATRIBUTOS + tuple(datos['atributos'])
    faltan = set()

    def traducir(texto):
        clave = normal(texto)
        if not clave:
            return texto
        if clave in tabla:
            inicio = texto[:len(texto) - len(texto.lstrip())]
            fin = texto[len(texto.rstrip()):]
            return inicio + tabla[clave][idioma] + fin
        if not re.search('[%s]' % LETRAS, clave) or clave in iguales:
            return texto
        faltan.add(clave)
        return texto

    s = fuente
    for viejo, nuevo in datos['fragmentos'].get(idioma, []):
        if viejo not in s:
            sys.exit(f'{PAGINAS[pagina]["fuente"]}: el fragmento ya no está: {viejo}')
        s = s.replace(viejo, nuevo)

    patron = patron_js(datos['js'])
    reemplazo = {e['es']: e[idioma] for e in datos['js']}
    salida = []
    for p in PARTES.split(s):
        if not p:
            continue
        if p.startswith('<!--') or p.startswith('<style'):
            salida.append(p)
        elif p.startswith('<script'):
            cab = re.match(r'<script\b[^>]*>', p).group(0)
            if 'application/ld+json' in cab:  # descripción para buscadores
                ld = lambda m: m.group(1) + json.dumps(traducir(json.loads(m.group(2))), ensure_ascii=False)
                p = re.sub(r'("description":\s*)("(?:[^"\\]|\\.)*")', ld, p)
                p = p.replace('"inLanguage":"es-UY"', f'"inLanguage":"{conf["formato"]}"')
            elif ' src=' not in cab and patron:
                cuerpo = p[len(cab):-len('</script>')]
                p = cab + patron.sub(lambda m: reemplazo[m.group(0)], cuerpo) + '</script>'
            p = re.sub(r'(\ssrc=")([^"]*)(")', lambda m: m.group(1) + absoluta(m.group(2)) + m.group(3), p)
            salida.append(p)
        elif p.startswith('<'):
            def atributo(m):
                return f' {m.group(1)}="{html.escape(traducir(html.unescape(m.group(2))), quote=True)}"'
            p = re.sub(r'\s(%s)="([^"]*)"' % '|'.join(map(re.escape, atributos)), atributo, p)
            if p.startswith('<meta') and re.search(r'name="description"|property="og:(title|description)"', p):
                p = re.sub(r'(content=")([^"]*)(")', lambda m: m.group(1) + html.escape(traducir(html.unescape(m.group(2))), quote=True) + m.group(3), p)
            p = re.sub(r'(\s(?:src|href|data-src)=")([^"]*)(")', lambda m: m.group(1) + absoluta(m.group(2)) + m.group(3), p)
            salida.append(p)
        else:
            salida.append(html.escape(traducir(html.unescape(p)), quote=False))
    s = ''.join(salida)
    if faltan:
        return None, faltan

    s = s.replace('<html lang="es-UY">', f'<html lang="{conf["lang"]}">', 1)
    if pagina == 'index':
        s = armar_index(s, idioma)
    if not s.startswith('<!doctype html>\n'):
        sys.exit(f'{PAGINAS[pagina]["fuente"]}: esperaba que empiece con <!doctype html>')
    return s.replace('\n', '\n' + AVISO.format(fuente=PAGINAS[pagina]['fuente']), 1), None


def armar_index(s, idioma):
    """Lo propio de la landing: dirección canónica, selector de idioma, tablero y prefijos del formulario."""
    conf = IDIOMAS[idioma]

    def una_vez(viejo, nuevo):
        nonlocal s
        if s.count(viejo) != 1:
            sys.exit(f'index.html: esperaba encontrar una vez: {viejo}')
        s = s.replace(viejo, nuevo)

    una_vez('<meta property="og:locale" content="es_UY">', f'<meta property="og:locale" content="{conf["locale"]}">')
    una_vez(f'<link rel="canonical" href="{SITIO}/">', f'<link rel="canonical" href="{SITIO}{conf["ruta"]}">')
    una_vez(f'<meta property="og:url" content="{SITIO}/">', f'<meta property="og:url" content="{SITIO}{conf["ruta"]}">')
    # Selector de idioma: se marca el idioma de esta página y el botón muestra su bandera
    s = s.replace('hreflang="es" lang="es" aria-current="page"', 'hreflang="es" lang="es"')
    s = s.replace(f'hreflang="{conf["lang"]}" lang="{conf["lang"]}"', f'hreflang="{conf["lang"]}" lang="{conf["lang"]}" aria-current="page"')
    una_vez('<use href="#f-uy"/></svg></span><span class="lang-code">ES</span>',
            f'<use href="#f-{conf["bandera"]}"/></svg></span><span class="lang-code">{idioma.upper()}</span>')
    # El tablero del supervisor y su foto (la del celular), en el idioma de la página
    una_vez('data-src="/tablero.html"', f'data-src="/tablero-{idioma}.html"')
    foto = f'tablero-foto-{idioma}.webp'
    if os.path.exists(os.path.join(RAIZ, foto)):
        una_vez('src="/tablero-foto.webp"', f'src="/{foto}"')
    else:
        print(f'Aviso: no está {foto}; /{idioma} usa la foto del tablero en español.')
    # Prefijos de WhatsApp: en orden alfabético del idioma y, en portugués, Brasil primero elegido
    m = re.search(r'(<select id="f-prefijo"[^>]*>)(.*?)(</select>)', s, re.S)
    opciones = re.findall(r'<option value="([^"]*)"( selected)?>([^<]*)</option>', m.group(2))
    clave = lambda o: re.sub(r'[^a-z ]', '', html.unescape(o[2]).lower().translate(str.maketrans('áéíóúâêôãõç', 'aeiouaeoaoc')))
    elegido = {'pt': '+55'}.get(idioma)
    lista = ''.join('<option value="%s"%s>%s</option>' % (v, ' selected' if (v == elegido if elegido else sel) else '', t)
                    for v, sel, t in sorted(opciones, key=clave))
    s = s[:m.start(2)] + lista + s[m.end(2):]
    return s


def main():
    pedidas = sys.argv[1:] or list(PAGINAS)
    for p in pedidas:
        if p not in PAGINAS:
            sys.exit(f'No conozco la página «{p}». Son: {", ".join(PAGINAS)}')
    problemas, resultados = [], {}
    for pagina in pedidas:
        datos = cargar(pagina)
        fuente = open(os.path.join(RAIZ, PAGINAS[pagina]['fuente']), encoding='utf-8').read()
        errores, faltan_js = revisar_js(fuente, datos)
        problemas += [f'{pagina}: {e}' for e in errores]
        problemas += [f'{pagina} (script): {t}' for t in faltan_js]
        faltan = set()
        for idioma in IDIOMAS:
            texto, falta = armar(pagina, idioma, datos, fuente)
            if falta:
                faltan |= falta
            else:
                resultados[PAGINAS[pagina]['salida'].format(idioma=idioma)] = texto
        problemas += [f'{pagina} (HTML): {t}' for t in sorted(faltan)]
    if problemas:
        print('Faltan traducciones (no se escribió nada):')
        for t in problemas:
            print('  ·', t)
        sys.exit(1)
    for ruta, texto in resultados.items():
        destino = os.path.join(RAIZ, ruta)
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        open(destino, 'w', encoding='utf-8').write(texto)
        print(f'{ruta} listo')


if __name__ == '__main__':
    main()
