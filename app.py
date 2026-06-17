from dotenv import load_dotenv
import os
from pathlib import Path
import json
import joblib
import pandas as pd
from prediction_service import make_prediction    #pegando o módulo prediction que criei
from fastapi import FastAPI, HTTPException
from schemas import PredictRequest, PredictResponse  #Define formato dos dados
from model_utils import load_model_artifacts         #Cuida do carregamento do modelo
from model_loader import load_metrics, load_features

import logging
logging.basicConfig(level=logging.INFO)

load_dotenv()                                        #Carrrega configuração .env

app = FastAPI(title="Customer Default Prediction API", version="0.1.0")

#Configuração do modelo
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")           #Define a versão do modelo
MODEL_FILENAME = f"model_{MODEL_VERSION}.joblib"     #Monta nome do arquivo
MODEL_PATH = Path("output") / MODEL_FILENAME         #Monta o caminho do arquivo

#Configuração de métricas
METRICS_PATH = Path("output/metrics.json")

print(f"Carregando modelo de: {MODEL_PATH}")


#Estado do modelo (runtime)
model = None
model_features = None

#Carregamento do modelo
@app.on_event("startup")
def load_model():
    global model, model_features

    model, _ = load_model_artifacts(MODEL_PATH, METRICS_PATH)
    model_features = load_features(METRICS_PATH)

@app.get("/")
def root():
    return {
        "message": "ML Customer Default Prediction API is running",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_version": MODEL_VERSION,
        "model_file": str(MODEL_PATH),
        "model_file_exists": MODEL_PATH.exists(),
        "metrics_file_exists": METRICS_PATH.exists(),
    }

@app.get("/model-info")
def model_info():
    return {
        "model_version": MODEL_VERSION,
        "model_file": str(MODEL_PATH),
        "model_loaded": model is not None,
        "model_file_exists": MODEL_PATH.exists()
    }


@app.get("/metrics")
def metrics():
    if not METRICS_PATH.exists():
        raise HTTPException(status_code=404, detail="Metrics file not found")

    return load_metrics(METRICS_PATH)


@app.get("/features")
def features():
    return {
        "features": model_features
}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):

    if model is None:
        raise HTTPEcpetion(status_code-500,detail="Model is not loaded")

    prediction, confidence = make_prediction(model, model_features, req)

    return PredictResponse(
        prediction_label="No Default" if prediction == 0 else "Default",
        model_version=MODEL_VERSION,
        model_file=str(MODEL_PATH),
        prediction=prediction,
        confidence=round(confidence,2)
    )

