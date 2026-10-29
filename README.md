# Landing de Libreta

La página de **https://libreta.dev**. Es HTML estático: todo el CSS y el JavaScript están dentro de `index.html`.

Está en español (`/`), portugués de Brasil (`/pt`) e inglés (`/en`). **El español es la única versión que se edita a mano**: las otras dos se generan (ver [Idiomas](#idiomas)).

## Cómo se publica

Cada cambio que entra a `main` se publica solo en libreta.dev a los pocos segundos (Vercel). Un cambio en otra rama genera una vista previa con su propio link, sin tocar la página publicada.

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | La landing completa, con la demo del celular (en español) |
| `pt/index.html`, `en/index.html` | La landing en portugués y en inglés. **Se generan con `i18n/armar.py`: no se editan a mano** |
| `tablero.html` | El tablero del supervisor que se ve dentro de la página (iframe). Se comunica con `index.html` por `postMessage`: el contrato está al principio del archivo |
| `tablero-pt.html`, `tablero-en.html` | El tablero en portugués y en inglés, el que cargan `/pt` y `/en`. También se generan con `i18n/armar.py` |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Íconos |
| `og-image.png` | La imagen al compartir el link (1200 × 630) |
| `tablero-foto.webp`, `tablero-foto-pt.webp`, `tablero-foto-en.webp` | La imagen del tablero que se ve en el celular, en lugar del interactivo, en cada idioma. Se sacan con `i18n/fotos.py` |
| `i18n/` | Las traducciones y los scripts que arman `/pt` y `/en` (no se publica) |
| `privacidad.html`, `soporte.html`, `eliminar-cuenta.html`, `legal.css` | Las páginas que piden las tiendas de apps (solo en español) |
| `vercel.json` | Direcciones limpias, encabezados y caché de los íconos |

## Antes de cambiar

- **Pedir una demo:** el formulario pide nombre, empresa, mail, vendedores en la calle y WhatsApp (opcional, con el prefijo de los países de LATAM y España; Uruguay por defecto) y abre adentro de la página la agenda de Calendly de D&C (`calendly.com/dearmascostantini/30min`, la misma de dearmascostantini.com). Calendly recibe el nombre con la empresa, el mail, `a1` con el motivo y `a2` con la empresa. La dirección está en `var CONFIG` de `index.html`. La página no muestra ningún mail.
- **Login:** el botón a la derecha de «Pedir una demo» y el link del pie llevan a `https://app.libreta.dev/login`, el ingreso de la app. Funciona cuando la app esté publicada ahí.
- **Tablero:** tiene la misma medida que el de la landing de Rondín. Se dibuja en 1440 × 860 y `escalarTablero` lo achica hasta 0,7 con el texto al costado (desde 1200 px de ancho) y 0,62 debajo. **En el celular (hasta 800 px) se ve `tablero-foto.webp`** (el tablero en «Hoy», 1200 × 717) y el interactivo no se carga: el iframe tiene `data-src` y se carga solo en pantallas grandes. Si cambia el tablero, hay que volver a sacar las fotos: `python3 i18n/fotos.py` (después de `armar.py`).
- **Ancho:** el contenido ocupa toda la pantalla, con un margen de 3,3 % a cada lado (entre 16 y 64 px), hasta 2368 px. Debajo de 1100 px los links del menú se esconden y quedan los botones.
- **Datos de la demo:** son de ejemplo y están en el mismo archivo (`var CATALOGO`, `CLI`, `RUTA`, `OPS`, `VEND`, `RIESGO`, `PEDIDOS`, `SOL`).
- **Dominio:** si cambia, hay que actualizar `<link rel="canonical">`, `og:url` y `og:image` (hoy `https://www.libreta.dev/`, porque libreta.dev redirige a www).
- **Marca:** colores Vereda `#0B6E7C` y Aviso `#FF6A3D`; letras Figtree e IBM Plex Mono.
- **Este repo es público:** no subas nada interno (precios en negociación, datos de clientes reales, credenciales).

## Idiomas

`index.html` y `tablero.html` están en español y son las únicas fuentes que se editan. `i18n/armar.py` arma las versiones en portugués y en inglés con las traducciones de `i18n/textos.json` (la landing) e `i18n/tablero.json` (el tablero):

```
python3 i18n/armar.py            # escribe pt/index.html, en/index.html, tablero-pt.html y tablero-en.html
python3 i18n/armar.py tablero    # una sola página (index o tablero)
python3 i18n/extraer.py          # lista lo que falta traducir de la landing (o: extraer.py tablero)
```

**Cada vez que cambia un texto en español hay que correr `armar.py` y subir también los archivos generados.** Si hay un texto sin traducción, o una traducción cuyo texto ya no está, lo lista y no escribe nada: se agrega en el JSON y se vuelve a correr.

En cada JSON:

- `textos`: los textos del HTML (nodos de texto, `alt`, `aria-label`, `placeholder`, `title`, el título y las descripciones), con `es`, `pt` y `en`.
- `js`: los textos de los `<script>`. Se reemplazan tal cual y solo dentro de los scripts, así que el `es` es el pedazo exacto del código (puede llevar comillas y un poco de código alrededor cuando la frase cambia de orden en otro idioma). Un reemplazo cambia todas las apariciones, así que si un texto se usa también como clave (categorías, estados) queda igual en todos lados.
- `iguales` y `js_iguales`: lo que no se traduce (Libreta, D&C, nombres de clientes, personas, calles y barrios de los datos de ejemplo, sistemas como Doria o SAP).
- `fragmentos`: reemplazos crudos por idioma, por si hace falta algo que no es un texto.

Además, `armar.py` cambia `lang`, `og:locale`, la dirección canónica y `og:url`, el idioma del JSON-LD, marca el idioma en el selector, carga `tablero-pt.html` / `tablero-en.html` y su foto, y ordena los prefijos de WhatsApp en el idioma (en portugués, Brasil queda elegido). Los datos de ejemplo siguen en pesos uruguayos ($U) y los precios de Libreta en dólares; los números y las fechas van con el formato de cada idioma (en inglés, 1,234.5 y mes/día).

**Selector de idioma:** en el encabezado, un botón con la bandera y el código del idioma despliega Español, Português e English (desde 761 px; en el celular está en el menú). En el menú del celular y en el pie están las tres banderas. Al cambiar, la página abre en la misma sección. Las páginas legales quedan en español.

**Chat:** desde `/pt` y `/en` el chat manda `idioma: 'pt'` o `'en'` junto con la conversación (y cada idioma guarda su propia conversación). Para que el asistente conteste en ese idioma desde el primer mensaje, la API (`/api/chat/libreta` del Sistema D&C) tiene que leer ese campo, como ya hace el chat de dearmascostantini.com.
