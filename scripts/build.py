from __future__ import annotations
import os
import json
import html
import shutil
from pathlib import Path
from content_scale import expand_articles

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DOCS = ROOT / "docs"
ASSETS = ROOT / "assets"

def read_json(name: str):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

SITE = read_json("site.json")
CATEGORIES = read_json("categories.json")
COUNTRIES = read_json("countries.json")
PROFESSIONS = read_json("professions.json")
CATEGORY_BY_SLUG = {c['slug']: c for c in CATEGORIES}

SITE_URL = SITE["site_url"].rstrip("/")
ARTICLES = expand_articles(PROFESSIONS, COUNTRIES, CATEGORIES)

def esc(v: object) -> str:
    return html.escape(str(v), quote=True)

def prefix(depth: int) -> str:
    return "../" * depth if depth > 0 else "./"

def route_url(route: str = "", depth: int = 0) -> str:
    p = prefix(depth)
    route = route.strip("/")
    if route:
        return f"{p}{route}/"
    return p if depth > 0 else "./"

def asset_url(path: str, depth: int = 0) -> str:
    p = prefix(depth)
    return f"{p}{path.strip('/')}"

def ensure_clean_docs():
    if DOCS.exists():
        shutil.rmtree(DOCS)
    DOCS.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ASSETS, DOCS / "assets")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

def head(title: str, description: str, canonical: str, depth: int = 0, og_type: str = "website", indexable: bool = True) -> str:
    ad_client = esc(SITE["adsense"]["client_id"])
    ad_script = (
        f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ad_client}" crossorigin="anonymous"></script>'
        if indexable else ""
    )
    return f"""
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(description)}">
  <meta name="robots" content="{'index,follow,max-image-preview:large' if indexable else 'noindex,follow'}">
  <meta name="theme-color" content="{esc(SITE['colors']['background'])}">
  <meta name="google-site-verification" content="{esc(SITE['verification']['google_site_verification'])}">
  <meta name="google-adsense-account" content="{esc(SITE['adsense']['client_id'])}">
  <link rel="canonical" href="{esc(canonical)}">
  <link rel="icon" href="{asset_url('assets/icons/favicon.svg', depth)}" type="image/svg+xml">
  <link rel="stylesheet" href="{asset_url('assets/css/styles.css', depth)}">
  
  <!-- Cookie Consent Banner (CookieYes CMP / IAB TCF v2.2) -->
  <script id="cookieyes" type="text/javascript" src="https://cdn-cookieyes.com/client_data/63029c5cae366ef7f38f04401f9d9185/script.js"></script>

  <!-- Google tag (gtag.js) GA4 -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={esc(SITE['analytics']['ga4_measurement_id'])}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{esc(SITE['analytics']['ga4_measurement_id'])}');
  </script>

  <!-- Google AdSense -->
  {ad_script}

  <meta property="og:type" content="{esc(og_type)}">
  <meta property="og:site_name" content="{esc(SITE['name'])}">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(description)}">
  <meta property="og:url" content="{esc(canonical)}">
  <meta property="og:image" content="{esc(SITE_URL)}/assets/icons/favicon.svg">
</head>
""".strip()

def header(active: str = "", depth: int = 0) -> str:
    nav_links = "\n".join([
        f'<a href="{route_url(c["slug"], depth)}" class="{"active" if active == c["slug"] else ""}">{esc(c["nav_label"])}</a>'
        for c in CATEGORIES[:5]
    ])
    return f"""
<header class="site-header">
  <div class="container header-inner">
    <a class="brand" href="{route_url('', depth)}">
      <img src="{asset_url('assets/icons/favicon.svg', depth)}" alt="Tarifa Pro" class="brand-logo">
      <span>Tarifa <span class="brand-gradient">Pro</span></span>
    </a>
    <nav class="main-nav" aria-label="Navegación principal">
      <a href="{route_url('calculadora-freelance', depth)}" class="{"active" if active == 'calc' else ""}">🧮 Calculadora</a>
      <a href="{route_url('generador-presupuestos', depth)}" class="{"active" if active == 'inv' else ""}">📄 Presupuestos</a>
      {nav_links}
    </nav>
  </div>
</header>
""".strip()

