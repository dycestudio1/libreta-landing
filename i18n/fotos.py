# Saca las fotos del tablero que se ven en el celular: tablero-foto.webp, tablero-foto-pt.webp y tablero-foto-en.webp.
#
# Uso, desde la raíz del repo (después de python3 i18n/armar.py):   python3 i18n/fotos.py
#
# Captura cada tablero con Chrome sin ventana a 1440 × 860 (la medida en que se dibuja), en «Hoy» y sin el
# botón del asesor, y lo achica a 1200 × 717 en WebP. Necesita Google Chrome y Pillow (pip install pillow).
import os
import subprocess
import sys
import tempfile

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
CHROME = os.environ.get('CHROME', '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
FOTOS = {'tablero.html': 'tablero-foto.webp', 'tablero-pt.html': 'tablero-foto-pt.webp', 'tablero-en.html': 'tablero-foto-en.webp'}

for fuente, foto in FOTOS.items():
    html = open(os.path.join(RAIZ, fuente), encoding='utf-8').read()
    with tempfile.TemporaryDirectory() as tmp:
        copia = os.path.join(tmp, fuente)
        open(copia, 'w', encoding='utf-8').write(html.replace('</head>', '<style>.ase-btn{display:none!important}</style></head>', 1))
        png = os.path.join(tmp, 'captura.png')
        subprocess.run([CHROME, '--headless=new', '--hide-scrollbars', '--force-device-scale-factor=1', '--window-size=1440,860',
                        '--virtual-time-budget=5000', '--user-data-dir=' + os.path.join(tmp, 'perfil'), '--screenshot=' + png,
                        'file://' + copia], check=True, capture_output=True)
        imagen = Image.open(png).convert('RGB').resize((1200, 717), Image.LANCZOS)
        imagen.save(os.path.join(RAIZ, foto), 'WEBP', quality=82, method=6)
    print(f'{foto} listo')
sys.exit(0)
