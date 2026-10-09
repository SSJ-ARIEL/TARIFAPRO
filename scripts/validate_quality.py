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
    print(f"Validated {len(html_files)} pages; {indexable_count} indexable, {noindex_count} noindex; {len(actual)} sitemap URLs.")


if __name__ == "__main__":
    main()
