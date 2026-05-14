import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_FILE = BASE_DIR / "data" / "results_history.json"


def save_result(report):
    os.makedirs(BASE_DIR / "data", exist_ok=True)

    history = []

    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r", encoding="utf-8") as file:
                history = json.load(file)

            if not isinstance(history, list):
                history = []

        except json.JSONDecodeError:
            history = []

    history.append(report)

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False, default=str)