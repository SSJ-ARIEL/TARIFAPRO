from __future__ import annotations
import json
import html
import shutil
from pathlib import Path
from content_scale import expand_articles
from editorial_guides import GUIDES
from editorial_extensions import EXTENDED_GUIDES
from category_workflows import CATEGORY_WORKFLOWS

GUIDES = GUIDES + EXTENDED_GUIDES

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

def clean_html(content: str) -> str:
    return "\n".join(line.rstrip() for line in content.splitlines()) + "\n"

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
    administrative_routes = ("privacidad", "terminos", "cookies", "contacto", "sobre-tarifa-pro")
    consent_ready = SITE.get("consent", {}).get("configured", False)
    eligible = indexable and not any(canonical == f"{SITE_URL}/{route}/" for route in administrative_routes)
    ads_enabled = eligible and consent_ready and SITE["adsense"].get("enabled", False)
    analytics_enabled = consent_ready and SITE["analytics"].get("enabled", False)
    services = ""
    if ads_enabled or analytics_enabled:
        services = f"""
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('consent', 'default', {{
      'ad_storage': 'denied', 'analytics_storage': 'denied',
      'ad_user_data': 'denied', 'ad_personalization': 'denied',
      'wait_for_update': 500
    }});
  </script>
  <script id="cookieyes" src="https://cdn-cookieyes.com/client_data/{esc(SITE['consent']['cookieyes_client_id'])}/script.js"></script>
"""
    if analytics_enabled:
        services += f"""<script async src="https://www.googletagmanager.com/gtag/js?id={esc(SITE['analytics']['ga4_measurement_id'])}"></script>
  <script>gtag('js', new Date());gtag('config', '{esc(SITE['analytics']['ga4_measurement_id'])}');</script>"""
    if ads_enabled:
        services += f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ad_client}" crossorigin="anonymous"></script>'
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

  {services}

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
        for c in CATEGORIES
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
          Métodos de cálculo y herramientas para preparar presupuestos freelance con alcance y supuestos claros.
        </p>
      </div>
      <div class="footer-col">
        <h4>Herramientas & Secciones</h4>
        <ul class="footer-links">
          <li><a href="{route_url('calculadora-freelance', depth)}">Calculadora de Tarifa por Hora</a></li>
          <li><a href="{route_url('generador-presupuestos', depth)}">Generador de Presupuestos PDF</a></li>
          <li><a href="{route_url('desarrollo-web', depth)}">Presupuestos de desarrollo</a></li>
          <li><a href="{route_url('diseno-multimedia', depth)}">Alcance de diseño visual</a></li>
          <li><a href="{route_url('marketing-digital', depth)}">Gestión de campañas</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Legal & Soporte</h4>
        <ul class="footer-links">
          <li><a href="{route_url('privacidad', depth)}">Política de Privacidad</a></li>
          <li><a href="{route_url('terminos', depth)}">Términos de Servicio</a></li>
          <li><a href="{route_url('cookies', depth)}">Política de Cookies</a></li>
          <li><a href="{route_url('sobre-tarifa-pro', depth)}">Sobre el proyecto y método</a></li>
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
    guide_cards = []
    for guide in GUIDES:
        href = route_url("guias/" + guide["slug"], depth)
        guide_cards.append(
            f'<a href="{href}" class="card"><h3>{esc(guide["title"])}</h3>'
            f'<p>{esc(guide["summary"])}</p></a>'
        )
    guides_html = "\n".join(guide_cards)

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
          <input type="text" id="search-input" class="search-input" data-index-path="{asset_url('assets/js/search-index.json', depth)}" placeholder="Busca una guía, categoría o calculadora...">
          <div id="search-results" class="search-results"></div>
        </div>
      </div>
    </section>

    <!-- Interactive Calculator Widget -->
    <section class="container">
      <div class="calc-card">
        <h2 style="font-size: 1.6rem; color: #fff; margin-bottom: 8px;">🧮 Calculadora Rápida de Tarifa Freelance</h2>
        <p style="color: var(--text-muted); font-size: 0.95rem;">Introduce gastos y disponibilidad para estimar un objetivo interno por hora. Incluye los costos personales y del negocio que quieras cubrir.</p>

        <div class="calc-grid">
          <div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-expenses">Gastos mensuales personales y del negocio:</label>
                <input type="number" id="c-expenses" class="form-input" value="1200" min="0" step="0.01">
              </div>
              <div class="form-group">
                <label class="form-label" for="c-hours">Horas Facturables / Sem.:</label>
                <input type="number" id="c-hours" class="form-input" value="25" min="0.01" max="168" step="0.25">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-vacations">Semanas de Vacaciones / Año:</label>
                <input type="number" id="c-vacations" class="form-input" value="4" min="0" max="51.99" step="0.25">
              </div>
              <div class="form-group">
                <label class="form-label" for="c-savings">Margen de Ahorro / Retiro (%):</label>
                <input type="number" id="c-savings" class="form-input" value="20" min="0" max="300" step="0.1">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
              <div class="form-group">
                <label class="form-label" for="c-taxes">Supuesto de impuestos (%):</label>
                <input type="number" id="c-taxes" class="form-input" value="0" min="0" max="99.99" step="0.1">
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

          <div class="result-card" aria-live="polite">
            <noscript><p>Activa JavaScript para calcular con tus datos. La fórmula y un ejemplo están explicados en la guía de tarifa por hora.</p></noscript>
            <div class="result-stat">
              <div class="result-label">Objetivo orientativo por hora</div>
              <div class="result-val-big" id="res-hourly">—</div>
            </div>
            <div class="result-breakdown">
              <div>
                <div class="result-label">Por Jornada (Day Rate)</div>
                <div class="breakdown-val" id="res-daily">—</div>
              </div>
              <div>
                <div class="result-label">Objetivo mensual medio</div>
                <div class="breakdown-val" id="res-retainer">—</div>
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

      <section style="margin-top:40px;margin-bottom:48px;">
      <h2 class="section-title">Guías con ejemplos que puedes comprobar</h2>
      <p style="color:var(--text-muted);line-height:1.8;margin-bottom:22px;">No son listas de precios supuestamente extraídas del mercado. Cada guía describe sus supuestos, hace las cuentas y explica qué decisiones debe tomar el lector.</p>
      <div class="categories-grid">{guides_html}</div>
    </section>

    <!-- EEAT Editorial Box -->
      <article class="editorial-box">
        <h2>🛡️ Metodología y Criterios Financieros de Tarifa Pro</h2>
        <p>
          En <strong>Tarifa Pro</strong> ofrecemos simulaciones a partir de datos introducidos por cada persona. Las cifras precargadas son ejemplos de cálculo. Las antiguas fichas por país se han retirado porque sus importes no procedían de datos de mercado verificados.
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
    (DOCS / "index.html").write_text(clean_html(html_content), encoding="utf-8")

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
      <h1 style="font-size: 2.4rem;">Calculadora de tarifa por hora y objetivo anual</h1>
      <p style="color: var(--text-muted); max-width: 600px; margin: 0 auto;">Introduce tus propios gastos y horas facturables para obtener una estimación. No es una cotización de mercado ni una recomendación fiscal.</p>
    </div>

    <div class="calc-card" style="max-width: 900px; margin: 0 auto 60px;">
      <div class="calc-grid">
        <div>
          <div class="form-group">
            <label class="form-label" for="c-expenses">Gastos Mensuales Personales & Negocio ($):</label>
            <input type="number" id="c-expenses" class="form-input" value="1500" min="0" step="0.01">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-hours">Horas Reales Facturables por Semana:</label>
            <input type="number" id="c-hours" class="form-input" value="20" min="0.01" max="168" step="0.25">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-vacations">Semanas de Descanso al Año:</label>
            <input type="number" id="c-vacations" class="form-input" value="4" min="0" max="51.99" step="0.25">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-savings">Margen de Ganancia / Ahorro (%):</label>
            <input type="number" id="c-savings" class="form-input" value="25" min="0" max="300" step="0.1">
          </div>
          <div class="form-group">
            <label class="form-label" for="c-taxes">Supuesto de impuestos sobre lo facturado (%):</label>
            <input type="number" id="c-taxes" class="form-input" value="0" min="0" max="99.99" step="0.1">
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

        <div class="result-card" aria-live="polite">
            <noscript><p>Activa JavaScript para calcular con tus datos. La fórmula y un ejemplo están explicados en la guía de tarifa por hora.</p></noscript>
          <div class="result-stat">
            <div class="result-label">Objetivo orientativo por hora</div>
            <div class="result-val-big" id="res-hourly">—</div>
          </div>
          <div class="result-breakdown">
            <div>
              <div class="result-label">Por Día (8h)</div>
              <div class="breakdown-val" id="res-daily">—</div>
            </div>
            <div>
              <div class="result-label">Objetivo mensual medio</div>
              <div class="breakdown-val" id="res-retainer">—</div>
            </div>
          </div>
          <div style="margin-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;">
            <div class="result-label">Meta de Facturación Anual Bruta</div>
            <div class="breakdown-val" id="res-annual" style="color: var(--cyan);">—</div>
          </div>
        </div>
      </div>
    </div>
    <section class="panel-card" style="max-width:900px;margin:0 auto 50px;padding:28px;line-height:1.8;">
      <h2>Cómo se obtiene la estimación</h2>
      <p>Empieza con tus gastos mensuales personales y del negocio. La herramienta calcula el costo anual multiplicando esa cifra por doce; añade el margen de ahorro que indiques y divide entre la proporción restante tras el porcentaje estimado de impuestos. Por último, divide el objetivo anual entre las horas que prevés facturar: horas semanales multiplicadas por las semanas del año menos tus vacaciones.</p>
      <p><strong>Media mensual:</strong> el objetivo bruto anual se divide entre doce, incluidas las semanas de descanso. No es la cotización de un contrato mensual ni equivale a facturar la misma cantidad todas las semanas.</p>
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
    (folder / "index.html").write_text(clean_html(html_content), encoding="utf-8")

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
        <div class="invoice-heading" style="display: flex; justify-content: space-between; border-bottom: 2px solid #0f172a; padding-bottom: 20px; margin-bottom: 20px;">
          <div>
            <h2 style="font-size: 1.6rem; font-weight: 800;">PRESUPUESTO / COTIZACIÓN</h2>
            <input type="text" aria-label="Número de propuesta" value="Nº: COT-001" style="width: 140px; font-weight: 700;">
          </div>
          <div style="text-align: right;">
            <input type="text" aria-label="Nombre del profesional o estudio" value="Tu Nombre o Estudio" style="text-align: right; font-weight: 700; font-size: 1.1rem;"><br>
            <input type="email" aria-label="Correo del profesional" placeholder="Tu correo de contacto" style="text-align: right; font-size: 0.9rem;">
          </div>
        </div>

        <div class="invoice-parties" style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
          <div>
            <strong>CLIENTE:</strong>
            <input type="text" aria-label="Nombre del cliente" value="Nombre del Cliente / Empresa" style="margin-top: 4px;">
            <input type="text" aria-label="Identificación del cliente, si procede" placeholder="Identificación fiscal, si procede" style="margin-top: 4px;">
          </div>
          <div style="text-align: right;">
            <strong>FECHA:</strong>
            <input type="date" id="inv-date" aria-label="Fecha de la propuesta" style="margin-top: 4px; text-align: right;">
          </div>
        </div>

        <p style="margin-bottom:16px;"><label for="inv-currency">Moneda de todos los importes:</label> <select id="inv-currency"><option value="USD">USD</option><option value="EUR">EUR</option><option value="MXN">MXN</option><option value="COP">COP</option><option value="PEN">PEN</option></select></p>
        <div class="table-scroll"><table class="invoice-table">
          <thead>
            <tr>
              <th>Descripción del Servicio / Entregable</th>
              <th style="width: 70px;">Cant.</th>
              <th style="width: 100px;">Precio unitario</th>
              <th style="width: 90px;">Total</th>
              <th style="width: 40px;"><span class="sr-only">Acciones</span></th>
            </tr>
          </thead>
          <tbody id="invoice-items">
            <tr>
              <td><input type="text" aria-label="Descripción del primer servicio" value="Diseño y desarrollo de landing page (ejemplo)" style="width: 100%;"></td>
              <td><input type="number" class="item-qty" aria-label="Cantidad" value="1" min="0.01" step="0.01" style="width: 60px;"></td>
              <td><input type="number" class="item-price" aria-label="Precio unitario" value="650" min="0" step="0.01" style="width: 90px;"></td>
              <td class="item-total" style="font-weight: 700;">—</td>
              <td><button type="button" aria-label="Eliminar servicio" onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">✕</button></td>
            </tr>
            <tr>
              <td><input type="text" aria-label="Descripción del segundo servicio" value="Configuración de dominio y analítica (ejemplo)" style="width: 100%;"></td>
              <td><input type="number" class="item-qty" aria-label="Cantidad" value="1" min="0.01" step="0.01" style="width: 60px;"></td>
              <td><input type="number" class="item-price" aria-label="Precio unitario" value="200" min="0" step="0.01" style="width: 90px;"></td>
              <td class="item-total" style="font-weight: 700;">—</td>
              <td><button type="button" aria-label="Eliminar servicio" onclick="this.closest('tr').remove(); updateInvoiceTotals();" style="background: none; border: none; color: #ef4444; cursor: pointer; font-weight: bold;">✕</button></td>
            </tr>
          </tbody>
        </table></div>

        <button type="button" onclick="addInvoiceRow()" class="btn btn-secondary" style="color: #0f172a; border-color: #cbd5e1; font-size: 0.85rem; padding: 6px 14px; margin-bottom: 20px;">+ Añadir Fila</button>

        <div class="invoice-summary" style="display: flex; justify-content: space-between; border-top: 1px solid #e2e8f0; padding-top: 16px;">
          <div>
            <strong>Términos & Forma de Pago:</strong>
            <textarea aria-label="Alcance, revisiones, plazos y condiciones de pago" style="margin-top: 6px; min-height: 130px; font-size: 0.85rem;">Ejemplo para adaptar: entregables y formatos acordados; dos rondas de revisión; fecha de entrega; exclusiones; vigencia de la propuesta; anticipo y pagos por hitos. Confirma estos términos con el cliente.</textarea>
          </div>
          <div style="text-align: right; min-width: 200px;">
            <p style="color: #64748b;">Subtotal: <span id="inv-subtotal" style="font-weight: 700; color: #0f172a;">—</span></p>
            <p style="color: #64748b; margin: 6px 0;"><label for="inv-tax-pct">Impuesto supuesto (%):</label> <input type="number" id="inv-tax-pct" value="0" min="0" max="100" step="0.01" style="width: 50px; text-align: right;"> <span id="inv-tax-amount" style="font-weight: 700; color: #0f172a;">—</span></p>
            <h3 style="font-size: 1.4rem; color: #0f172a; margin-top: 10px;">TOTAL: <span id="inv-grand-total" style="color: #10b981;">—</span></h3>
          </div>
        </div>
      </div>

      <noscript><p>Activa JavaScript para calcular los totales de tus propios importes antes de imprimir.</p></noscript>
      <p id="invoice-error" role="status" style="color:#fbbf24;margin:16px 0;"></p>
      <div style="display: flex; gap: 16px; justify-content: center;">
        <button id="invoice-print" type="button" disabled onclick="window.print()" class="btn btn-primary">🖨️ Imprimir o guardar como PDF</button>
      </div>
      <section class="panel-card" style="margin:32px 0;padding:28px;line-height:1.8;">
        <h2>Lista de revisión de tu presupuesto</h2>
        <p><strong>Alcance:</strong> define entregables, número de revisiones y exclusiones. <strong>Plazo:</strong> añade fechas de entrega y lo que debe facilitar el cliente. <strong>Pagos:</strong> escribe anticipo, hitos, medios de pago y vencimiento de la propuesta.</p>
        <p>Las cantidades son un ejemplo y el impuesto comienza en cero para que lo determines según tu situación; cero tampoco es una recomendación fiscal. El selector cambia la etiqueta de moneda y no convierte importes. Cámbialos por los que correspondan a tu servicio y verifica la normativa aplicable. Relee los datos personales antes de compartir el archivo.</p>
        <p>La descarga se realiza desde la función «Guardar como PDF» del diálogo de impresión del navegador; no se crea una factura electrónica certificada ni se verifica la identidad de sus participantes.</p>
      </section>
    </div>
  </main>
  {footer(depth)}
  <script src="{asset_url('assets/js/invoice.js', depth)}"></script>
