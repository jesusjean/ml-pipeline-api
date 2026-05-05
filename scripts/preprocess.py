from pathlib import Path
import pandas as pd


RAW_PATH = Path("data/raw/customers.csv")
PROCESSED_PATH = Path("data/processed/clean.csv")


def preprocess():
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"{RAW_PATH} not found")

    df = pd.read_csv(RAW_PATH)

    # Limpeza simples
    df = df.dropna(subset=["income", "city"])

    # Criar feature simples
    df["income_per_age"] = df["income"] / df["age"]

    # One-hot encoding da cidade
    df = pd.get_dummies(df, columns=["city"], drop_first=True)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Clean data saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    preprocess()
