from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    age: int = Field(..., example=30)
    income: float = Field(..., example=5000)
    city: str = Field(..., example="Sao Paulo")


class PredictResponse(BaseModel):
    prediction_label: str = Field(..., example="No Default")
    confidence: float = Field(..., example=0.82)
    model_version: str = Field(..., example="v1")
    model_file: str = Field(..., example="output/model_v1.joblib")
    prediction: int = Field(..., example=0)
