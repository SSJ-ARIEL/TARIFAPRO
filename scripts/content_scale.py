"""Historical route inventory, without manufactured salaries or fiscal data."""
from __future__ import annotations


def expand_articles(professions: list[dict], countries: list[dict], categories: list[dict]) -> list[dict]:
    notices = []
    intents = ("cuanto-cobrar", "presupuesto-proyecto", "guia-impuestos", "salario-junior-senior")
    for profession in professions:
        for country in countries:
            for intent in intents:
                notices.append({
                    "slug": f"{intent}-{profession['slug']}-{country['slug']}",
                    "title": f"Ficha retirada: {profession['title']} en {country['name']}",
                    "category": profession["category"],
                    "profession": profession["title"],
                    "country": country["name"],
                    "intent_type": intent,
                    "excerpt": "Esta ficha antigua se ha retirado. Consulta los métodos de cálculo y las guías de alcance para preparar un presupuesto con tus propios datos.",
                })
    return notices
