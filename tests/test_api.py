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

def test_features():
    client = TestClient(app)

    response = client.get("/features")

    assert response.status_code == 200

    data = response.json()

    expected_features = [
        "age",
        "income",
        "income_per_age",
        "city_Rio",
        "city_Sao Paulo"
    ]

    assert data["features"] == expected_features


def test_model_info():
    client = TestClient(app)

    response = client.get("/model-info")

    assert response.status_code == 200

    data = response.json()

    assert data["model_version"] == "v1"
    assert data["model_loaded"] is True
    assert data["model_file_exists"] is True

def test_predict_invalid_input():
    payload = {
       "age": "banana",
       "income": 5000,
       "city": "Sao Paulo"
    }

    client = TestClient(app)
    response = client.post("/predict", json=payload)
    assert response.status_code == 422

def test_predict_missing_filed():
    payload = {
      "age": 30,
      "city": "Sao Paulo"
    }

    client = TestClient(app)
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
