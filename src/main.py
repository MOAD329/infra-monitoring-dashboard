import json
from ingestion import load_data
from models import InfrastructureMetrics
from anomaly_detector import detect_anomalies
from recommender import generate_recommendations
from report_generator import generate_report


def main():
    data = load_data("../data/input.json")

    metrics = InfrastructureMetrics(**data)

    anomalies = detect_anomalies(metrics)

    recommendations = generate_recommendations(anomalies)

    report = generate_report(metrics, anomalies, recommendations)

    print(json.dumps(report, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()