def footer(depth: int = 0) -> str:
    return f"""
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col">
        <a class="brand" href="{route_url('', depth)}" style="margin-bottom: 14px;">
          <img src="{asset_url('assets/icons/favicon.svg', depth)}" alt="Tarifa Pro" class="brand-logo">
          <span>Tarifa <span class="brand-gradient">Pro</span></span>
        </a>
        <p style="color: var(--text-muted); font-size: 0.9rem; max-width: 360px;">
          Plataforma de referencia financiera y de cotización para freelancers, agencias y creadores digitales en español.
        </p>
      </div>
      <div class="footer-col">
        <h4>Herramientas & Secciones</h4>
        <ul class="footer-links">
          <li><a href="{route_url('calculadora-freelance', depth)}">Calculadora de Tarifa por Hora</a></li>
          <li><a href="{route_url('generador-presupuestos', depth)}">Generador de Presupuestos PDF</a></li>
          <li><a href="{route_url('desarrollo-web', depth)}">Tarifas de Programación</a></li>
          <li><a href="{route_url('diseno-multimedia', depth)}">Tarifas de Diseño UI/UX</a></li>
          <li><a href="{route_url('marketing-digital', depth)}">Tarifas de Marketing Digital</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Legal & Soporte</h4>
        <ul class="footer-links">
          <li><a href="{route_url('privacidad', depth)}">Política de Privacidad</a></li>
          <li><a href="{route_url('terminos', depth)}">Términos de Servicio</a></li>
          <li><a href="{route_url('cookies', depth)}">Política de Cookies</a></li>
          <li><a href="{route_url('sobre-tarifa-pro', depth)}">Sobre el Proyecto (EEAT)</a></li>
          <li><a href="{route_url('contacto', depth)}">Contacto</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>&copy; 2026 Tarifa Pro. Todos los derechos reservados. Información de referencia y herramientas de cotización profesional.</p>
    </div>
  </div>
</footer>
<script src="{asset_url('assets/js/search.js', depth)}" defer></script>
""".strip()

