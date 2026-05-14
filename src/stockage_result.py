import json
import os


RESULTS_FILE = "../data/results_history.json"


def save_result(report):
    os.makedirs("../data", exist_ok=True)

    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    history.append(report)

    with open(RESULTS_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=4, ensure_ascii=False)
        