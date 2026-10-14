"""Validate the consolidated publishing surface and withdrawn historical URLs.

These checks detect regressions; they do not certify AdSense approval.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from build import SITE, SITE_URL, CATEGORIES, GUIDES, ARTICLES
from category_workflows import CATEGORY_WORKFLOWS

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = SITE_URL + "/"
INDEXABLE = {
    "", "calculadora-freelance/", "generador-presupuestos/",
    "sobre-tarifa-pro/", "contacto/", "privacidad/", "terminos/", "cookies/",
    *(category["slug"] + "/" for category in CATEGORIES),
    *("guias/" + guide["slug"] + "/" for guide in GUIDES),
}
LEGACY = {article["category"] + "/" + article["slug"] + "/" for article in ARTICLES}


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.script_sources = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        for key in ("href", "src"):
            if attributes.get(key):
                self.urls.append(attributes[key])
        if tag == "script" and attributes.get("src"):
            self.script_sources.append(attributes["src"])


def main() -> None:
    if len(GUIDES) != 9 or len(LEGACY) != 1500:
        raise AssertionError("The reviewed guide inventory or historical URL inventory changed unexpectedly")
    sitemap = ElementTree.parse(DOCS / "sitemap.xml").getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    actual = [entry.findtext(f"{ns}loc") for entry in sitemap.findall(f"{ns}url")]
    expected = {BASE + route for route in INDEXABLE}
    if set(actual) != expected or len(actual) != len(expected):
        raise AssertionError(f"Sitemap difference: missing={expected-set(actual)}, unexpected={set(actual)-expected}")
    if SITE["adsense"]["publisher_id_for_ads_txt"] not in (DOCS / "ads.txt").read_text(encoding="utf-8"):
        raise AssertionError("ads.txt publisher mismatch")
    if BASE + "sitemap.xml" not in (DOCS / "robots.txt").read_text(encoding="utf-8"):
        raise AssertionError("robots.txt sitemap mismatch")

    html_files = list(DOCS.rglob("index.html"))
    seen = set()
    references_checked = 0
    for path in html_files:
        text = path.read_text(encoding="utf-8")
        relative = path.parent.relative_to(DOCS).as_posix()
        route = "" if relative == "." else relative + "/"
        seen.add(route)
        robots = re.search(r'<meta name="robots" content="([^"]+)"', text)
        if not robots:
            raise AssertionError(f"{path}: missing robots meta")
        if ("noindex" not in robots.group(1)) != (route in INDEXABLE):
            raise AssertionError(f"{path}: incorrect indexation state")
        if f'<link rel="canonical" href="{BASE + route}">' not in text:
            raise AssertionError(f"{path}: incorrect canonical")
        if text.count("<h1") != 1:
            raise AssertionError(f"{path}: expected one main heading")
        if f'<meta name="google-adsense-account" content="{SITE["adsense"]["client_id"]}">' not in text:
            raise AssertionError(f"{path}: lost account ownership metadata")
        if SITE["verification"]["google_site_verification"] not in text:
            raise AssertionError(f"{path}: lost site verification")

        parser = References()
        parser.feed(text)
        # Review mode intentionally loads no remote ad, analytics or CMP resources.
        if any(urlsplit(src).scheme or src.startswith("//") for src in parser.script_sources):
            raise AssertionError(f"{path}: third-party scripts must stay paused during review")
        for url in parser.urls:
            parts = urlsplit(url)
            if parts.scheme or parts.netloc or not parts.path:
                continue
            target = (path.parent / unquote(parts.path)).resolve()
            if not target.is_relative_to(DOCS.resolve()):
                raise AssertionError(f"{path}: reference escapes site root: {url}")
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                raise AssertionError(f"{path}: broken local reference: {url}")
            references_checked += 1
        if route in LEGACY:
            if "Ficha antigua retirada" not in text or "Hemos retirado esta ficha" not in text:
                raise AssertionError(f"{path}: missing withdrawal explanation")
            for obsolete in ("hourly_junior", "Nivel Junior", "Nivel Senior", "Régimen RESICO", "Tabulador", '"@type": "Article"'):
                if obsolete in text:
                    raise AssertionError(f"{path}: unsourced matrix content returned: {obsolete}")
        elif route not in INDEXABLE:
            raise AssertionError(f"{path}: unexpected publication route")
    if seen != INDEXABLE | LEGACY:
        raise AssertionError("Missing or unexpected output routes")

    search = json.loads((DOCS / "assets/js/search-index.json").read_text(encoding="utf-8"))
    search_routes = {entry["url"] for entry in search}
    expected_search = INDEXABLE - {"", "sobre-tarifa-pro/", "contacto/", "privacidad/", "terminos/", "cookies/"}
    if search_routes != expected_search or len(search) != len(expected_search):
        raise AssertionError("Search must expose the consolidated tools, categories and original guides only")
    for category in CATEGORIES:
        slug = category["slug"]
        text = (DOCS / slug / "index.html").read_text(encoding="utf-8")
        for expected_text in ("Preguntas que debes resolver antes de cotizar", "Plantilla de alcance", "Cuándo volver a presupuestar", CATEGORY_WORKFLOWS[slug]["guide"]):
            if expected_text not in text:
                raise AssertionError(f"{slug}: missing category-specific scope guidance")
        if "cuanto-cobrar-" in text:
            raise AssertionError(f"{slug}: still promotes retired routes")
    for guide in GUIDES:
        path = DOCS / "guias" / guide["slug"] / "index.html"
        text = path.read_text(encoding="utf-8")
        if text.count("<h2") < 4 or "<table" not in text:
            raise AssertionError(f"{path}: missing worked-example structure")
        if len(re.sub(r"<[^>]+>", " ", guide["html"]).split()) < 420:
            raise AssertionError(f"{path}: substantial guide content unexpectedly lost")
        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
        schema = json.loads(match.group(1)) if match else {}
        if schema.get("@type") != "Article" or schema.get("mainEntityOfPage") != BASE + "guias/" + guide["slug"] + "/":
            raise AssertionError(f"{path}: missing or incorrect editorial metadata")
        if schema.get("author", {}).get("name") != "Tarifa Pro" or "datePublished" in schema:
            raise AssertionError(f"{path}: unverified authorship or publication date")
    contact = (DOCS / "contacto" / "index.html").read_text(encoding="utf-8")
    if f'mailto:{SITE["contact_email"]}' not in contact or "no envía mensajes por sí sola" not in contact:
        raise AssertionError("Contact must provide the existing email and describe its actual behavior")
    for source in (ROOT / "data" / "professions.json", ROOT / "data" / "countries.json"):
        if any(key in source.read_text() for key in ("base_usd_hour", "usd_rate", "tax_info")):
            raise AssertionError(f"{source}: unsourced rate/fiscal model returned")
    print(f"Validated {len(html_files)} pages: {len(INDEXABLE)} indexable, {len(LEGACY)} withdrawal notices, {len(GUIDES)} practical guides.")
    print(f"Sitemap/search, ownership metadata and {references_checked} local references verified; third-party loaders paused.")


if __name__ == "__main__":
    main()