def build_home():
    depth = 0
    cards = []
    for c in CATEGORIES:
        slug = c['slug']
        icon = c['icon']
        name = esc(c['name'])
        desc = esc(c['description'])
        url = route_url(slug, depth)
        card = f'<a href="{url}" class="card"><div><div class="card-icon">{icon}</div><h3>{name}</h3><p>{desc}</p></div></a>'
        cards.append(card)
    categories_html = "\n".join(cards)

    html_content = f"""<!doctype html>
<html lang="es">
{head("Tarifa Pro | Calculadora de tarifas y presupuestos freelance", SITE['description'], f"{SITE_URL}/", depth)}
<body>
  {header('', depth)}
  
  <main>
    <section class="hero">
      <div class="container">
        <span class="badge-pill">📊 Herramientas de cotización orientativa</span>
        <h1>¿Cuánto Cobrar por tus <span>Servicios Digitales?</span></h1>
        <p class="hero-lead">Calcula una tarifa orientativa desde tus propios gastos, prepara presupuestos y explora ejemplos de proyectos. Los importes ilustrativos no constituyen estadísticas de mercado.</p>
        
        <div class="search-container">
          <span class="search-icon">🔍</span>
          <input type="text" id="search-input" class="search-input" data-index-path="{asset_url('assets/js/search-index.json', depth)}" placeholder="Busca por profesión o país (ej: Desarrollador React en México, Editor en España...)">
          <div id="search-results" class="search-results"></div>
        </div>
      </div>
    </section>

    <!-- Interactive Calculator Widget -->
    <section class="container">
      <div class="calc-card">
        <h2 style="font-size: 1.6rem; color: #fff; margin-bottom: 8px;">🧮 Calculadora Rápida de Tarifa Freelance</h2>
        <p style="color: var(--text-muted); font-size: 0.95rem;">Ingresa tus metas financieras y descubre tu tarifa mínima recomendada por hora y jornada.</p>
        
        <div class="calc-grid">
          <div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-expenses">Gastos Mensuales de Vida ($):</label>
                <input type="number" id="c-expenses" class="form-input" value="1200">
              </div>
              <div class="form-group">
                <label class="form-label" for="c-hours">Horas Facturables / Sem.:</label>
                <input type="number" id="c-hours" class="form-input" value="25">
              </div>
            </div>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-vacations">Semanas de Vacaciones / Año:</label>
                <input type="number" id="c-vacations" class="form-input" value="4">
              </div>
              <div class="form-group">
                <label class="form-label" for="c-savings">Margen de Ahorro / Retiro (%):</label>
                <input type="number" id="c-savings" class="form-input" value="20">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-taxes">Impuestos Estimados (%):</label>
                <input type="number" id="c-taxes" class="form-input" value="15">
              </div>
              <div class="form-group">
                <label class="form-label" for="c-currency">Moneda:</label>
                <select id="c-currency" class="form-select">
                  <option value="$">USD ($) / Dólares</option>
                  <option value="€">EUR (€) / Euros</option>
                  <option value="MX$">MXN ($) / Pesos Mex.</option>
                  <option value="COP$">COP ($) / Pesos Col.</option>
                </select>
              </div>
            </div>
          </div>

          <div class="result-card">
            <div class="result-stat">
              <div class="result-label">Tarifa Mínima Recomendada</div>
              <div class="result-val-big" id="res-hourly">$20 / h</div>
            </div>
            <div class="result-breakdown">
              <div>
                <div class="result-label">Por Jornada (Day Rate)</div>
                <div class="breakdown-val" id="res-daily">$150</div>
              </div>
              <div>
                <div class="result-label">Retainer Mensual</div>
                <div class="breakdown-val" id="res-retainer">$2,100 / mes</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Categories Grid -->
    <section class="container">
      <h2 class="section-title">Explora Guías y Tarifas por Categoría</h2>
      <div class="categories-grid">
        {categories_html}
      </div>

      <!-- EEAT Editorial Box -->
      <article class="editorial-box">
        <h2>🛡️ Metodología y Criterios Financieros de Tarifa Pro</h2>
        <p>
          En <strong>Tarifa Pro</strong> ofrecemos simulaciones a partir de datos introducidos por cada persona. Las cifras precargadas y las fichas por país son ejemplos de cálculo, no resultados de encuestas salariales o tipos de cambio actualizados.
        </p>
        <p>
          Para fijar un precio real, calcula tus gastos, considera el tiempo no facturable y contrasta tus estimaciones con propuestas comparables. El selector de moneda cambia el símbolo, pero no realiza conversiones de divisas.
        </p>
        <div class="badges-row">
          <span class="badge-item">✓ Cálculos editables y orientativos</span>
          <span class="badge-item">✓ Información fiscal a verificar localmente</span>
          <span class="badge-item">✓ Símbolos de moneda sin conversión</span>
          <span class="badge-item">✓ Sin Registro Requerido</span>
        </div>
      </article>
    </section>
  </main>

  {footer(depth)}
  <script src="{asset_url('assets/js/calculator.js', depth)}"></script>
</body>
</html>
"""
    (DOCS / "index.html").write_text(html_content, encoding="utf-8")

