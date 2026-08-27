from __future__ import annotations
import json
import math

def expand_articles(professions: list[dict], countries: list[dict], categories: list[dict]) -> list[dict]:
    articles = []
    
    # Variations of project intents
    intents = [
        {"type": "cuanto-cobrar", "title_tpl": "¿Cuánto cobrar como {profession} en {country}? (Tarifas 2026)", "focus": "tarifas por hora y jornada"},
        {"type": "presupuesto-proyecto", "title_tpl": "Cómo presupuestar proyectos de {profession} en {country}", "focus": "cotización de entregables y alcance"},
        {"type": "guia-impuestos", "title_tpl": "Impuestos y facturación para {profession} freelance en {country}", "focus": "régimen fiscal y retenciones"},
        {"type": "salario-junior-senior", "title_tpl": "Salarios y tarifas Junior vs Senior para {profession} en {country}", "focus": "escalas de experiencia"}
    ]
    
    for prof in professions:
        for country in countries:
            for intent in intents:
                slug = f"{intent['type']}-{prof['slug']}-{country['slug']}"
                title = intent['title_tpl'].format(profession=prof['title'], country=country['name'])
                
                # Dynamic calculations based on exchange rate & country tier
                base_hr_usd_mid = prof.get('base_usd_hour_mid', 25)
                local_rate = country.get('usd_rate', 1.0)
                symbol = country.get('symbol', '$')
                
                hourly_local_mid = int(base_hr_usd_mid * local_rate)
                hourly_local_jr = int(prof.get('base_usd_hour_junior', 12) * local_rate)
                hourly_local_sr = int(prof.get('base_usd_hour_senior', 45) * local_rate)
                
                monthly_est = int(hourly_local_mid * 100)
                
                articles.append({
                    "slug": slug,
                    "title": title,
                    "category": prof["category"],
                    "profession": prof["title"],
                    "country": country["name"],
                    "country_code": country["code"],
                    "currency": country["currency"],
                    "symbol": symbol,
                    "hourly_junior": f"{symbol}{hourly_local_jr:,}",
                    "hourly_mid": f"{symbol}{hourly_local_mid:,}",
                    "hourly_senior": f"{symbol}{hourly_local_sr:,}",
                    "monthly_mid": f"{symbol}{monthly_est:,}",
                    "tax_info": country.get("tax_info", "Régimen fiscal general"),
                    "skills": prof.get("skills", []),
                    "deliverables": prof.get("common_deliverables", []),
                    "intent_type": intent["type"],
                    "excerpt": f"Guía actualizada de tarifas y cotización para {prof['title']} en {country['name']}. Rangos por hora de {symbol}{hourly_local_jr:,} a {symbol}{hourly_local_sr:,} {country['currency']}, impuestos y mejores prácticas de cobro."
                })
                
    return articles
