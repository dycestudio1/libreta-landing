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

- **Contacto del formulario:** está en `var CONFIG` de `index.html` (WhatsApp y mail).
- **Datos de la demo:** son de ejemplo y están en el mismo archivo (`var CATALOGO`, `CLI`, `RUTA`, `OPS`, `VEND`, `RIESGO`, `PEDIDOS`, `SOL`).
- **Dominio:** si cambia, hay que actualizar `<link rel="canonical">`, `og:url` y `og:image`.
- **Marca:** colores Vereda `#0B6E7C` y Aviso `#FF6A3D`; letras Figtree e IBM Plex Mono.
- **Este repo es público:** no subas nada interno (precios en negociación, datos de clientes reales, credenciales).
