from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from dotenv import load_dotenv
import os

load_dotenv()

DATA_PATH = Path("data/processed/clean.csv")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")
MODEL_PATH = Path(f"output/model_{MODEL_VERSION}.joblib")
METRICS_PATH = Path("output/metrics.json")

def train():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"{DATA_PATH} not found. Run preprocess first."
        )

    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns=["customer_id", "defaulted"])
    y = df["defaulted"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    metrics = {
        "accuracy": acc,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "features": list(X.columns)
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)

    import json
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"Model saved to {MODEL_PATH}")
    print(f"Accuracy: {acc:.4f}")


if __name__ == "__main__":
    train()
