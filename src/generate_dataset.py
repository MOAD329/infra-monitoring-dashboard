import json
from simulator import generate_batch


def main():
    data = generate_batch(size=300, interval_minutes=1)

    with open("../data/simulated_metrics.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    print("Dataset généré avec succès")


if __name__ == "__main__":
    main()