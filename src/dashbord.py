import json
import time
from pathlib import Path

import pandas as pd
import streamlit as st

from models import InfrastructureMetrics
from anomaly_detector import detect_anomalies
#from recommender import generate_recommendations
from report_generator import generate_report
from stockage_result import save_result
from recommendation_LLM import generate_recommendations


# =========================
# CONFIGURATION
# =========================

st.set_page_config(
    page_title="Infrastructure Monitoring",
    layout="wide",
    page_icon="🖥️"
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "rapport.json"

DISPLAY_INTERVAL_SECONDS = 5


# =========================
# STYLE
# =========================

st.markdown("""
<style>
    .main-title {
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 0px;
    }

    .subtitle {
        color: #6c757d;
        font-size: 16px;
        margin-bottom: 25px;
    }

    .status-box {
        padding: 18px;
        border-radius: 12px;
        margin-bottom: 20px;
        font-weight: 600;
        text-align: center;
    }

    .healthy {
        background-color: #d1e7dd;
        color: #0f5132;
    }

    .degraded {
        background-color: #fff3cd;
        color: #664d03;
    }

    .critical {
        background-color: #f8d7da;
        color: #842029;
    }
</style>
""", unsafe_allow_html=True)


# =========================
# FUNCTIONS
# =========================

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def process_metric(raw_metric):

    metrics = InfrastructureMetrics(**raw_metric)

    anomalies = detect_anomalies(metrics)

    recommendations = generate_recommendations(
        anomalies,
        metrics.model_dump()
    )

    report = generate_report(
        metrics,
        anomalies,
        recommendations
    )

    save_result(report)

    return metrics, report


def format_status(status):
    if status == "critical":
        return "CRITIQUE"
    if status == "degraded":
        return "DÉGRADÉ"
    return "SAIN"


# =========================
# HEADER
# =========================

st.markdown('<div class="main-title">Infrastructure Monitoring Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Supervision temps réel simulée à partir de métriques JSON collectées toutes les 30 minutes.</div>',
    unsafe_allow_html=True
)


# =========================
# SIDEBAR
# =========================

st.sidebar.title("Contrôle")

start = st.sidebar.button("Démarrer", use_container_width=True)
stop = st.sidebar.button("Stop", use_container_width=True)
reset = st.sidebar.button("Réinitialiser", use_container_width=True)


# =========================
# SESSION STATE
# =========================

if "index" not in st.session_state:
    st.session_state.index = 0

if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = []


if start:
    st.session_state.running = True

if stop:
    st.session_state.running = False

if reset:
    st.session_state.index = 0
    st.session_state.running = False
    st.session_state.history = []
    st.rerun()


# =========================
# DATA LOADING
# =========================

data = load_data()
dataset_size = len(data)

st.sidebar.info(f"Mesures disponibles : {dataset_size}")
st.sidebar.caption(f"Vitesse de lecture : {DISPLAY_INTERVAL_SECONDS}s / mesure")


if not st.session_state.running:
    st.info("Clique sur **Démarrer** pour lancer la simulation temps réel.")
    st.stop()


if st.session_state.index >= dataset_size:
    st.success("Simulation terminée.")
    st.stop()


# =========================
# CURRENT METRIC
# =========================

raw_metric = data[st.session_state.index]
metrics, report = process_metric(raw_metric)

progress = (st.session_state.index + 1) / dataset_size


# =========================
# HISTORY
# =========================

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

df = pd.DataFrame(st.session_state.history)


# =========================
# GLOBAL STATUS
# =========================

status = report["global_status"]

if status == "critical":
    st.markdown(
        '<div class="status-box critical">🚨 État : CRITIQUE — intervention recommandée</div>',
        unsafe_allow_html=True
    )
elif status == "degraded":
    st.markdown(
        '<div class="status-box degraded">⚠️ État : DÉGRADÉ — surveillance renforcée</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown(
        '<div class="status-box healthy">✅ État : SAIN — aucune anomalie critique </div>',
        unsafe_allow_html=True
    )


# =========================
# PROGRESS
# =========================

st.progress(progress)
st.caption(
    f"Mesure {st.session_state.index + 1} / {dataset_size} — Timestamp : {metrics.timestamp}"
)


# =========================
# KPI
# =========================

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("CPU", f"{metrics.cpu_usage}%", "Seuil 80%")
kpi2.metric("Mémoire", f"{metrics.memory_usage}%", "Seuil 85%")
kpi3.metric("Latence", f"{metrics.latency_ms} ms", "Seuil 200 ms")
kpi4.metric("Disque", f"{metrics.disk_usage}%", "Seuil 90%")
kpi5.metric("Anomalies", report["summary"]["total_anomalies"])


# =========================
# SYNTHESIS
# =========================

st.subheader("Synthèse opérationnelle")

col_a, col_b, col_c = st.columns(3)

with col_a:
    st.metric("Statut", format_status(status))

with col_b:
    st.metric("Taux d’erreur", f"{metrics.error_rate}")

with col_c:
    st.metric("Température", f"{metrics.temperature_celsius}°C")


# =========================
# CHARTS
# =========================

st.subheader("Évolution des métriques principales")

chart_df = df.set_index("timestamp")[
    [
        "cpu_usage",
        "memory_usage",
        "disk_usage",
        "temperature_celsius"
    ]
]

st.line_chart(chart_df)

st.subheader("Évolution de la latence")

latency_df = df.set_index("timestamp")[["latency_ms"]]
st.line_chart(latency_df)


# =========================
# ANOMALIES AND RECOMMENDATIONS
# =========================

left, right = st.columns(2)

with left:
    st.subheader("Anomalies détectées")

    if report["anomalies"]:
        anomalies_df = pd.DataFrame(report["anomalies"])
        st.dataframe(anomalies_df, use_container_width=True)
    else:
        st.success("Aucune anomalie détectée sur cette mesure.")

with right:
    st.subheader("Recommandations prioritaires")

    if report["recommendations"]:
        recommendations_df = pd.DataFrame(report["recommendations"])
        st.dataframe(recommendations_df, use_container_width=True)
    else:
        st.success("Aucune action corrective nécessaire.")


# =========================
# HISTORY TABLE
# =========================

with st.expander("Historique détaillé des mesures"):
    st.dataframe(df, use_container_width=True)


with st.expander("Dernier rapport JSON"):
    st.json(report)


# =========================
# NEXT STEP
# =========================

st.session_state.index += 1

time.sleep(DISPLAY_INTERVAL_SECONDS)
st.rerun()