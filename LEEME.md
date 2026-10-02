# Landing de Libreta

Sitio de una sola página, listo para publicar en cualquier hosting estático (Vercel, Netlify, el hosting de D&C). Todo el CSS y el JavaScript están dentro de `index.html`; lo único externo son las tipografías de Google Fonts (Figtree, IBM Plex Mono y DM Sans para el «&»).

## Archivos

| Archivo | Para qué |
|---|---|
| `index.html` | La landing completa |
| `favicon.svg`, `favicon-32.png` | Ícono de la pestaña del navegador |
| `apple-touch-icon.png` | Ícono cuando se guarda en la pantalla de inicio del celular |
| `og-image.png` | Imagen que aparece al compartir el link en WhatsApp, LinkedIn o redes (1200 × 630) |

Para mandar la página por WhatsApp o por mail está `Libreta_para_Gian/3_Landing/Libreta_Landing_un_archivo.html` (fuera del repo): la misma página en un solo archivo, con los íconos adentro. Se ve completa en la compu y en Android. En iPhone, WhatsApp la abre como vista previa y ahí la demo puede no funcionar; para eso conviene publicarla y mandar el link. El logo en todas sus versiones está en `docs/marca/logo/`.

## Qué tiene

- **Frase:** «Tu libreta ya sabe qué venderle a cada uno. Vos solo vendés.», en la misma línea que Tildalo, Vuelta y Encargue. Alternativas para charlar: «Cada cliente con su motivo. Vos solo vendés.» o «La calle, ordenada. Vos solo vendés.».
- **Demo interactiva en un celular (la app de María Fernández, vendedora de Distribuidora Central).** Todas las pestañas funcionan:
  - **Hoy:** saludo, botón Iniciar / Terminar jornada (con el resumen que le llega a Laura), comisión del mes, avance contra el objetivo, la ruta del día paso a paso, oportunidades y las tareas que dejó la supervisora (se tildan).
  - **Ruta:** mapa con las 5 paradas y la lista. Cada parada abre una hoja con «Llegué», «Cargar pedido», «Visita hecha» o «Con problema» (el motivo va al panel). Abajo: «Visita fuera de ruta» (suma un cliente cercano) y «Avisar desvío» (llega a Solicitudes del panel; si nadie lo aprueba, Laura lo aprueba sola a los 9 segundos y le llega el aviso al celular).
  - **Pedido (botón + del medio):** elegir cliente, productos sugeridos para ese cliente (venta cruzada, recompra, lo de siempre), lista de precios con buscador y categorías, cantidades, revisión con nota para el depósito y envío. Al enviar: la visita queda hecha, la oportunidad pasa a «vendida», sube la comisión en Hoy, el pedido aparece en el panel («Recién llegado» y a los segundos «En Doria») y en la pestaña «El pedido entra solo» de Cómo funciona.
  - **Oportunidades:** los cuatro tipos (Recompra, Venta cruzada, Reactivar, Cobrar) con filtro, valor estimado por mes y botones «Ya se lo ofrecí» / «No le interesa» (con Deshacer), «Registrar cobro» y «Cargar pedido».
  - **Cartera y ficha:** buscador y filtros; la ficha tiene evolución de 12 meses, qué día compra, cómo viene el ticket, compras por familia (con «Dejó de llevarlo»), cuenta con facturas y saldo, y notas que se pueden agregar.
  - Abajo del celular, los 5 pasos (Jornada, Ruta, Oportunidad, Pedido, Ficha) para saltar directo.
- **Funciona con:** carrusel discreto con Doria, Zureo, Odoo, SAP Business One, Memory, GNS y Excel o Google Sheets, como texto en gris.
- **Cómo funciona:** cinco pestañas (lee tu sistema; encuentra qué venderle, con el «por qué» de cada tipo de oportunidad; el pedido como lo recibe el sistema; la bandeja de solicitudes con Aprobar / Rechazar; el asistente que pide confirmación antes de crear una tarea). Se abren directo con `#sistema`, `#oportunidades`, `#pedido`, `#solicitudes` o `#asistente`. Si en el asistente se confirma la tarea, le aparece a María en el celular.
- **Panel del supervisor:** mini panel funcionando adentro de una ventana: Resumen (venta neta contra objetivo, contra el año pasado, clientes activos y nuevos, a cobrar, venta por vendedor, oportunidades), Vendedores, Clientes en riesgo («Pedir visita»), Pedidos y Solicitudes. Filtra por vendedor y por mes. En el celular se ve apilado.
- **Cuánto suma:** calculadora con vendedores, clientes por vendedor, compra promedio y de dónde parten. Está presentada como estimación, con los supuestos a la vista. Debajo, cuatro beneficios sin números inventados.
- **Precios** con opción mensual o anual, **preguntas** y **formulario para pedir una demo** que abre WhatsApp. No hay prueba gratis ni programa Fundadores. No hay testimonios.

