import json
import joblib


def load_model_artifacts(model_path, metrics_path):
    if not model_path.exists():
        raise FileNotFoundError(
            f"Model file not found at {model_path}. Run pipeline.py first."
        )

    model = joblib.load(model_path)

    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        model_features = metrics.get("features")
    else:
        model_features = None

    return model, model_features