</body>
</html>"""
    (folder / "index.html").write_text(clean_html(html_content), encoding="utf-8")

def build_category_pages():
    category_notes = {
        "desarrollo-web": "Separa descubrimiento, diseño, desarrollo, pruebas, publicación y mantenimiento. Cotiza las integraciones y revisiones como entregables medibles y aclara quién aporta textos, dominios y servicios externos.",
        "diseno-multimedia": "Especifica número de pantallas o piezas, versiones, licencias de imágenes, archivos editables y rondas de cambios. Un diseño con transferencia de derechos puede requerir condiciones distintas de una pieza de uso limitado.",
        "marketing-digital": "Distingue honorarios de gestión y presupuesto de anuncios. Define métricas, periodicidad de informes y límites del servicio, sin garantizar conversiones o resultados dependientes de terceros.",
        "video-animacion": "Pide duración final, material disponible, formato de entrega, cantidad de correcciones, subtítulos y complejidad de efectos. Un video breve con animación compleja no se presupuesta igual que un recorte simple.",
        "redaccion-copywriting": "Aclara investigación, entrevistas, extensión, edición SEO, verificación de fuentes, derechos y cantidad de revisiones. La cantidad de palabras por sí sola no explica el trabajo de una pieza editorial.",
        "ia-automatizacion": "Delimita procesos, accesos, integraciones autorizadas, pruebas, soporte y responsabilidades sobre los datos. Separa costo de configuración de pagos recurrentes por proveedores o consumo.",
        "consultoria-negocios": "Define diagnóstico, reuniones, entregables escritos, horas de seguimiento, supuestos y límites. No prometas resultados financieros que dependen de decisiones o condiciones fuera del alcance contratado.",
    }
    category_questions = {
        "desarrollo-web": [
            "¿Cuántas pantallas, integraciones y formularios están realmente incluidos?",
            "¿Quién entrega textos, imágenes, dominio, alojamiento y accesos de prueba?",
            "¿Cuántas rondas de cambio y cuántos días de soporte ofreces?",
            "¿Cómo se presupuestan futuras funciones después de aprobar el alcance?",
        ],
        "diseno-multimedia": [
            "¿Qué formatos, tamaños y versiones necesita el cliente?",
            "¿Cuántas propuestas iniciales y revisiones están incluidas?",
            "¿Se entregan archivos editables y qué permisos de uso se transfieren?",
            "¿Habrá que comprar recursos visuales o tipografías?",
        ],
        "marketing-digital": [
            "¿Cuál es el objetivo medible de cada campaña y quién aprueba piezas?",
            "¿Qué parte del costo corresponde a honorarios y cuál a la plataforma de anuncios?",
            "¿Quién entrega la página de destino y configura las mediciones?",
            "¿Qué informes, plazos y dependencias quedan por escrito?",
        ],
        "video-animacion": [
            "¿Cuántas horas de material bruto deben revisarse?",
            "¿Qué proporciones, duraciones y subtítulos se entregarán?",
            "¿Quién aporta música y materiales con licencias válidas?",
            "¿Cuántas revisiones de audio, montaje y grafismos se incluyen?",
        ],
        "redaccion-copywriting": [
            "¿El trabajo incluye investigar fuentes, entrevistar o solo editar textos entregados?",
            "¿Qué longitud aproximada, tono, piezas y plazos fueron acordados?",
            "¿Quién revisa exactitud técnica, derechos y atribuciones?",
            "¿Cuántas rondas de correcciones están cubiertas?",
        ],
        "ia-automatizacion": [
            "¿Cuál es el proceso actual y qué resultado concreto debe producir la automatización?",
            "¿Qué sistemas, permisos, datos y proveedores se autorizan?",
            "¿Quién paga suscripciones, consumo de API y mantenimiento?",
            "¿Cómo se prueban fallos, acceso a datos y un posible retorno al proceso manual?",
        ],
        "consultoria-negocios": [
            "¿Cuál es la pregunta de negocio y qué evidencia aportará el cliente?",
            "¿Cuántas reuniones, entrevistas y entregables están incluidos?",
            "¿Qué partes son recomendaciones y cuáles requieren aprobación del cliente?",
            "¿Cómo se definen confidencialidad, seguimiento y tareas fuera de alcance?",
        ],
    }
    depth = 1
    for c in CATEGORIES:
        folder = DOCS / c['slug']
        folder.mkdir(parents=True, exist_ok=True)
        # Link the category's own scope example and the shared calculation method.
        cards = []
        for guide in GUIDES:
            if guide.get("category") != c["slug"] and guide["slug"] != "calcular-tarifa-hora-freelance":
                continue
            url = route_url("guias/" + guide["slug"], depth)
            cards.append(
                f'<a href="{url}" class="card" style="padding:20px;">'
                f'<div><h3>{esc(guide["title"])}</h3>'
                f'<p>{esc(guide["summary"])}</p></div></a>'
            )
        cards_html = "\n".join(cards)
        questions_html = "".join(f"<li>{esc(q)}</li>" for q in category_questions[c["slug"]])
        workflow = CATEGORY_WORKFLOWS[c["slug"]]
        rows_html = "".join(
            f"<tr><th scope='row'>{esc(task)}</th><td>{esc(deliverable)}</td><td>{esc(check)}</td></tr>"
            for task, deliverable, check in workflow["rows"]
        )

        html_content = f"""<!doctype html>