def build_calculator_page():
    depth = 1
    folder = DOCS / "calculadora-freelance"
    folder.mkdir(parents=True, exist_ok=True)
    html_content = f"""<!doctype html>
<html lang="es">
{head("Calculadora de Tarifa Freelance por Hora | Tarifa Pro", "Estima una tarifa orientativa a partir de gastos, horas facturables y márgenes configurables.", f"{SITE_URL}/calculadora-freelance/", depth)}
<body>
  {header('calc', depth)}
  <main class="container" style="padding-top: 40px;">
    <div style="text-align: center; margin-bottom: 30px;">
      <span class="badge-pill">🧮 Herramienta Financiera</span>
      <h1 style="font-size: 2.4rem;">Calculadora de Tarifa por Hora y Retainer</h1>
      <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">Introduce tus propios gastos y horas facturables para obtener una estimación. No es una cotización de mercado ni una recomendación fiscal.</p>
    </div>
    
    <div class="calc-card" style="max-width: 900px; margin: 0 auto 60px;">
      <div class="calc-grid">
        <div>
          <div class="form-group">
            <label class="form-label" for="c-expenses">Gastos Mensuales Personales & Negocio ($):</label>
            <input type="number" id="c-expenses" class="form-input" value="1500">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-hours">Horas Reales Facturables por Semana:</label>
            <input type="number" id="c-hours" class="form-input" value="20">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-vacations">Semanas de Descanso al Año:</label>
            <input type="number" id="c-vacations" class="form-input" value="4">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-savings">Margen de Ganancia / Ahorro (%):</label>
            <input type="number" id="c-savings" class="form-input" value="25">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-taxes">Retención de Impuestos Estimada (%):</label>
            <input type="number" id="c-taxes" class="form-input" value="18">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-currency">Símbolo de Moneda:</label>
            <select id="c-currency" class="form-select">
              <option value="$">$ (USD / Pesos)</option>
              <option value="€">€ (Euros)</option>
              <option value="S/">S/ (Soles)</option>
            </select>
          </div>
        </div>

        <div class="result-card">
          <div class="result-stat">
            <div class="result-label">Tu Tarifa por Hora Mínima</div>
            <div class="result-val-big" id="res-hourly">$29 / h</div>
          </div>
          <div class="result-breakdown">
            <div>
              <div class="result-label">Por Día (8h)</div>
              <div class="breakdown-val" id="res-daily">$218</div>
            </div>
            <div>
              <div class="result-label">Retainer Mensual</div>
              <div class="breakdown-val" id="res-retainer">$2,436</div>
            </div>
          </div>
          <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;">
            <div class="result-label">Meta de Facturación Anual Bruta</div>
            <div class="breakdown-val" id="res-annual" style="color: var(--cyan);">$27,439</div>
          </div>
        </div>
      </div>
    </div>
    <section class="panel-card" style="max-width:900px;margin:0 auto 50px;padding:28px;line-height:1.8;">
      <h2>Cómo se obtiene la estimación</h2>
      <p>Empieza con tus gastos mensuales personales y del negocio. La herramienta calcula el costo anual multiplicando esa cifra por doce; añade el margen de ahorro que indiques y divide entre la proporción restante tras el porcentaje estimado de impuestos. Por último, divide el objetivo anual entre las horas que prevés facturar: horas semanales multiplicadas por las semanas del año menos tus vacaciones.</p>
      <h3>Ejemplo que puedes comprobar</h3>
      <p>Si necesitas cubrir 1.000 unidades monetarias al mes, trabajas 20 horas facturables a la semana, descansas 4 semanas y estableces ahorro e impuestos en cero, la cuenta es 12.000 dividido entre 960 horas: 12,50 por hora antes de otros costos. Modifica cada casilla para ver el efecto real de tus supuestos.</p>
      <h3>Qué significa y qué no significa</h3>
      <p>El resultado es un punto de partida matemático, no el precio que pagará un cliente. Contrástalo con costos de herramientas, revisiones, alcance, demanda y presupuestos comparables. Cambiar el símbolo de moneda no convierte importes: introduce todas las cifras en la moneda seleccionada. Revisa tus obligaciones fiscales en fuentes oficiales.</p>
    </section>
  </main>
  {footer(depth)}
  <script src="{asset_url('assets/js/calculator.js', depth)}"></script>
</body>
</html>"""
    (folder / "index.html").write_text(html_content, encoding="utf-8")

