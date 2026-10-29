# Lista lo que falta traducir de una página, listo para completar en su JSON.
#
# Uso, desde la raíz del repo:
#   python3 i18n/extraer.py              la landing (index.html → i18n/textos.json)
#   python3 i18n/extraer.py tablero      el tablero (tablero.html → i18n/tablero.json)
#   python3 i18n/extraer.py tablero --todo   todos los textos, también los que ya tienen traducción
#
# Saca los textos del HTML (nodos de texto, atributos, <title> y descripciones) y los strings de los
# <script> que parecen texto visible. Los de los scripts salen limpios (sin etiquetas): en el JSON va
# el pedazo exacto del código que se reemplaza, que puede incluir comillas o partes de etiquetas.
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from armar import ATRIBUTOS, LETRAS, PAGINAS, PARTES, RAIZ, cargar, limpio, literales, normal, parece_texto, revisar_js, scripts

pagina = next((a for a in sys.argv[1:] if not a.startswith('--')), 'index')
todo = '--todo' in sys.argv
datos = cargar(pagina)
fuente = open(os.path.join(RAIZ, PAGINAS[pagina]['fuente']), encoding='utf-8').read()
hechos = {normal(t['es']) for t in datos['textos']} | set(datos['iguales'])
atributos = ATRIBUTOS + tuple(datos['atributos'])

textos = []
def agregar(t):
    t = normal(html.unescape(t))
    if t and re.search('[%s]' % LETRAS, t) and t not in textos and (todo or t not in hechos):
        textos.append(t)

for p in PARTES.split(fuente):
    if not p or p.startswith('<!--') or p.startswith('<script') or p.startswith('<style'):
        continue
    if p.startswith('<'):
        for a in atributos:
            for m in re.finditer(r'\s%s="([^"]*)"' % re.escape(a), p):
                agregar(m.group(1))
        if p.startswith('<meta') and re.search(r'name="description"|property="og:(title|description)"', p):
            agregar(re.search(r'content="([^"]*)"', p).group(1))
    else:
        agregar(p)

if todo:
    codigo = ''.join(fuente[a:b] for a, b in scripts(fuente))
    js = []
    for _, _, c in literales(codigo):
        t = limpio(c)
        if parece_texto(t) and t not in js:
            js.append(t)
    errores = []
else:
    errores, js = revisar_js(fuente, datos)

json.dump({'html': textos, 'js': js, 'errores': errores}, sys.stdout, ensure_ascii=False, indent=1)
print()
