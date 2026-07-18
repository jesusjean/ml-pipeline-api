# ML Customer Default Prediction Pipeline



[![CI/CD](https://github.com/jesusjean/ml-pipeline-api/actions/workflows/tests.yml/badge.svg)](https://github.com/jesusjean/ml-pipeline-api/actions/workflows/tests.yml)



End-to-end Machine Learning project that trains a simple customer default prediction model and serves it through a FastAPI REST API.

The project includes data preprocessing, model training, API serving, Docker containerization, automated tests, and a CI/CD pipeline with GitHub Actions and Render.

## Project Overview

This project demonstrates a complete Machine Learning Engineering workflow:

```text
Raw data
↓
Preprocessing
↓
Model training
↓
Model artifacts
↓
FastAPI inference API
↓
Docker image
↓
CI/CD pipeline
↓
Production deployment on Render
```

The goal is not to build the most accurate model, but to demonstrate how a Machine Learning model can be packaged, tested, deployed, and monitored as a production-ready API.

## Live API

Production Swagger documentation:

```text
https://ml-pipeline-api-29u7.onrender.com/docs
```

Main endpoints:

```text
GET  /health
GET  /model-info
GET  /metrics
GET  /features
POST /predict
```

## Features

* End-to-end ML pipeline
* Data preprocessing
* Model training with scikit-learn
* Model artifact generation with joblib
* FastAPI REST API for inference
* Pydantic request and response schemas
* Docker containerization
* Automated tests with pytest
* GitHub Actions CI pipeline
* Docker build validation in CI
* Render deployment through Deploy Hook
* Production verification after deploy
* Commit-based deployment validation

## Architecture

```text
data/raw
   ↓
scripts/preprocess.py
   ↓
data/processed
   ↓
train.py
   ↓
output/model\\\\\\\_v1.joblib
output/metrics.json
   ↓
FastAPI app
   ↓
Docker
   ↓
Render
```

## CI/CD Pipeline

The project uses GitHub Actions to automate quality checks and deployment.

Current workflow:

```text
git push
↓
test
↓
build
↓
deploy
↓
verify
```

Pipeline stages:

1. **test**
Installs dependencies and runs automated tests with pytest.
2. **build**
Builds the Docker image to ensure the Dockerfile is valid.
3. **deploy**
Triggers a Render deployment using a secure Deploy Hook stored in GitHub Secrets.
4. **verify**
Calls the production `/model-info` endpoint and verifies that the deployed commit matches the GitHub commit that triggered the workflow.

This ensures that the API is not only deployed, but that the correct version is running in production.

## Project Structure

```text
.
├── app.py
├── schemas.py
├── model\\\\\\\_utils.py
├── model\\\\\\\_loader.py
├── prediction\\\\\\\_service.py
├── pipeline.py
├── train.py
├── watch\\\\\\\_raw\\\\\\\_data.py
├── requirements.txt
├── Dockerfile
├── README.md
├── data/
│   ├── raw/
│   └── processed/
├── output/
│   ├── model\\\\\\\_v1.joblib
│   └── metrics.json
├── logs/
├── scripts/
│   └── preprocess.py
├── tests/
│   └── test\\\\\\\_api.py
└── .github/
    └── workflows/
        └── tests.yml
```

## Main Components

### `app.py`

Defines the FastAPI application and exposes the API endpoints.

Responsibilities:

* API routing
* Startup model loading
* Health check
* Model information endpoint
* Metrics endpoint
* Features endpoint
* Prediction endpoint

### `schemas.py`

Defines the input and output schemas using Pydantic.

It controls the expected request format and the response structure returned by the API.

### `prediction\\\\\\\_service.py`

Contains the prediction logic.

Responsibilities:

* Prepare input data
* Build the feature row
* Align input columns with model features
* Run model prediction
* Return prediction and confidence

### `model\\\\\\\_loader.py`

Responsible for loading model-related resources.

Responsibilities:

* Load model metrics
* Load expected model features

### `model\\\\\\\_utils.py`

Responsible for loading model artifacts.

Responsibilities:

* Load trained model
* Load model metadata

### `train.py`

Trains the machine learning model and saves the model artifact.

### `pipeline.py`

Runs the full local ML pipeline.

Responsibilities:

* Run preprocessing
* Train model
* Save outputs

### `tests/test\\\\\\\_api.py`

Contains automated API tests.

The test suite validates:

* Health check
* Valid prediction request
* Invalid prediction request
* Missing required field
* Metrics endpoint
* Features endpoint
* Model info endpoint

## Running Locally

### 1\. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 2\. Install dependencies

```bash
pip install -r requirements.txt
```

### 3\. Run the pipeline

```bash
python pipeline.py
```

This will:

1. Preprocess raw data
2. Train the model
3. Save model artifacts

### 4\. Run the API locally

```bash
uvicorn app:app --reload
```

Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Example Prediction Request

Endpoint:

```text
POST /predict
```

Request body:

```json
{
  "age": 30,
  "income": 5000,
  "city": "Sao Paulo"
}
```

Example response:

```json
{
  "prediction\\\\\\\_label": "No Default",
  "confidence": 0.82,
  "model\\\\\\\_version": "v1",
  "model\\\\\\\_file": "output/model\\\\\\\_v1.joblib",
  "prediction": 0
}
```

## Model Info Endpoint

Endpoint:

```text
GET /model-info
```

Example response:

```json
{
  "model\\\\\\\_version": "v1",
  "model\\\\\\\_file": "output/model\\\\\\\_v1.joblib",
  "model\\\\\\\_loaded": true,
  "model\\\\\\\_file\\\\\\\_exists": true,
  "commit\\\\\\\_sha": "543d645..."
}
```

This endpoint is used by the CI/CD pipeline to verify that the expected commit is running in production.

## Metrics Endpoint

Endpoint:

```text
GET /metrics
```

Example response:

```json
{
  "accuracy": 0.5,
  "n\\\\\\\_train": 2,
  "n\\\\\\\_test": 2,
  "features": \\\\\\\[
    "age",
    "income",
    "income\\\\\\\_per\\\\\\\_age",
    "city\\\\\\\_Rio",
    "city\\\\\\\_Sao Paulo"
  ]
}
```

## Features Endpoint

Endpoint:

```text
GET /features
```

Example response:

```json
{
  "features": \\\\\\\[
    "age",
    "income",
    "income\\\\\\\_per\\\\\\\_age",
    "city\\\\\\\_Rio",
    "city\\\\\\\_Sao Paulo"
  ]
}
```

## Running Tests

```bash
pytest
```

Expected result:

```text
7 passed
```

The tests are also executed automatically by GitHub Actions on every push to the `main` branch.

## Docker

Build the Docker image locally:

```bash
docker build -t ml-pipeline-api .
```

Run the container:

```bash
docker run -p 8000:8000 ml-pipeline-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Technologies

* Python
* Pandas
* scikit-learn
* FastAPI
* Pydantic
* Uvicorn
* Joblib
* Pytest
* Docker
* GitHub Actions
* Render

## What This Project Demonstrates

This project demonstrates practical Machine Learning Engineering skills, including:

* Building an end-to-end ML pipeline
* Serving a trained model through an API
* Structuring a Python ML project
* Writing automated API tests
* Containerizing an ML application
* Creating a CI/CD pipeline
* Deploying to production
* Verifying the deployed production version
* Managing secrets securely with GitHub Secrets

## Notes

This project uses a small sample dataset for learning purposes. The main focus is the engineering workflow around the model, not model performance.