<html lang="es">
{head(f"{c['name']}: alcance y presupuestos | Tarifa Pro", c['description'], f"{SITE_URL}/{c['slug']}/", depth)}
<body>
  {header(c['slug'], depth)}
  <main class="container" style="padding-top: 40px; margin-bottom: 60px;">
    <span class="badge-pill">{c['icon']} Categoría Especializada</span>
    <h1 style="font-size: 2.2rem; margin-bottom: 12px;">{esc(c['name'])}</h1>
    <p style="color: var(--text-muted); font-size: 1.1rem; max-width: 700px; margin-bottom: 36px;">{esc(c['description'])}</p>

    <div class="categories-grid">
      {cards_html}
    </div>
    <section class="panel-card" style="margin-top:36px;padding:28px;line-height:1.8;">
      <h2>Cómo preparar un presupuesto de {esc(c['name'])}</h2>
      <p>{esc(category_notes[c['slug']])}</p>
      <p>{esc(workflow['brief'])}</p>
      <h3>Plantilla de alcance para completar con el cliente</h3>
      <p>Copia las tareas que correspondan a tu proyecto y sustituye cada descripción por una cantidad, formato, fecha y responsable concretos. Si una tarea no se incluye, anótala como exclusión para que la propuesta pueda revisarse antes de empezar.</p>
      <div class="table-scroll"><table class="invoice-table"><thead><tr><th>Tarea</th><th>Entrega que debes definir</th><th>Criterio que debes acordar</th></tr></thead><tbody>{rows_html}</tbody></table></div>
      <h3>Preguntas que debes resolver antes de cotizar</h3>
      <ul>{questions_html}</ul>
      <h3>Cuándo volver a presupuestar</h3>
      <p>{esc(workflow['change'])}</p>
      <p>Usa la <a href="{route_url('calculadora-freelance', depth)}">calculadora de tarifas</a> con tus costos reales y el <a href="{route_url('generador-presupuestos', depth)}">generador de propuestas</a> para anotar alcance, plazos y condiciones. Revisa el alcance concreto de tu trabajo y adapta los valores de ejemplo antes de presupuestar.</p>
    </section>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(clean_html(html_content), encoding="utf-8")

