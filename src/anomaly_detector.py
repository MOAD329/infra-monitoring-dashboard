THRESHOLDS = {
    "cpu_usage": 80,
    "memory_usage": 85,
    "latency_ms": 200,
    "disk_usage": 90,
    "io_wait": 10,
    "temperature_celsius": 75,
    "error_rate": 0.05
}


def get_severity(value: float, threshold: float) -> str:
    ratio = value / threshold

    if ratio >= 1.5:
        return "critical"
    elif ratio >= 1.2:
        return "high"
    else:
        return "medium"


def detect_anomalies(metrics):
    anomalies = []

    for metric, threshold in THRESHOLDS.items():
        value = getattr(metrics, metric)

        if value > threshold:
            anomalies.append({
                "metric": metric,
                "value": value,
                "threshold": threshold,
                "severity": get_severity(value, threshold),
                "message": f"{metric} exceeds the threshold"
            })

    for service, status in metrics.service_status.items():
        if status != "online":
            anomalies.append({
                "metric": f"service_status.{service}",
                "value": status,
                "threshold": "online",
                "severity": "high",
                "message": f"{service} service is {status}"
            })

    return anomalies