# Resposável por carregar recursos do modelo

from pathlib import Path
import json
import joblib


def load_metrics(metrics_path):
    with open(metrics_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_features(metrics_path):
    metrics = load_metrics(metrics_path)
    return metrics.get("features")