def build_invoice_page():
    depth = 1
    folder = DOCS / "generador-presupuestos"
    folder.mkdir(parents=True, exist_ok=True)
    html_content = f"""<!doctype html>
<html lang="es">
{head("Generador de Presupuestos y Cotizaciones PDF | Tarifa Pro", "Prepara una propuesta editable con importes e impuestos de ejemplo y guárdala con la función Imprimir como PDF.", f"{SITE_URL}/generador-presupuestos/", depth)}
<body>
  {header('inv', depth)}
  <main class="container" style="padding-top: 40px; margin-bottom: 60px;">
    <div style="text-align: center; margin-bottom: 30px;">
      <span class="badge-pill">📄 Documento Comercial</span>
      <h1 style="font-size: 2.4rem;">Generador de Presupuestos y Cotizaciones</h1>
      <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">Edita entregables, precios y condiciones. Utiliza la función de impresión del navegador para guardar como PDF y verifica todos los datos antes de enviarlo.</p>
    </div>

    <div style="max-width: 860px; margin: 0 auto;">
      <div id="invoice-area" class="invoice-paper">
        <div style="display: flex; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 1.6rem; font-weight: 800;">PRESUPUESTO / COTIZACIÓN</h2>
            <input type="text" value="Nº: COT-2026-001" style="width: 140px; font-weight: 700;">
          </div>
          <div style="text-align: right;">
            <input type="text" value="Tu Nombre o Estudio" style="text-align: right; font-weight: 700; font-size: 1.1rem;"><br>
            <input type="text" value="contacto@tuweb.com" style="text-align: right; font-size: 0.9rem;">
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
          <div>
            <strong>CLIENTE:</strong>
            <input type="text" value="Nombre del Cliente / Empresa" style="margin-top: 4px;">
            <input type="text" value="Identificación Fiscal / RUC / CIF / RFC" style="margin-top: 4px;">
          </div>
          <div style="text-align: right;">
            <strong>FECHA:</strong>
            <input type="date" value="2026-08-27" style="margin-top: 4px; text-align: right;">
          </div>
        </div>

        <table class="invoice-table">
          <thead>
            <tr>
              <th>Descripción del Servicio / Entregable</th>
              <th style="width: 70px;">Cant.</th>
              <th style="width: 100px;">Precio ($)</th>
              <th style="width: 90px;">Total</th>
              <th style="width: 40px;"></th>
            </tr>
          </thead>
          <tbody id="invoice-items">
            <tr>
              <td><input type="text" value="Diseño y desarrollo de Landing Page de alta conversión" style="width: 100%;"></td>
              <td><input type="number" class="item-qty" value="1" min="1" style="width: 60px;"></td>
              <td><input type="number" class="item-price" value="650" min="0" style="width: 90px;"></td>
              <td class="item-total" style="font-weight: 700;">$650.00</td>
              <td><button onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">✕</button></td>
            </tr>
            <tr>
              <td><input type="text" value="Configuración de analítica, dominio y optimización SEO" style="width: 100%;"></td>
              <td><input type="number" class="item-qty" value="1" min="1" style="width: 60px;"></td>
              <td><input type="number" class="item-price" value="200" min="0" style="width: 90px;"></td>
              <td class="item-total" style="font-weight: 700;">$200.00</td>
              <td><button onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">✕</button></td>
            </tr>
          </tbody>
        </table>

        <button onclick="addInvoiceRow()" class="btn btn-secondary" style="color: #0f172a; border-color: #cbd5e1; font-size: 0.85rem; padding: 6px 14px; margin-bottom: 20px;">+ Añadir Fila</button>

        <div style="display: flex; justify-content: space-between; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          <div>
            <strong>Términos & Forma de Pago:</strong>
            <textarea style="margin-top: 6px; height: 60px; font-size: 0.85rem;">50% de anticipo al inicio y 50% contra entrega final satisfactoria. Pago vía transferencia o Stripe.</textarea>
          </div>
          <div style="text-align: right; min-width: 200px;">
            <p style="color: #64748b;">Subtotal: <span id="inv-subtotal" style="font-weight: 700; color: #0f172a;">$850.00</span></p>
            <p style="color: #64748b; margin: 6px 0;">Impuesto / IVA (%): <input type="number" id="inv-tax-pct" value="16" style="width: 50px; text-align: right;"> <span id="inv-tax-amount" style="font-weight: 700; color: #0f172a;">$136.00</span></p>
            <h3 style="font-size: 1.4rem; color: #0f172a; margin-top: 10px;">TOTAL: <span id="inv-grand-total" style="color: #10b981;">$986.00</span></h3>
          </div>
        </div>
      </div>

      <div style="display: flex; gap: 16px; justify-content: center;">
        <button onclick="window.print()" class="btn btn-primary">🖨️ Imprimir o guardar como PDF</button>
      </div>
      <section class="panel-card" style="margin:32px 0;padding:28px;line-height:1.8;">
        <h2>Lista de revisión de tu presupuesto</h2>
        <p><strong>Alcance:</strong> define entregables, número de revisiones y exclusiones. <strong>Plazo:</strong> añade fechas de entrega y lo que debe facilitar el cliente. <strong>Pagos:</strong> escribe anticipo, hitos, medios de pago y vencimiento de la propuesta.</p>
        <p>Las cantidades de ejemplo y el porcentaje de impuestos precargado no son un presupuesto real ni una tasa fiscal universal. Cámbialos por los que correspondan a tu servicio y verifica la normativa aplicable. Relee los datos personales antes de compartir el archivo.</p>
        <p>La descarga se realiza desde la función «Guardar como PDF» del diálogo de impresión del navegador; no se crea una factura electrónica certificada ni se verifica la identidad de sus participantes.</p>
      </section>
    </div>
  </main>
  {footer(depth)}
  <script src="{asset_url('assets/js/invoice.js', depth)}"></script>
</body>
</html>"""
    (folder / "index.html").write_text(html_content, encoding="utf-8")