## Antes de publicar

1. **Precios (confirmados el 01/10/2026).** Calle USD 69, Equipo USD 59 y Fuerza de ventas USD 49 por vendedor activo por mes; el anual se paga 10 meses (690 / 590 / 490). Instalación USD 690 con planilla, USD 1.950 con integración completa y desde USD 2.500 a medida. El asistente por WhatsApp no está incluido en ningún plan. Se cambian en el HTML (`data-precio`, `data-anual` y el bloque `.instalacion`) y en `planDe()` de la calculadora.
2. **WhatsApp del formulario.** En `index.html`, buscá `var CONFIG` y completá `whatsapp` con el número en formato internacional, sin `+` ni espacios (ej.: `59899123456`). Mientras esté vacío, el formulario arma un mail a `hola@dearmascostantini.com`.
3. **Guardar cada contacto (opcional).** Si querés una copia de cada pedido de demo además del WhatsApp, creá un formulario en Formspree o Basin y pegá su URL en `formEndpoint`.
4. **Datos de la demo.** Catálogo, clientes, ruta, oportunidades, vendedores, clientes en riesgo, pedidos y solicitudes están en `var CATALOGO`, `CLI`, `RUTA`, `OPS`, `VEND`, `RIESGO`, `PEDIDOS` y `SOL`. Son de ejemplo, como los de la app en modo demo.
5. **Calculadora.** Supone que las oportunidades concretadas suman 3 %, 2 % o 1 % a lo que ya compra la cartera (según «De memoria», «Planilla» o «Con datos»), dólar a $U 40 y margen bruto de 20 %. Están en `data-extra`, `TC` y `MARGEN`. Conviene ajustarlos cuando haya resultados medidos de un cliente real.
6. **Dominio.** La página asume `https://libreta.uy/` (no verificamos que esté libre). Si es otro, cambialo en `<link rel="canonical">`, `og:url`, `og:image` y en la barra del panel (`app.libreta.uy`).
7. **Afirmaciones a revisar.** Las preguntas dicen que hoy hay conexión directa con Doria (es la que ya funciona en la app) y que la instalación tarda de dos a cuatro semanas. Si cambia, corregirlo en la sección Preguntas.
8. **Medición.** Pegá el código de Google Analytics 4 o Google Tag Manager, y el Meta Pixel si se va a pautar, en el `<head>`. La página ya manda estos eventos al `dataLayer`:
   - Botones: `cta_barra`, `cta_hero`, `cta_demo`, `cta_plan_calle`, `cta_plan_equipo`, `cta_plan_fuerza`, `cta_fijo_movil`.
   - Demo: `demo_jornada` (con `accion`), `demo_parada`, `demo_llegada`, `demo_desvio`, `demo_oportunidad` (con `tipo` y `estado`), `demo_ficha`, `demo_pedido_abrir`, `demo_pedido_enviado` (con `renglones` y `total`), `demo_paso`.
   - Cómo funciona: `como_pestana`, `como_tipo`, `asistente_pregunta`, `asistente_confirmacion`.
   - Panel: `panel_seccion`, `panel_periodo`, `panel_vendedor`, `panel_pedir_visita`, `panel_solicitud`.
   - Otros: `precios_periodo`, `lead_enviar` (con `sistema` y `vendedores`).

## Cómo publicarla

- **Vercel:** en vercel.com/new, arrastrá esta carpeta. Después, en Settings → Domains, sumá el dominio.
- **Netlify:** en app.netlify.com/drop, arrastrá esta carpeta.
- **Otro hosting:** subí los archivos a la raíz del dominio.

## Marcas de terceros

Doria, Zureo, Odoo, SAP Business One, Memory, GNS, Excel, Google Sheets y WhatsApp se nombran como texto, sin logos. Si más adelante se usan sus logos, conviene pedir autorización a cada empresa.
