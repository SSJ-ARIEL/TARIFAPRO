"""Guías originales y manualmente redactadas, con ejemplos hipotéticos comprobables.

No contienen cotizaciones del mercado, estadísticas no verificadas ni consejos fiscales.
Cada ejemplo usa una tarea distinta y hace visible la fórmula o alcance.
"""

GUIDES = [
    {
        "slug": "calcular-tarifa-hora-freelance",
        "title": "Cómo calcular tu tarifa freelance con horas facturables reales",
        "description": "Ejemplo paso a paso para estimar una tarifa por hora con gastos, vacaciones, ahorro e impuestos hipotéticos, sin confundir horas trabajadas y horas facturables.",
        "summary": "Calcula un punto de partida con un caso de números transparentes y comprueba qué cambia cuando tienes menos horas que vender.",
        "html": """
        <h2>El problema: no todas las horas de trabajo se pueden cobrar</h2>
        <p>Preparar propuestas, contestar consultas, revisar facturas y organizar archivos requiere tiempo, pero no siempre genera una factura. Por eso, dividir los gastos entre cuarenta horas semanales puede hacerte creer que tienes más capacidad de facturación de la que realmente tienes. La distinción útil es entre horas disponibles y horas que esperas cobrar.</p>
        <p>Antes de empezar, anota por separado los costos del negocio, los gastos personales que quieras cubrir y cualquier reserva para meses con poca actividad. No son estadísticas del mercado: son tus propios números. Para mostrar el método, usaremos un caso <strong>totalmente hipotético</strong>.</p>
        <h2>Ejemplo: una persona que factura 20 horas a la semana</h2>
        <table class="invoice-table"><thead><tr><th>Dato elegido</th><th>Valor hipotético</th></tr></thead><tbody>
        <tr><td>Gastos personales mensuales</td><td>1.000 unidades monetarias</td></tr>
        <tr><td>Herramientas y costos mensuales del negocio</td><td>200 unidades monetarias</td></tr>
        <tr><td>Horas que se podrán facturar por semana</td><td>20</td></tr>
        <tr><td>Descanso en el año</td><td>4 semanas</td></tr>
        <tr><td>Reserva o ahorro que se desea añadir</td><td>15 %</td></tr>
        <tr><td>Porcentaje ilustrativo usado solo para el cálculo</td><td>10 %</td></tr></tbody></table>
        <h3>Paso 1: determina tus horas de cobro anuales</h3>
        <p>El año tiene 52 semanas. Restamos cuatro de descanso y multiplicamos por 20 horas facturables: <strong>(52 − 4) × 20 = 960 horas</strong>. Una semana puede implicar más horas reales de trabajo, pero las tareas internas no deben confundirse con las horas que puedes facturar.</p>
        <h3>Paso 2: calcula el objetivo anual</h3>
        <p>Los gastos son 1.200 por mes. En doce meses equivalen a <strong>14.400</strong>. Si a ese total añades una reserva del 15 %, el objetivo neto ilustrativo es <strong>16.560</strong>. En este ejemplo matemático, si supones un 10 % de impuestos sobre lo facturado, el objetivo bruto queda en <strong>16.560 ÷ 0,90 = 18.400</strong>. El 10 % no representa un impuesto real ni sirve para decidir obligaciones tributarias.</p>
        <h3>Paso 3: divide el objetivo entre las horas facturables</h3>
        <p><strong>18.400 ÷ 960 = 19,17 por hora</strong>, redondeado a dos decimales. Ese resultado no es una tarifa oficial ni la cantidad que un cliente aceptará: es una referencia interna para comprobar si un proyecto ayuda a cubrir los costos elegidos. Una jornada completa de ocho horas equivaldría a 153,33 aproximadamente, antes de negociar alcance, imprevistos o condiciones.</p>
        <h2>Prueba de sensibilidad: ¿y si no consigues vender 20 horas?</h2>
        <p>Manteniendo el mismo objetivo bruto de 18.400, con 15 horas facturables semanales solo tienes 720 horas al año: el resultado es <strong>25,56 por hora</strong>. Con 25 horas semanales, tienes 1.200 horas: <strong>15,33 por hora</strong>. Esa comparación muestra por qué no basta con escoger un precio por intuición: el número de horas vendibles cambia toda la cuenta.</p>
        <h2>Errores que puedes detectar antes de enviar una propuesta</h2>
        <ul><li><strong>Ignorar reuniones y revisiones:</strong> reserva tiempo para tareas que el cliente sí exige, aunque no produzcan el entregable final.</li>
        <li><strong>Contar semanas de vacaciones como semanas facturables:</strong> ajusta el calendario con tu disponibilidad real.</li>
        <li><strong>Confundir la moneda con la conversión:</strong> cambiar el símbolo en la calculadora no transforma cantidades entre países.</li>
        <li><strong>Tratar un impuesto ilustrativo como obligatorio:</strong> el régimen fiscal depende de la jurisdicción, la actividad y tu situación; confírmalo con fuentes oficiales.</li>
        <li><strong>Interpretar el resultado como precio de mercado:</strong> valida alcance, entregables, demanda y propuestas comparables de tu nicho.</li></ul>
        <h2>Cómo usar el resultado sin perder el control</h2>
        <p>Abre la <a href="../../calculadora-freelance/">calculadora de Tarifa Pro</a>, introduce tus propios datos y cambia una variable cada vez. Después, en el <a href="../../generador-presupuestos/">generador de presupuestos</a>, registra tareas, entregables, revisiones y fechas. Así podrás explicar de dónde salió tu precio y qué incluye, sin atribuirlo a un supuesto estudio de salarios.</p>
        <p>Este ejercicio es educativo. Si tienes gastos irregulares, tipos de impuestos distintos o pagos en otra moneda, adapta el procedimiento y consulta fuentes profesionales antes de usarlo para una decisión contractual.</p>
        """
    },
    {
        "slug": "presupuestar-pagina-web-alcance",
        "title": "Presupuestar una página web: horas, revisiones y cambios de alcance",
        "description": "Caso hipotético de presupuesto de una web con fases verificables, 60 horas de trabajo, licencias, reserva de imprevistos y condiciones para cambios de alcance.",
        "summary": "Desglosa una web en fases y aprende a separar el trabajo contratado de los cambios adicionales.",
        "html": """
        <h2>Por qué una cotización de «una web» es demasiado ambigua</h2>
        <p>Dos proyectos llamados «página web» pueden requerir esfuerzos muy distintos. No es lo mismo crear una landing page con materiales ya entregados que diseñar contenido, conectar formularios, configurar analítica y realizar pruebas en varios navegadores. Una propuesta útil debe explicar el trabajo incluido y aquello que no está incluido.</p>
        <p>Este caso describe una <strong>web informativa hipotética de cinco secciones</strong>, con textos e imágenes facilitados por el cliente, una plantilla propia sencilla, formulario de contacto y dos rondas de revisión. No incluye tienda, reservas ni integraciones externas especiales. Las cantidades son ilustrativas: no reflejan los precios de un mercado o país.</p>
        <h2>Desglose de trabajo que el cliente puede revisar</h2>
        <table class="invoice-table"><thead><tr><th>Fase</th><th>Horas estimadas</th><th>Qué se entrega</th></tr></thead><tbody>
        <tr><td>Descubrimiento y estructura</td><td>6 h</td><td>Mapa de páginas y lista de contenidos necesarios</td></tr>
        <tr><td>Diseño visual</td><td>12 h</td><td>Propuesta de estilos y versiones de escritorio y móvil</td></tr>
        <tr><td>Construcción</td><td>30 h</td><td>Páginas y formulario con validaciones básicas</td></tr>
        <tr><td>Pruebas</td><td>8 h</td><td>Comprobación de navegación, dispositivos y formularios</td></tr>
        <tr><td>Entrega y explicación</td><td>4 h</td><td>Archivos, accesos y guía básica de mantenimiento</td></tr>
        <tr><th>Total</th><th>60 h</th><th>Alcance descrito arriba</th></tr></tbody></table>
        <h2>Una cuenta completa, sin fingir tarifas de mercado</h2>
        <p>Supongamos que <strong>tu propia tarifa de referencia</strong>, calculada previamente con tus gastos y horas facturables, es 20 unidades por hora. Las 60 horas del proyecto representan <strong>60 × 20 = 1.200</strong> unidades. Añades 70 de una licencia acordada y documentada, por lo que la base pasa a <strong>1.270</strong>. Si reservas un 10 % para imprevistos dentro de este ejemplo, obtienes <strong>1.397</strong> unidades antes de cualquier impuesto aplicable.</p>
        <p>Este 10 % no es un recargo universal. Puedes pactar otra reserva o presentar imprevistos por separado; lo importante es que se explique y que los costos externos se puedan comprobar.</p>
        <h2>Qué se incluye y qué requiere una nueva cotización</h2>
        <h3>Incluido</h3>
        <ul><li>Cinco secciones informativas con contenidos entregados en una fecha acordada.</li>
        <li>Diseño adaptable a pantalla pequeña y grande.</li>
        <li>Formulario de contacto con validación básica, condicionado al proveedor de envío que se acuerde.</li>
        <li>Dos rondas consolidadas de ajustes sobre el alcance inicial.</li></ul>
        <h3>Fuera de alcance salvo acuerdo adicional</h3>
        <ul><li>Nuevos idiomas, módulos de pago, cuentas de usuarios o catálogos extensos.</li>
        <li>Redacción integral de todos los textos o producción de fotografías.</li>
        <li>Licencias o servicios de terceros que el cliente no haya autorizado.</li>
        <li>Una tercera ronda de cambios que modifique el diseño ya aprobado.</li></ul>
        <p>Si un cliente pide después una tienda en línea, no lo incluyas como «pequeño arreglo». Registra el pedido, detalla horas y dependencias y envía una ampliación antes de comenzar. Esta práctica hace que ambas partes puedan comparar el presupuesto original con el nuevo.</p>
        <h2>Calendario y pagos: ejemplo negociable</h2>
        <p>Antes de prometer una fecha, confirma cuándo recibirás textos, imágenes, accesos y comentarios. Un retraso en esos materiales puede cambiar el calendario. En este ejemplo ilustrativo, una distribución del total de 1.397 podría ser <strong>30 % al inicio (419,10)</strong>, <strong>40 % tras aprobar el diseño y la primera versión (558,80)</strong> y <strong>30 % en la entrega (419,10)</strong>. Son opciones de negociación, no requisitos legales.</p>
        <h2>Lista de control previa al envío</h2>
        <ol><li>¿La persona que recibirá la propuesta entiende cuántas páginas, plantillas y revisiones se incluyen?</li>
        <li>¿Has separado tu trabajo de licencias, dominio y alojamiento?</li>
        <li>¿Están claras las fechas y qué sucede si faltan materiales?</li>
        <li>¿El impuesto mostrado es realmente el aplicable a tu factura?</li>
        <li>¿Los accesos y la propiedad de los archivos finales quedan definidos?</li></ol>
        <p>Usa el <a href="../../generador-presupuestos/">generador de presupuestos</a> para escribir tus propios importes. Si todavía no conoces tu tarifa mínima interna, calcula primero un escenario en la <a href="../../calculadora-freelance/">calculadora</a>. Revisa el contrato y los requisitos fiscales con personal cualificado cuando corresponda.</p>
        """
    },
    {
        "slug": "cotizar-edicion-video-entregables",
        "title": "Cómo cotizar una edición de video sin olvidar subtítulos ni revisiones",
        "description": "Desglose de un proyecto hipotético de edición de video con 19 horas de trabajo, subtítulos, mezcla, exportación, licencias, revisiones y presupuesto transparente.",
        "summary": "Separa edición, audio, subtítulos, formatos y derechos para que el precio responda al trabajo real.",
        "html": """
        <h2>La duración final del video no mide todo el trabajo</h2>
        <p>Un video terminado de tres minutos puede exigir organizar material bruto, elegir tomas, limpiar audio, añadir subtítulos, comprobar derechos y exportar formatos diferentes. Cotizar solo por minuto final oculta tareas importantes. Lo más claro es detallar cada entrega y las rondas de cambios acordadas.</p>
        <p>Vamos a preparar un presupuesto para un <strong>video informativo hipotético de tres minutos</strong>, basado en material ya grabado por el cliente, con subtítulos, corrección básica de color y dos rondas de cambios. Este ejemplo no se basa en una tarifa comercial observada: sirve para aprender a justificar una propuesta propia.</p>
        <h2>Presupuesto de tiempo por entregable</h2>
        <table class="invoice-table"><thead><tr><th>Actividad</th><th>Horas previstas</th></tr></thead><tbody>
        <tr><td>Revisión del material y selección inicial</td><td>2 h</td></tr>
        <tr><td>Edición y montaje</td><td>8 h</td></tr>
        <tr><td>Subtítulos con revisión manual</td><td>3 h</td></tr>
        <tr><td>Mezcla y limpieza básica de audio</td><td>2 h</td></tr>
        <tr><td>Exportación y control de calidad</td><td>1 h</td></tr>
        <tr><td>Dos rondas de ajustes limitados</td><td>3 h</td></tr>
        <tr><th>Total previsto</th><th>19 h</th></tr></tbody></table>
        <h2>Cálculo verificable con números hipotéticos</h2>
        <p>Supongamos que, según tus propios gastos y disponibilidad, eliges 18 unidades monetarias por hora. El tiempo previsto equivale a <strong>19 × 18 = 342</strong> unidades. Si necesitas una licencia de música por 40, documentada en la cotización, la base sube a <strong>382</strong>. Con una reserva de imprevistos del 10 % aplicada a esa base, el total ilustrativo sería <strong>420,20</strong>, sin incluir impuestos que deban determinarse de forma individual.</p>
        <p>La reserva del 10 % no es una norma ni un promedio de la industria. Es una decisión explícita de este ejemplo, que puede reemplazarse por una cantidad fija, una tarifa acordada por cambios o un presupuesto por fases.</p>
        <h2>Tres preguntas que cambian de verdad el alcance</h2>
        <h3>1. ¿Cuánto material bruto habrá que revisar?</h3>
        <p>Tres minutos terminados pueden proceder de diez minutos de grabación o de varias horas de entrevistas. Solicita duración aproximada, número de cámaras y formato de archivos antes de cerrar el tiempo de selección y almacenamiento.</p>
        <h3>2. ¿Quién entrega música, imágenes y tipografías con permisos de uso?</h3>
        <p>Comprueba si el cliente proporciona recursos autorizados o si tendrás que buscar y pagar licencias. Especifica si la licencia permite el tipo de publicación previsto; no utilices contenido protegido suponiendo que será válido por aparecer en una plataforma.</p>
        <h3>3. ¿Qué significa «dos revisiones»?</h3>
        <p>Define una revisión como un único conjunto consolidado de comentarios. Corregir una palabra de subtítulos es diferente de rehacer el guion o sustituir todas las tomas. La propuesta debe permitir solicitar cambios mayores mediante una cotización adicional.</p>
        <h2>Entrega que se puede comprobar</h2>
        <ul><li>Un archivo final en la resolución, proporción y formato acordados.</li>
        <li>Subtítulos incrustados o archivo aparte, según se haya solicitado.</li>
        <li>Audio revisado para que las voces sean comprensibles, sin prometer estándares no comprobados.</li>
        <li>Una explicación del procedimiento para nuevas correcciones o exportaciones.</li></ul>
        <h2>Antes de dar el precio</h2>
        <p>Pide al cliente un ejemplo del estilo buscado, revisa el material disponible y confirma el plazo. Ajusta las horas del proyecto en función de la información real. Si aún no tienes una tarifa de referencia, empieza por el <a href="../../guias/calcular-tarifa-hora-freelance/">ejercicio de tarifa por hora</a>; después prepara el documento con el <a href="../../generador-presupuestos/">generador de presupuestos</a>.</p>
        <p>La finalidad del ejemplo no es decir cuánto debe cobrar un editor, sino mostrar una manera clara de explicar cómo se forma un precio y qué recibe el cliente a cambio.</p>
        """
    }
]