def build_category_pages():
    depth = 1
    for c in CATEGORIES:
        folder = DOCS / c['slug']
        folder.mkdir(parents=True, exist_ok=True)
        cat_articles = [a for a in ARTICLES if a["category"] == c["slug"]]
        
        cards = []
        for a in cat_articles[:30]:
            country_name = esc(a['country'])
            country_code = esc(a['country_code'])
            art_title = esc(a['title'])
            mid = esc(a['hourly_mid'])
            curr = esc(a['currency'])
            exc = esc(a['excerpt'][:100])
            url = route_url(c['slug'] + '/' + a['slug'], depth)
            card = f'<a href="{url}" class="card" style="padding: 20px;"><div><span class="badge-pill" style="font-size: 0.75rem; margin-bottom: 8px;">{country_name} ({country_code})</span><h3 style="font-size: 1.15rem; margin-bottom: 8px;">{art_title}</h3><p style="font-size: 0.88rem;">Tarifa recomendada: <strong>{mid}/h</strong> ({curr}). {exc}...</p></div></a>'
            cards.append(card)
        cards_html = "\n".join(cards)

        html_content = f"""<!doctype html>
<html lang="es">
{head(f"{c['name']} - Tarifas y Cotizaciones Freelance | Tarifa Pro", c['description'], f"{SITE_URL}/{c['slug']}/", depth)}
<body>
  {header(c['slug'], depth)}
  <main class="container" style="padding-top: 40px; margin-bottom: 60px;">
    <span class="badge-pill">{c['icon']} Categoría Especializada</span>
    <h1 style="font-size: 2.2rem; margin-bottom: 12px;">{esc(c['name'])}</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem; max-width: 700px; margin-bottom: 36px;">{esc(c['description'])}</p>

    <div class="categories-grid">
      {cards_html}
    </div>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(html_content, encoding="utf-8")

def build_article_pages():
    depth = 2
    for a in ARTICLES:
        folder = DOCS / a["category"] / a["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        
        skills_pills = " ".join([f'<span class="badge-item">{esc(s)}</span>' for s in a["skills"]])
        deliverables_li = "".join([f'<li>{esc(d)}</li>' for d in a["deliverables"]])
        cat_name = esc(CATEGORY_BY_SLUG[a['category']]['name'])
        
        html_content = f"""<!doctype html>
