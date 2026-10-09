"""Checks for the intentionally indexable Tarifa Pro content.

This validation does not certify AdSense approval. It detects accidental reindexing
of templated country/profession combinations and deployment mistakes.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = "https://ssj-ariel.github.io/TARIFAPRO/"
INDEXABLE = {
    "",
    "calculadora-freelance/",
    "generador-presupuestos/",
    "sobre-tarifa-pro/",
    "contacto/",
    "privacidad/",
    "terminos/",
    "cookies/",
    "desarrollo-web/",
    "diseno-multimedia/",
    "marketing-digital/",
    "video-animacion/",
    "redaccion-copywriting/",
    "ia-automatizacion/",
    "consultoria-negocios/",
    "guias/calcular-tarifa-hora-freelance/",
    "guias/presupuestar-pagina-web-alcance/",
    "guias/cotizar-edicion-video-entregables/",
}
PUBLISHER = "pub-7507181626477156"


def main() -> None:
    sitemap = ElementTree.parse(DOCS / "sitemap.xml").getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    actual = {entry.findtext(f"{ns}loc") for entry in sitemap.findall(f"{ns}url")}
    expected = {BASE + route for route in INDEXABLE}
    if actual != expected:
        raise AssertionError(f"Sitemap difference: missing={expected-actual}, unexpected={actual-expected}")

    if PUBLISHER not in (DOCS / "ads.txt").read_text(encoding="utf-8"):
        raise AssertionError("ads.txt publisher mismatch")
    if BASE + "sitemap.xml" not in (DOCS / "robots.txt").read_text(encoding="utf-8"):
        raise AssertionError("robots.txt sitemap mismatch")

    html_files = list(DOCS.rglob("index.html"))
    indexable_count = 0
    noindex_count = 0
    for path in html_files:
        html = path.read_text(encoding="utf-8")
        relative = path.parent.relative_to(DOCS).as_posix()
        route = "" if relative == "." else relative + "/"
        robots = re.search(r'<meta name="robots" content="([^"]+)"', html)
        if not robots:
            raise AssertionError(f"{path}: missing robots meta")
        has_ad = "pagead2.googlesyndication.com/pagead/js/adsbygoogle.js" in html
        if route in INDEXABLE:
            indexable_count += 1
            if "noindex" in robots.group(1):
                raise AssertionError(f"{path}: expected indexable")
            if not has_ad:
                raise AssertionError(f"{path}: AdSense ownership script missing")
        else:
            noindex_count += 1
            if "noindex" not in robots.group(1):
                raise AssertionError(f"{path}: generated guide must be noindex")
            if has_ad:
                raise AssertionError(f"{path}: generated guide must not load ads")
            if "esta ficha es una simulación" not in html.lower():
                raise AssertionError(f"{path}: generated guide missing disclosure")

    if indexable_count != len(INDEXABLE) or noindex_count != 1500:
        raise AssertionError(f"Unexpected pages: {indexable_count} indexable, {noindex_count} noindex")
    home = (DOCS / "index.html").read_text(encoding="utf-8")
    if "Fórmulas Validadas con Contadores" in home or "Estándares Fiscales 2026" in home:
        raise AssertionError("Unverified marketing claims reintroduced")
    about = (DOCS / "sobre-tarifa-pro" / "index.html").read_text(encoding="utf-8")
    if "matriz de profesiones" not in about:
        raise AssertionError("Methodology page does not disclose data source")
    # These three editorial articles must contain worked examples and be independent.
    for slug in [
        "calcular-tarifa-hora-freelance",
        "presupuestar-pagina-web-alcance",
        "cotizar-edicion-video-entregables",
    ]:
        file = DOCS / "guias" / slug / "index.html"
        text = file.read_text(encoding="utf-8")
        text_without_html = re.sub(r"<[^>]+>", " ", text)
        if len(text_without_html.split()) < 420:
            raise AssertionError(f"{file}: guide is too short to demonstrate its worked example")
        if not ('"@type": "Article"' in text and 'dateModified' in text):
            raise AssertionError(f"{file}: missing honest editorial metadata")
        if text.count("<h1") != 1 or text.count("<h2") < 4:
            raise AssertionError(f"{file}: missing article structure")
        if f'<link rel="canonical" href="{BASE}guias/{slug}/">' not in text:
            raise AssertionError(f"{file}: wrong canonical")
    print("Worked guides and editorial disclosures checked.")
    print(f"Validated {len(html_files)} pages; {indexable_count} indexable, {noindex_count} noindex; {len(actual)} sitemap URLs.")


if __name__ == "__main__":
    main()
