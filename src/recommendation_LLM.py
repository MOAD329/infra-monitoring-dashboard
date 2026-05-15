import os
import json
from groq import Groq
from dotenv import load_dotenv

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"


def load_groq_key():
    if not ENV_PATH.exists():
        print("Fichier .env introuvable :", ENV_PATH)
        return None

    content = ENV_PATH.read_text(encoding="utf-8-sig").strip()

    print("ENV CONTENT =", content[:20] + "...")

    if content.startswith("GROQ_API_KEY="):
        return content.split("=", 1)[1].strip()

    return None


GROQ_API_KEY = load_groq_key()

print("ENV PATH =", ENV_PATH)
print("GROQ KEY FOUND =", bool(GROQ_API_KEY))

def generate_manual_recommendations(anomalies):
    recommendations = []

    for anomaly in anomalies:
        metric = anomaly["metric"]
        severity = anomaly["severity"]

        recommendations.append({
            "priorite": severity,
            "categorie": "Infrastructure",
            "probleme": f"Anomalie détectée sur {metric}",
            "explication": anomaly.get("message", "Une anomalie technique a été détectée."),
            "action": "Analyser la métrique concernée, vérifier les logs et appliquer une correction adaptée."
        })

    return recommendations


def generate_llm_recommendations(anomalies, metrics):
    if not anomalies:
        return []

    #client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    client = Groq(api_key=GROQ_API_KEY)
    
    prompt = f"""
Tu es un expert DevOps / SRE.

À partir des métriques infrastructure et des anomalies détectées,
génère des recommandations techniques professionnelles en français.

Réponds uniquement avec un JSON valide sous forme de liste.
Chaque élément doit contenir :
- priorite
- categorie
- probleme
- explication
- impact
- action
- action_court_terme
- action_long_terme

Métriques :
{json.dumps(metrics, ensure_ascii=False, default=str)}

Anomalies :
{json.dumps(anomalies, ensure_ascii=False)}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "Tu génères uniquement du JSON valide, sans markdown."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content
    return json.loads(content)


def generate_recommendations(anomalies, metrics=None):
    try:
        if not anomalies:
            print("Aucune anomalie : pas d'appel Groq.")
            return []

        print("Appel Groq en cours...")

        if metrics is None:
            metrics = {}

        recommendations = generate_llm_recommendations(anomalies, metrics)

        print("Recommandations générées par Groq.")
        return recommendations

    except Exception as e:
        print("Erreur Groq, fallback manuel :", e)
        return generate_manual_recommendations(anomalies)