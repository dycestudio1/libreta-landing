# Landing de Libreta

La página de **https://libreta.dev**. Es HTML estático: todo el CSS y el JavaScript están dentro de `index.html`.

## Cómo se publica

Cada cambio que entra a `main` se publica solo en libreta.dev a los pocos segundos (Vercel). Un cambio en otra rama genera una vista previa con su propio link, sin tocar la página publicada.

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | La landing completa, con la demo del celular |
| `tablero.html` | El tablero del supervisor que se ve dentro de la página (iframe). Se comunica con `index.html` por `postMessage`: el contrato está al principio del archivo |
| `favicon.svg`, `favicon-32.png`, `apple-touch-icon.png` | Íconos |
| `og-image.png` | La imagen al compartir el link (1200 × 630) |
| `vercel.json` | Encabezados y caché de los íconos |

## Antes de cambiar

- **Pedir una demo:** el formulario pide nombre, empresa, mail, vendedores en la calle y WhatsApp (opcional, con el prefijo de los países de LATAM y España; Uruguay por defecto) y abre adentro de la página la agenda de Calendly de D&C (`calendly.com/dearmascostantini/30min`, la misma de dearmascostantini.com). Calendly recibe el nombre con la empresa, el mail, `a1` con el motivo y `a2` con la empresa. La dirección está en `var CONFIG` de `index.html`. La página no muestra ningún mail.
- **Login:** el botón a la derecha de «Pedir una demo» y el link del pie llevan a `https://app.libreta.dev/login`, el ingreso de la app. Funciona cuando la app esté publicada ahí.
- **Tablero:** tiene la misma medida que el de la landing de Rondín. Se dibuja en 1440 × 860 y `escalarTablero` lo achica hasta 0,7 con el texto al costado (desde 1200 px de ancho) y 0,62 debajo; en el celular va a todo el ancho, con 820 px de alto.
- **Ancho:** el contenido ocupa toda la pantalla, con un margen de 3,3 % a cada lado (entre 16 y 64 px), hasta 2368 px. Debajo de 1100 px los links del menú se esconden y quedan los botones.
- **Datos de la demo:** son de ejemplo y están en el mismo archivo (`var CATALOGO`, `CLI`, `RUTA`, `OPS`, `VEND`, `RIESGO`, `PEDIDOS`, `SOL`).
- **Dominio:** si cambia, hay que actualizar `<link rel="canonical">`, `og:url` y `og:image` (hoy `https://www.libreta.dev/`, porque libreta.dev redirige a www).
- **Marca:** colores Vereda `#0B6E7C` y Aviso `#FF6A3D`; letras Figtree e IBM Plex Mono.
- **Este repo es público:** no subas nada interno (precios en negociación, datos de clientes reales, credenciales).
