import json
import time
import pandas as pd
import streamlit as st

from models import InfrastructureMetrics
from anomaly_detector import detect_anomalies
from recommender import generate_recommendations
from report_generator import generate_report
from stockage_result import save_result


st.set_page_config(
    page_title="Infra Monitoring",
    layout="wide"
)


def load_data():
    with open("data/simulated_metrics.json", "r", encoding="utf-8") as file:
        return json.load(file)


def process_metric(raw_metric):
    metrics = InfrastructureMetrics(**raw_metric)

    anomalies = detect_anomalies(metrics)

    recommendations = generate_recommendations(anomalies)

    report = generate_report(metrics, anomalies, recommendations)

    save_result(report)

    return metrics, report


st.title("Dashboard de Monitoring Infrastructure")
st.caption("Simulation temps réel à partir de données JSON")

st.markdown("""
### Vue temps réel simulée
Ce tableau de bord lit automatiquement le dataset JSON, injecte les mesures une par une,
détecte les anomalies, affiche les alertes,sauvegarde chaque rapport généré et propose des recommendations.
""")


st.sidebar.header("Contrôle")

start = st.sidebar.button("Démarrer")
reset = st.sidebar.button("Réinitialiser")


if "index" not in st.session_state:
    st.session_state.index = 0

if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = []

if start:
    st.session_state.running = True

if reset:
    st.session_state.index = 0
    st.session_state.running = False
    st.session_state.history = []
    st.rerun()


data = load_data()
dataset_size = len(data)

st.sidebar.info(f"Nombre total de mesures : {dataset_size}")

if not st.session_state.running:
    st.info("Clique sur **Démarrer** dans la barre latérale.")
    st.stop()


if st.session_state.index >= dataset_size:
    st.success("Simulation terminée.")
    st.stop()


raw_metric = data[st.session_state.index]
metrics, report = process_metric(raw_metric)

progress = (st.session_state.index + 1) / dataset_size
st.progress(progress)
st.write(f"Mesure {st.session_state.index + 1} / {dataset_size}")


st.session_state.history.append({
    "timestamp": metrics.timestamp,
    "cpu_usage": metrics.cpu_usage,
    "memory_usage": metrics.memory_usage,
    "latency_ms": metrics.latency_ms,
    "disk_usage": metrics.disk_usage,
    "error_rate": metrics.error_rate,
    "temperature_celsius": metrics.temperature_celsius,
    "anomalies": report["summary"]["total_anomalies"],
    "status": report["global_status"]
})

st.session_state.history = st.session_state.history[-dataset_size:]

df = pd.DataFrame(st.session_state.history)


col1, col2, col3, col4 = st.columns(4)

col1.metric("CPU", f"{metrics.cpu_usage}%", delta="Seuil 80%")
col2.metric("Mémoire", f"{metrics.memory_usage}%", delta="Seuil 85%")
col3.metric("Latence", f"{metrics.latency_ms} ms", delta="Seuil 200 ms")
col4.metric("Température", f"{metrics.temperature_celsius}°C", delta="Seuil 75°C")


if report["global_status"] == "critical":
    st.error("Alerte critique détectée")
elif report["global_status"] == "degraded":
    st.warning("Infrastructure dégradée")
else:
    st.success("Infrastructure saine")


st.subheader("Évolution des métriques")

chart_df = df.set_index("timestamp")[
    [
        "cpu_usage",
        "memory_usage",
        "latency_ms",
        "disk_usage",
        "temperature_celsius"
    ]
]

st.line_chart(chart_df)


left, right = st.columns(2)

with left:
    st.subheader("Anomalies détectées")

    if report["anomalies"]:
        st.dataframe(
            pd.DataFrame(report["anomalies"]),
            use_container_width=True
        )
    else:
        st.info("Aucune anomalie détectée")


with right:
    st.subheader("Recommandations")

    if report["recommendations"]:
        st.dataframe(
            pd.DataFrame(report["recommendations"]),
            use_container_width=True
        )
    else:
        st.info("Aucune recommandation")


st.subheader("Historique affiché")

st.dataframe(df, use_container_width=True)


st.subheader("Dernier rapport JSON")

st.json(report)


st.session_state.index += 1

time.sleep(1)
st.rerun()