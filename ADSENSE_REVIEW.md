# Revisión de contenido de Tarifa Pro

La versión anterior publicaba 1.500 combinaciones de oficio, país e intención con textos repetidos. Las cifras salían de tarifas base y multiplicadores fijos, sin un estudio de mercado. Además, el `docs` versionado conservaba afirmaciones de revisión por contadores y páginas legales prácticamente idénticas. Esos problemas se han retirado; ninguna prueba local permite garantizar una aprobación de AdSense.

## Resultado preparado

- Nueve guías educativas distintas con ejemplos hipotéticos y cuentas explícitas: tarifa por hora, web, video, identidad visual, campañas, redacción investigada, automatización, consultoría y verificación de impuestos en fuentes oficiales.
- Siete categorías con una plantilla propia de alcance, entregables, criterios de aceptación y procedimiento para cambios. Cada una enlaza su guía especializada.
- Calculadora con objetivo mensual igual al objetivo anual dividido entre doce, incluidas las vacaciones; entradas inválidas no producen una tarifa aparente.
- Presupuesto con moneda explícita, cantidades e impuestos validados, redondeo de cada línea a centavos y bloqueo de impresión con datos inválidos. El impuesto inicial es cero como campo pendiente de determinar, no una recomendación fiscal.
- 24 páginas indexables y 18 rutas de herramientas, guías y categorías en la búsqueda. Las 1.500 direcciones antiguas se conservan como avisos de retirada útiles, sin rangos, consejos fiscales, datos estructurados de artículo ni descubrimiento en búsqueda o sitemap. Mantener una URL no mantiene su antigua afirmación.
- Contacto privado por `mailto`, con explicación de que abre el correo. Se reutiliza `sabiasque496@gmail.com`, que el mismo propietario ya publicó en su sitio principal. Conviene confirmar que el buzón sigue atendido antes de publicar. GitHub Issues se reserva para reportes públicos sin información personal.
- Publicador identificado como el proyecto Tarifa Pro y su cuenta SSJ-ARIEL, sin inventar autores humanos, encuestas, revisiones de expertos o fechas de publicación.

## Recursos externos y revisión

En `data/site.json`, `adsense.enabled`, `analytics.enabled` y `consent.configured` son `false`. No se cargan scripts de anuncios, analítica ni CookieYes durante esta revisión. Se preservan el identificador del publicador, los metadatos de propiedad, la verificación de Search Console y `ads.txt`.

Antes de reactivar estos recursos, hay que comprobar en la configuración real de la CMP qué servicios y finalidades controla, probar aceptación, rechazo y cambio de preferencias, y actualizar privacidad y cookies con el comportamiento efectivo. Una URL de CookieYes, por sí sola, no demuestra que el consentimiento esté configurado. Los avisos antiguos y las páginas administrativas siguen excluidos del código de anuncios aunque se habilite publicidad. La validación actual bloquea la introducción de cargadores externos; su contrato deberá revisarse junto con la activación comprobada.

Las direcciones de este proyecto son `https://ssj-ariel.github.io/TARIFAPRO/`. GitHub Pages utiliza el archivo `robots.txt` y `ads.txt` del dominio raíz para operaciones del dominio; hay que conservar y comprobar también los archivos correspondientes del sitio principal. La revisión de AdSense de `ssj-ariel.github.io` incluye la calidad del sitio publicado en ese dominio, no solo esta sección.

## Validación y publicación

Python 3.12 y Node 20 bastan para generar y verificar el sitio:

```sh
python scripts/build.py
python scripts/validate_quality.py
node scripts/test_tools.js
```

Las comprobaciones validan las 1.524 páginas resultantes, el sitemap, la búsqueda, los enlaces locales, la retirada de la matriz sin fuentes y la conservación de la propiedad. Los casos de cálculo comprueban los ejemplos de la guía, el equilibrio entre objetivo anual y mensual, la precisión por línea y las entradas inválidas. Ambas acciones de GitHub ejecutan las comprobaciones antes de publicar el artefacto generado.

También se ejecutó una prueba real en Chromium con escritorio y móvil, con y sin JavaScript: 64 comprobaciones de páginas y flujos, sin errores de aplicación, recursos fallidos ni solicitudes a terceros. Incluyó cálculo, cambio de moneda, errores, filas de presupuesto y estilos de impresión. La prueba de impresión revisa estilos; no acredita cómo cada dispositivo imprimirá un documento largo.

Después de publicar una versión revisada, comprueba las páginas del dominio real y solicita una nueva revisión desde AdSense. Las páginas retiradas pueden seguir apareciendo temporalmente en Google hasta que se rastreen de nuevo. `noindex` limita su indexación; la mejora de valor consiste en retirar sus afirmaciones y ofrecer herramientas y guías útiles, no en añadir una etiqueta. La decisión final y su plazo corresponden a Google.
