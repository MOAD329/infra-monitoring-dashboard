def generate_report(metrics, anomalies, recommendations):
    if not anomalies:
        status = "healthy"
    elif any(a["severity"] == "critical" for a in anomalies):
        status = "critical"
    else:
        status = "degraded"

    return {
        "timestamp": metrics.timestamp.isoformat(),
        "global_status": status,
        "summary": {
            "total_anomalies": len(anomalies),
            "total_recommendations": len(recommendations)
        },
        "anomalies": anomalies,
        "recommendations": recommendations
    }