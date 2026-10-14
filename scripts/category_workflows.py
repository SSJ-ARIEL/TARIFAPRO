"""Distinct scope checklists for the seven budgeting workflows."""

CATEGORY_WORKFLOWS = {
    "desarrollo-web": {
        "guide": "presupuestar-pagina-web-alcance",
        "rows": [
            ("Estructura", "Lista de secciones, plantillas e idiomas", "Mapa aprobado y textos identificados por página"),
            ("Integraciones", "Formularios, correos y servicios acordados", "Caso de prueba de envío y de error para cada servicio"),
            ("Diseño", "Versiones de escritorio y pantalla pequeña", "Aprobación del diseño antes de construir nuevas funciones"),
            ("Publicación", "Dominio, alojamiento y entrega de accesos", "Responsable del pago y prueba del dominio final"),
            ("Mantenimiento", "Período de soporte y tareas incluidas", "Diferencia escrita entre corregir un fallo y añadir una función"),
        ],
        "change": "Si una web informativa pasa a necesitar reservas, usuarios o cobros, pide los flujos y sistemas implicados antes de estimar la ampliación. El número de páginas no describe esos cambios: hay que probar permisos, estados y fallos de los servicios.",
        "brief": "La propuesta debe permitir a otra persona enumerar lo que recibirá. Escribe quién facilita contenidos y accesos, cuándo deben estar listos y cómo se enviarán las correcciones. Aclara si la publicación depende de un proveedor de formulario o alojamiento. El soporte posterior tiene su propio alcance; evita prometer mantenimiento indefinido dentro del precio de construcción.",
    },
    "diseno-multimedia": {
        "guide": "presupuestar-identidad-visual-alcance",
        "rows": [
            ("Exploración", "Brief, referencias y propuestas iniciales", "Cantidad de direcciones visuales que se presentarán"),
            ("Identidad", "Logotipo y variantes acordadas", "Listado de usos y versiones a color y monocromas"),
            ("Aplicaciones", "Piezas concretas para los canales elegidos", "Medidas, proporciones y formatos por pieza"),
            ("Archivos", "Exportaciones y editables pactados", "Inventario de archivos y software necesario para abrirlos"),
            ("Recursos", "Tipografías, imágenes y licencias", "Quién compra cada licencia y quién podrá utilizarla"),
        ],
        "change": "Una nueva propuesta completa después de aprobar una dirección visual no es lo mismo que ajustar espaciado o color. Define qué constituye una ronda de comentarios, quién consolida las decisiones y cuándo un cambio requiere otra propuesta.",
        "brief": "Un presupuesto de identidad visual comienza por dónde se utilizará la marca. Pregunta si habrá impresión, redes, envases o interfaces; cada soporte puede requerir archivos y comprobaciones diferentes. La entrega de editables y las licencias de terceros deben quedar expresadas. No presupongas que pagar una pieza da acceso ilimitado a cualquier tipografía o fotografía utilizada.",
    },
    "marketing-digital": {
        "guide": "cotizar-gestion-campanas-publicidad",
        "rows": [
            ("Preparación", "Accesos y comprobación de medición", "Cuenta autorizada y eventos que se pueden observar"),
            ("Creatividades", "Cantidad de textos y piezas", "Responsable de producción y aprobación de cada versión"),
            ("Gestión", "Campañas, canales y cadencia de cambios", "Número de campañas cubiertas y límites de atención"),
            ("Inversión", "Dinero que se paga a la plataforma", "Presupuesto autorizado, separado del honorario"),
            ("Informes", "Resumen de resultados y decisiones", "Métricas, período, fuente y limitaciones de atribución"),
        ],
        "change": "Añadir otro canal, producir una página de destino o crear diez piezas nuevas puede ampliar el trabajo aunque la inversión publicitaria no cambie. Describe el servicio adicional y quién lo aprueba antes de ejecutarlo.",
        "brief": "Define el objetivo de la campaña y la evidencia disponible antes de presentar resultados esperados. Un honorario de gestión cubre tareas acordadas; no equivale al dinero destinado a anuncios. La disponibilidad de medición depende del sitio, de permisos y de las plataformas. Presenta observaciones comprobables y evita garantizar ventas o conversiones que el servicio por sí solo no controla.",
    },
    "video-animacion": {
        "guide": "cotizar-edicion-video-entregables",
        "rows": [
            ("Entrada", "Horas de material y formatos de origen", "Archivos legibles, audio disponible y respaldo acordado"),
            ("Montaje", "Duración final y estructura narrativa", "Referencia de estilo y criterio de aprobación del primer corte"),
            ("Audio y texto", "Limpieza, música y subtítulos", "Idioma, permisos y tipo de archivo de subtítulos"),
            ("Versiones", "Resoluciones, proporciones y duraciones", "Inventario de exportaciones con nombres y formatos"),
            ("Correcciones", "Rondas sobre el corte aprobado", "Comentarios consolidados y límite para reemplazar material"),
        ],
        "change": "Rehacer el guion o sustituir todas las entrevistas después de aprobar el montaje modifica la selección, los subtítulos y el audio. Presupuesta esas tareas por separado; una exportación adicional y un montaje nuevo tienen esfuerzos distintos.",
        "brief": "Pide una muestra del material antes de estimar el tiempo. La duración final no explica cuántas horas habrá que revisar ni qué problemas de audio pueden aparecer. Acuerda el destino del video, la resolución y si se necesitan subtítulos incrustados o separados. Registra quién aporta recursos autorizados y cuánto tiempo conservarás los archivos del proyecto.",
    },
    "redaccion-copywriting": {
        "guide": "presupuestar-redaccion-investigacion",
        "rows": [
            ("Brief", "Audiencia, finalidad y canal", "Pregunta que el texto debe responder y tono acordado"),
            ("Investigación", "Fuentes y entrevistas previstas", "Acceso a documentación y responsables de resolver dudas"),
            ("Borrador", "Piezas y extensión aproximada", "Estructura aprobada y criterios de exactitud"),
            ("Edición", "Correcciones y revisión técnica", "Número de rondas y persona que confirma los datos"),
            ("Entrega", "Archivo final y elementos de publicación", "Definir si incluye CMS, metadatos, imágenes o solo texto"),
        ],
        "change": "Cambiar la audiencia, pedir una entrevista adicional o convertir un artículo en una secuencia de correos crea trabajo nuevo. La longitud puede permanecer igual mientras cambia toda la investigación. Describe la nueva tarea antes de volver a redactar.",
        "brief": "Pregunta qué información existe y qué datos necesitan verificación. Separa escribir un borrador de investigar, entrevistar, editar e incorporar comentarios. Aclara quién revisará afirmaciones técnicas y quién autoriza las citas. Los plazos deben considerar respuestas de entrevistados y aprobaciones del cliente. Un recuento de palabras sirve para delimitar una entrega, pero no mide por sí solo su dificultad.",
    },
    "ia-automatizacion": {
        "guide": "cotizar-automatizacion-pruebas-soporte",
        "rows": [
            ("Proceso", "Flujo actual y resultado esperado", "Ejemplos de entrada y salida que el cliente puede revisar"),
            ("Acceso", "Sistemas, cuentas y permisos", "Cuenta de prueba y autorización de cada integración"),
            ("Datos", "Campos, volumen y excepciones", "Qué datos se necesitan y cuáles deben excluirse"),
            ("Pruebas", "Casos normales y fallos", "Duplicados, límites, reintentos y retorno al proceso manual"),
            ("Operación", "Suscripciones, consumo y soporte", "Quién paga proveedores y quién recibe alertas"),
        ],
        "change": "Añadir otro origen de datos o permitir que el sistema actúe sin revisión cambia permisos y pruebas, además de la configuración. Detalla esos cambios y el límite de consumo. Una demostración con pocos registros no prueba un flujo de producción completo.",
        "brief": "Presupuesta el resultado del proceso, no solo una conexión entre aplicaciones. Pide ejemplos que incluyan errores y excepciones; acuerda qué tareas requieren revisión humana. Distingue la construcción inicial del consumo recurrente y del soporte. El proveedor puede cambiar su API o límites: registra cómo se detectarán fallos y cómo continuará el negocio si el flujo se detiene.",
    },
    "consultoria-negocios": {
        "guide": "presupuestar-consultoria-diagnostico",
        "rows": [
            ("Pregunta", "Decisión concreta que se quiere informar", "Problema y alcance de la investigación por escrito"),
            ("Evidencia", "Documentación y datos del cliente", "Disponibilidad, período y limitaciones conocidas"),
            ("Entrevistas", "Personas y reuniones previstas", "Agenda, duración y acceso a interlocutores"),
            ("Diagnóstico", "Hallazgos, opciones y supuestos", "Diferenciar lo observado de lo estimado"),
            ("Seguimiento", "Sesión de entrega y aclaraciones", "Plazo y número de preguntas cubiertas después del informe"),
        ],
        "change": "Pasar de un diagnóstico a implementar un sistema, negociar contratos o dirigir equipos amplía la responsabilidad y los entregables. No lo incluyas implícitamente en una sesión de seguimiento; redacta un alcance nuevo con sus dependencias.",
        "brief": "Una propuesta útil define la pregunta que se investigará y qué decisión ayudará a tomar el informe. Especifica datos disponibles, entrevistas y sesiones. Registra las limitaciones de evidencia y quién valida los supuestos. Separa recomendaciones de acciones aprobadas: el consultor puede presentar opciones, pero no controla por sí solo el resultado económico de decisiones posteriores.",
    },
}
