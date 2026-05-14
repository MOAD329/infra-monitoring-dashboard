import random
import time
from datetime import datetime, timezone, timedelta


def generate_metric(timestamp=None):
    if timestamp is None:
        timestamp = datetime.now(timezone.utc)

    return {
        "timestamp": timestamp.isoformat(),
        "cpu_usage": round(random.uniform(20, 95), 2),
        "memory_usage": round(random.uniform(30, 95), 2),
        "latency_ms": round(random.uniform(50, 350), 2),
        "disk_usage": round(random.uniform(40, 95), 2),
        "network_in_kbps": round(random.uniform(500, 3000), 2),
        "network_out_kbps": round(random.uniform(300, 2500), 2),
        "io_wait": round(random.uniform(1, 20), 2),
        "thread_count": random.randint(50, 300),
        "active_connections": random.randint(10, 200),
        "error_rate": round(random.uniform(0.0, 0.1), 4),
        "uptime_seconds": random.randint(1000, 500000),
        "temperature_celsius": round(random.uniform(45, 90), 2),
        "power_consumption_watts": round(random.uniform(150, 500), 2),
        "service_status": {
            "database": random.choice(["online", "online", "degraded"]),
            "api_gateway": random.choice(["online", "online", "degraded", "offline"]),
            "cache": random.choice(["online", "online", "degraded"])
        }
    }


def generate_batch(size=200, interval_minutes=5):
    start_time = datetime.now(timezone.utc) - timedelta(minutes=size * interval_minutes)

    data = []

    for i in range(size):
        timestamp = start_time + timedelta(minutes=i * interval_minutes)
        data.append(generate_metric(timestamp))

    return data


def stream_metrics(interval_seconds=2):
    current_time = datetime.now(timezone.utc)

    while True:
        yield generate_metric(current_time)
        current_time += timedelta(seconds=interval_seconds)
        time.sleep(interval_seconds)