def build_editorial_guides():
    depth = 2
    for guide in GUIDES:
        folder = DOCS / "guias" / guide["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        canonical = f"{SITE_URL}/guias/{guide['slug']}/"
        schema = json.dumps({
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": guide["title"],
            "description": guide["description"],
            "author": {"@type": "Organization", "name": SITE["author"]},
            "publisher": {"@type": "Organization", "name": SITE["name"]},
            "dateModified": "2026-10-14",
            "mainEntityOfPage": canonical,
        }, ensure_ascii=False)
        page = f"""<!doctype html>
<html lang="es">
{head(guide["title"] + " | Tarifa Pro", guide["description"], canonical, depth, "article")}
<body>
  {header("", depth)}
  <main class="container" style="padding-top:48px;padding-bottom:60px;">
    <nav aria-label="Ruta" style="margin-bottom:22px;line-height:1.7;">
      <a href="{route_url('', depth)}">Inicio</a> / Guías / {esc(guide["title"])}
    </nav>
    <div class="panel-card" style="max-width:920px;margin:0 auto;padding:clamp(22px,5vw,48px);">
      <p class="badge-pill">Guía práctica · Actualizada el 14 de octubre de 2026</p>
      <h1 style="font-size:clamp(1.7rem,4vw,2.8rem);line-height:1.2;margin:16px 0;">{esc(guide["title"])}</h1>
      <p style="color:var(--text-muted);font-size:1.15rem;line-height:1.8;margin-bottom:28px;">{esc(guide["summary"])}</p>
      <article class="guide-content" style="color:var(--text-main);font-size:1.05rem;line-height:1.9;">
        {guide["html"]}
      </article>
      <p style="margin-top:32px;padding:18px;border-left:4px solid var(--primary);line-height:1.8;">
        <strong>Nota editorial:</strong> los números son ejemplos elaborados para explicar un método, no datos reales de mercado, tipos de cambio ni asesoría tributaria. Consulta la <a href="{route_url('sobre-tarifa-pro', depth)}">metodología</a> para conocer los límites de la herramienta.
      </p>
      <script type="application/ld+json">{schema}</script>
    </div>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(clean_html(page), encoding="utf-8")


def build_article_pages():
    """Keep bookmarks useful while withdrawing the entire unsourced matrix."""
    depth = 2
    for notice in ARTICLES:
        folder = DOCS / notice["category"] / notice["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        if notice["intent_type"] == "guia-impuestos":
            target = "impuestos-presupuesto-fuentes-oficiales"
        elif notice["intent_type"] in ("cuanto-cobrar", "salario-junior-senior"):
            target = "calcular-tarifa-hora-freelance"
        else:
            target = CATEGORY_WORKFLOWS[notice["category"]]["guide"]
        guide = next(g for g in GUIDES if g["slug"] == target)
        content = f"""<!doctype html>
<html lang="es">
{head(notice['title'] + ' | Tarifa Pro', notice['excerpt'], f"{SITE_URL}/{notice['category']}/{notice['slug']}/", depth, indexable=False)}
<body>
  {header('', depth)}
  <main class="container" style="padding-top:48px;padding-bottom:60px;">
    <article class="panel-card" style="max-width:840px;margin:auto;padding:32px;line-height:1.8;">
      <p class="badge-pill">Ficha antigua retirada</p>
      <h1 style="font-size:clamp(1.6rem,4vw,2.4rem);margin:16px 0;">{esc(notice['title'])}</h1>
      <p>Has llegado a una dirección de una versión anterior de Tarifa Pro. Hemos retirado esta ficha porque sus rangos y resúmenes fiscales no tenían fuentes suficientes para describir el mercado de {esc(notice['country'])}. No se deben usar para cotizar ni para determinar impuestos.</p>
      <h2 style="margin-top:24px;">Continúa con un método que puedes adaptar</h2>
      <p><a href="{route_url('guias/' + target, depth)}">{esc(guide['title'])}</a>: {esc(guide['summary'])}</p>
      <ul>
        <li><a href="{route_url('calculadora-freelance', depth)}">Calcula con tus gastos y horas facturables</a>, sin rangos atribuidos a tu país.</li>
        <li><a href="{route_url('generador-presupuestos', depth)}">Prepara una propuesta con tus importes y entregables</a>.</li>
        <li><a href="{route_url(notice['category'], depth)}">Revisa las preguntas de alcance para {esc(CATEGORY_BY_SLUG[notice['category']]['name'])}</a>.</li>
      </ul>
      <p style="margin-top:20px;">Los nuevos ejemplos son hipotéticos y explican sus cuentas. Para decidir obligaciones fiscales, comprueba las fuentes oficiales de tu jurisdicción.</p>
    </article>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(clean_html(content), encoding="utf-8")

def build_legal_pages():
    depth = 1
    legals = [
        ("privacidad", "Política de Privacidad", "Información sobre tratamiento de datos, cookies de AdSense y privacidad en Tarifa Pro."),
        ("terminos", "Términos de Servicio", "Condiciones de uso de los servicios y calculadoras de Tarifa Pro."),
        ("cookies", "Política de Cookies", "Detalle de cookies técnicas y publicitarias empleadas en el sitio."),
        ("sobre-tarifa-pro", "Sobre Tarifa Pro y Metodología", "Estándares editoriales, origen de los datos y criterios de validación de tarifas freelance."),
        ("contacto", "Contacto y Soporte", "Canal directo para consultas, sugerencias y correcciones de tarifas.")
    ]
    legal_bodies = {
        "privacidad": """
          <h2>Responsable y contacto</h2>
          <p>Tarifa Pro es un proyecto publicado desde la cuenta <a href="https://github.com/SSJ-ARIEL">SSJ-ARIEL</a>. Para consultas privadas sobre el sitio o tus datos, utiliza el correo indicado en la <a href="../contacto/">página de contacto</a>. No publiques información privada en incidencias públicas.</p>
          <h2>Datos introducidos en las herramientas</h2>
          <p>El código de la calculadora y del presupuesto hace las cuentas en tu navegador; no envía esos campos a un formulario o servidor propio de Tarifa Pro. Los documentos se generan con la impresión del navegador. Antes de compartir una cotización o captura, comprueba que no contenga información privada que no quieras entregar. El alojamiento y los servicios que puedan activarse tienen sus propias políticas, descritas a continuación.</p>
          <h2>Servicios externos</h2>
          <p>El alojamiento de GitHub Pages puede recibir datos técnicos de conexión, como la dirección IP y el navegador. En esta versión se han pausado Google Analytics, Google AdSense y CookieYes: las páginas no cargan sus scripts ni usan sus cookies. Antes de activar medición o anuncios, deben verificarse las preferencias de consentimiento y actualizarse esta información con los servicios efectivos.</p>
          <p>Consulta la <a href="https://docs.github.com/es/site-policy/privacy-policies/github-general-privacy-statement">privacidad de GitHub</a>, la <a href="https://policies.google.com/privacy?hl=es">privacidad de Google</a>, <a href="https://policies.google.com/technologies/partner-sites?hl=es">cómo usa Google datos de sitios asociados</a> y la <a href="https://www.cookieyes.com/privacy-policy/">privacidad de CookieYes</a>. Puedes controlar cookies desde tu navegador. Si se activan servicios que requieran consentimiento, sus preferencias deberán estar disponibles en el sitio. Si escribes por correo, el contenido se utiliza para atender esa consulta; evita adjuntar documentación privada que no sea necesaria.</p>
          <h2>Consultas y correcciones</h2>
          <p>Si detectas un dato desactualizado, utiliza el <a href="https://github.com/SSJ-ARIEL/TARIFAPRO/issues">repositorio público de incidencias</a>. No publiques allí datos personales ni documentos confidenciales.</p>
        """,
        "terminos": """
          <h2>Finalidad de las herramientas</h2>
          <p>Tarifa Pro ofrece cálculos y plantillas como material educativo. No garantiza ingresos, condiciones comerciales, salarios ni la aceptación de un presupuesto por clientes o autoridades.</p>
          <h2>Responsabilidad de las decisiones</h2>
          <p>Comprueba los costos, horas, monedas, requisitos fiscales y cláusulas contractuales antes de usar los resultados. Los porcentajes que aparecen al abrir la herramienta son valores de demostración, no recomendaciones universales.</p>
          <h2>Limitaciones</h2>
          <p>Los ejemplos no equivalen a una encuesta de mercado ni determinan obligaciones tributarias. Para casos concretos, acude a fuentes oficiales y profesionales cualificados.</p>
        """,
        "cookies": """
          <h2>Qué servicios se cargan</h2>
          <p>En esta versión están desactivados los scripts de Google Analytics, Google AdSense y CookieYes. La calculadora y el presupuesto no guardan cookies ni propuestas en una cuenta. El alojamiento puede registrar datos técnicos conforme a su propia política de privacidad. Si activamos medición o anuncios, actualizaremos esta página y las preferencias aplicables.</p>
          <h2>Control y preferencias</h2>
          <p>Puedes revisar y eliminar cookies con las opciones de tu navegador. No necesitas aceptar cookies de publicidad o medición para usar las herramientas de esta versión. Para una consulta sobre privacidad, utiliza el correo de <a href="../contacto/">contacto</a>.</p>
          <p>Para conocer el uso de estos recursos, consulta <a href="https://policies.google.com/technologies/cookies?hl=es">la información de cookies de Google</a> y la <a href="https://www.cookieyes.com/privacy-policy/">política de CookieYes</a>. Estos enlaces explican las prácticas de proveedores que se podrían activar en el futuro; no indican que estén cargados en esta versión.</p>
        """,
        "sobre-tarifa-pro": """
          <h2>Quién publica el proyecto</h2>
          <p>Tarifa Pro se mantiene desde la cuenta pública <a href="https://github.com/SSJ-ARIEL">SSJ-ARIEL</a>. Publicamos herramientas educativas y ejemplos con supuestos explícitos. Puedes revisar el código y comunicar correcciones en el repositorio.</p>
          <h2>Qué puedes hacer aquí</h2>
          <p>Calcula una tarifa orientativa desde tus propios gastos y horas facturables y prepara una propuesta que puedes editar e imprimir. Cada ejemplo explica sus supuestos y muestra sus cuentas para que puedas adaptarlo.</p>
          <h2>Cómo se calcula</h2>
          <p>La calculadora convierte tus gastos mensuales en un objetivo anual, suma el margen de ahorro elegido, ajusta por el porcentaje de impuestos que introduces y divide entre las horas facturables estimadas para el año. El precio final sigue dependiendo de tu proyecto y de tu mercado.</p>
          <h2>Cómo interpretamos los datos de ejemplo</h2>
          <p>La versión anterior generaba fichas desde una matriz de profesiones y países con multiplicadores fijos. Ese procedimiento no demostraba precios de mercado; sus rangos y resúmenes fiscales se han eliminado. Las rutas antiguas muestran un aviso de retirada y acceso a las herramientas actuales.</p>
          <h2>Correcciones</h2>
          <p>Las observaciones documentadas pueden comunicarse en <a href="https://github.com/SSJ-ARIEL/TARIFAPRO/issues">GitHub Issues</a>. Evita compartir datos personales en reportes públicos.</p>
        """,
        "contacto": f"""
          <h2>Contacto privado</h2>
          <p>Escribe a <a href="mailto:{esc(SITE["contact_email"])}">{esc(SITE["contact_email"])}</a> para consultas sobre el sitio, privacidad o una corrección que contenga información que no deba publicarse. El enlace abre tu aplicación de correo; esta página no envía mensajes por sí sola. Indica la página afectada y el motivo de la consulta, sin adjuntar documentos fiscales o de clientes innecesarios.</p>
          <h2>Correcciones públicas</h2>
          <p>Puedes comunicar errores de funcionamiento, enlaces rotos, propuestas de mejora o datos que necesiten verificación mediante el <a href="https://github.com/SSJ-ARIEL/TARIFAPRO/issues">formulario de incidencias de GitHub</a>. GitHub puede pedir una cuenta para publicar.</p>
          <p>Selecciona «New issue», describe la página afectada y los pasos para reproducir el problema. Ese espacio es público: no incluyas correo privado de clientes, documentos, identificadores fiscales ni contraseñas.</p>
        """,
    }
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
      <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px;">Actualización: 14 de octubre de 2026</p>

      <div style="color: var(--text-muted); line-height: 1.8; display: flex; flex-direction: column; gap: 16px;">
        {legal_bodies[slug]}
      </div>
    </div>
  </main>
  {footer(depth)}
</body>
</html>"""
        (folder / "index.html").write_text(clean_html(html_content), encoding="utf-8")

def build_search_index():
    # Search only the pages reviewed for public indexing.
    # Preserve previous templated URLs for bookmarks, not for discovery.
    search_data = [
        {
            "title": "Calculadora de tarifa freelance por hora",
            "url": "calculadora-freelance/",
            "profession": "Calculadora de tarifas",
            "country": "",
            "category": "herramientas",
            "currency": "",
        },
        {
            "title": "Generador de presupuestos y cotizaciones",
            "url": "generador-presupuestos/",
            "profession": "Presupuestos",
            "country": "",
            "category": "herramientas",
            "currency": "",
        },
    ]
    for guide in GUIDES:
        search_data.append({
            "title": guide["title"],
            "url": "guias/" + guide["slug"] + "/",
            "profession": "Guía práctica",
            "country": "",
            "category": "guias",
            "currency": "",
        })
    for category in CATEGORIES:
        search_data.append({
            "title": category["name"],
            "url": category["slug"] + "/",
            "profession": category["description"],
            "country": "",
            "category": "categorias",
            "currency": "",
        })
    (DOCS / "assets" / "js" / "search-index.json").write_text(
        json.dumps(search_data, ensure_ascii=False), encoding="utf-8"
    )


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
    for guide in GUIDES:
        urls.append(f"{SITE_URL}/guias/{guide['slug']}/")
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
    print(f"Generating {len(GUIDES)} practical guides, {len(CATEGORIES)} categories and {len(ARTICLES)} withdrawn historical routes...")
    ensure_clean_docs()
    build_home()
    build_calculator_page()
    build_invoice_page()
    build_category_pages()
    build_editorial_guides()
    build_article_pages()
    build_legal_pages()
    build_search_index()
    build_sitemap_and_robots()
    print(f"[OK] Generated guides and withdrawal notices in {DOCS}")

if __name__ == '__main__':
    main()