<html lang="es">
{head(f"{a['title']} | Tarifa Pro", a['excerpt'], f"{SITE_URL}/{a['category']}/{a['slug']}/", depth, "article", indexable=False)}
<body>
  {header(a['category'], depth)}
  <main class="container" style="padding-top: 40px; margin-bottom: 60px;">
    <div style="max-width: 880px; margin: 0 auto;">
      <nav style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 16px;">
        <a href="{route_url('', depth)}" style="color: var(--text-muted); text-decoration: none;">Inicio</a> / 
        <a href="{route_url(a['category'], depth)}" style="color: var(--text-muted); text-decoration: none;">{cat_name}</a> / 
        <span>{esc(a['country'])}</span>
      </nav>

      <span class="badge-pill">📍 {esc(a['country'])} &bull; {esc(a['currency'])}</span>
      <h1 style="font-size: clamp(2rem, 4vw, 2.8rem); margin-bottom: 16px; line-height: 1.25;">{esc(a['title'])}</h1>
      <p style="color: var(--text-muted); font-size: 1.15rem; line-height: 1.6; margin-bottom: 30px;">{esc(a['excerpt'])}</p>
      <p role="note" style="padding:16px;border-left:4px solid #f59e0b;line-height:1.7;background:#111827;"><strong>Importante:</strong> esta ficha es una simulación generada a partir de supuestos fijos. Sus cifras no proceden de una encuesta salarial actualizada ni representan impuestos oficiales. Se mantiene accesible para consultas anteriores, pero fuera del índice de buscadores hasta completar una revisión independiente.</p>

      <!-- Pricing Summary Card -->
      <div class="calc-card" style="padding: 24px; margin-bottom: 36px; border-color: var(--border-hover);">
        <h2 style="font-size: 1.3rem; margin-bottom: 16px; color: #fff;">📊 Ejemplo ilustrativo en {esc(a['country'])}</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px;">
          <div style="background: #040914; padding: 16px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="result-label">Nivel Junior (1-2 años)</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--primary);">{esc(a['hourly_junior'])} / h</div>
          </div>
          <div style="background: #040914; padding: 16px; border-radius: 8px; border: 1px solid var(--border-hover);">
            <div class="result-label">Nivel Semi-Senior (3-5 años)</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--cyan);">{esc(a['hourly_mid'])} / h</div>
          </div>
          <div style="background: #040914; padding: 16px; border-radius: 8px; border: 1px solid var(--border);">
            <div class="result-label">Nivel Senior / Consultor</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--indigo);">{esc(a['hourly_senior'])} / h</div>
          </div>
        </div>
      </div>

      <!-- Main Editorial Guide Body -->
      <article style="color: var(--text-main); font-size: 1.05rem; line-height: 1.8;">
        <h2 style="font-size: 1.5rem; margin: 30px 0 14px; color: #fff;">1. Factores que determinan el precio de {esc(a['profession'])}</h2>
        <p style="color: var(--text-muted); margin-bottom: 16px;">
          Al cotizar servicios de <strong>{esc(a['profession'])}</strong> en <strong>{esc(a['country'])}</strong>, es fundamental no basar el precio únicamente en el tiempo dedicado, sino en el valor comercial que la solución aporta al cliente final.
        </p>

        <h3 style="font-size: 1.25rem; margin: 24px 0 10px; color: #fff;">Habilidades técnicas valoradas:</h3>
        <div class="badges-row" style="margin-bottom: 24px;">
          {skills_pills}
        </div>

        <h2 style="font-size: 1.5rem; margin: 30px 0 14px; color: #fff;">2. Entregables más cotizados</h2>
        <ul style="color: var(--text-muted); margin-left: 24px; margin-bottom: 24px;">
          {deliverables_li}
        </ul>

        <h2 style="font-size: 1.5rem; margin: 30px 0 14px; color: #fff;">3. Consideraciones Fiscales e Impuestos en {esc(a['country'])}</h2>
        <p style="color: var(--text-muted); margin-bottom: 16px;">
          Para emitir facturas legales y deducir gastos en {esc(a['country'])}, toma en cuenta:
        </p>
        <div style="background: rgba(16, 185, 129, 0.08); border-left: 4px solid var(--primary); padding: 18px; border-radius: 4px; margin-bottom: 30px;">
          <p style="color: #e2e8f0; font-size: 0.95rem;"><strong>Régimen Fiscal:</strong> Confirma los impuestos, categorías y porcentajes vigentes con la autoridad tributaria de tu país. Esta simulación no determina tu régimen fiscal.</p>
        </div>

        <div style="text-align: center; margin: 40px 0;">
          <a href="{route_url('calculadora-freelance', depth)}" class="btn btn-primary" style="margin-right: 12px;">🧮 Calcular mi tarifa personalizada</a>
          <a href="{route_url('generador-presupuestos', depth)}" class="btn btn-secondary">📄 Crear presupuesto en PDF</a>
        </div>
      </article>
    </div>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(html_content, encoding="utf-8")

