# ML Customer Default Prediction Pipeline

This project demonstrates a simple end-to-end machine learning pipeline.

It includes:

- Data ingestion
- Data preprocessing
- Model training
- Pipeline orchestration
- Model serving through a REST API

## Architecture

Raw data → preprocessing → model training → API inference




## Project Structure

## Project Structure

- `app.py`: orquestra a API FastAPI, define endpoints e chama os serviços
- `schemas.py`: define os formatos de entrada e saída da API
- `model_utils.py`: carrega o modelo e as métricas/features
- `prediction_service.py`: prepara os dados e executa a previsão

- `pipeline.py`: executa o fluxo completo de preprocessamento e treino
- `train.py`: treina o modelo e salva os artefatos
- `scripts/preprocess.py`: limpa e prepara os dados

- `data/`: dados brutos e processados
- `output/`: modelo treinado e métricas
- `logs/`: logs de execução
- `tests/`: testes automatizados (em evolução)


## Running the Pipeline

python pipeline.py


This will:

1. Preprocess raw data
2. Train the model
3. Save model artifacts

## Running the API

uvicorn app:app --reload


Swagger docs:
http://127.0.0.1:8000/docs


## Example Prediction Request

```json
{
  "age": 30,
  "income": 5000,
  "city": "Sao Paulo"
}


## Technologies

Python
Pandas
Scikit-learn
FastAPI
Docker (to be added)
Pytest (to be added)
