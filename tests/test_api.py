import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient
from app import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_predict():
    payload = {
        "age": 30,
        "income": 5000,
        "city": "Sao Paulo"
    }

    with TestClient(app) as client:
        response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data

def test_metrics():
    client = TestClient(app)
    
    response = client.get("/metrics")

    assert response.status_code == 200

    data = response.json()

    assert "accuracy" in data
    assert "features" in data