def build_legal_pages():
    depth = 1
    legals = [
        ("privacidad", "Política de Privacidad", "Información sobre tratamiento de datos, cookies de AdSense y privacidad en Tarifa Pro."),
        ("terminos", "Términos de Servicio", "Condiciones de uso de los servicios y calculadoras de Tarifa Pro."),
        ("cookies", "Política de Cookies", "Detalle de cookies técnicas y publicitarias empleadas en el sitio."),
        ("sobre-tarifa-pro", "Sobre Tarifa Pro y Metodología", "Estándares editoriales, origen de los datos y criterios de validación de tarifas freelance."),
        ("contacto", "Contacto y Soporte", "Canal directo para consultas, sugerencias y correcciones de tarifas.")
    ]
    for slug, title, desc in legals:
        folder = DOCS / slug
        folder.mkdir(parents=True, exist_ok=True)
        html_content = f"""<!doctype html>
<html lang="es">
{head(f"{title} | Tarifa Pro", desc, f"{SITE_URL}/{slug}/", depth)}
<body>
  {header('', depth)}
  <main class="container" style="padding-top: 40px; margin-bottom: 60px;">
    <div class="panel-card" style="max-width: 840px; margin: 0 auto; background: var(--bg-card); padding: 36px; border-radius: 16px; border: 1px solid var(--border);">
      <h1 style="font-size: 2.2rem; margin-bottom: 16px; color: #fff;">{title}</h1>
      <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px;">Última actualización: Agosto 2026</p>
      
      <div style="color: var(--text-muted); line-height: 1.8; display: flex; flex-direction: column; gap: 16px;">
        <p>En <strong>Tarifa Pro</strong> nos comprometemos con la transparencia, la seguridad de los usuarios y el cumplimiento de las directrices de Google AdSense y normativas internacionales de protección de datos (GDPR / TCF v2.2).</p>
        <p>{desc}</p>
        <p>Para cualquier inquietud o solicitud de soporte, puedes escribirnos a través de nuestro formulario oficial de <a href="{route_url('contacto', depth)}" style="color: var(--primary);">Contacto</a>.</p>
      </div>
    </div>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(html_content, encoding="utf-8")

def build_search_index():
    search_data = []
    for a in ARTICLES:
        search_data.append({
            "title": a["title"],
            "url": f"{a['category']}/{a['slug']}/",
            "category": a["category"],
            "country": a["country"],
            "profession": a["profession"],
            "currency": a["currency"]
        })
    
    (DOCS / "assets" / "js" / "search-index.json").write_text(json.dumps(search_data, ensure_ascii=False), encoding="utf-8")

def build_sitemap_and_robots():
    urls = [
        f"{SITE_URL}/",
        f"{SITE_URL}/calculadora-freelance/",
        f"{SITE_URL}/generador-presupuestos/",
        f"{SITE_URL}/sobre-tarifa-pro/",
        f"{SITE_URL}/contacto/",
        f"{SITE_URL}/privacidad/",
        f"{SITE_URL}/terminos/",
        f"{SITE_URL}/cookies/"
    ]
    for c in CATEGORIES:
        urls.append(f"{SITE_URL}/{c['slug']}/")
    # Pages generated by a country/profession template remain accessible for bookmarks,
    # but are excluded from search indexing until independently reviewed and sourced.
    
    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        xml_lines.append(f"  <url><loc>{esc(u)}</loc><changefreq>weekly</changefreq><priority>0.8</priority></url>")
    xml_lines.append('</urlset>')
    (DOCS / "sitemap.xml").write_text("\n".join(xml_lines), encoding="utf-8")

    robots = f"""User-agent: *
Allow: /
Sitemap: {SITE_URL}/sitemap.xml
"""
    (DOCS / "robots.txt").write_text(robots, encoding="utf-8")
    
    ads_txt = f"google.com, {SITE['adsense']['publisher_id_for_ads_txt']}, DIRECT, f08c47fec0942fa0\n"
    (DOCS / "ads.txt").write_text(ads_txt, encoding="utf-8")

def main():
    print(f"Generating Tarifa Pro for {len(ARTICLES)} guides and {len(CATEGORIES)} categories with relative depth resolution...")
    ensure_clean_docs()
    build_home()
    build_calculator_page()
    build_invoice_page()
    build_category_pages()
    build_article_pages()
    build_legal_pages()
    build_search_index()
    build_sitemap_and_robots()
    print(f"[OK] Generated {len(ARTICLES)} articles in {DOCS}")

if __name__ == '__main__':
    main()
