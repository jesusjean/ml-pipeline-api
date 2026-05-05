import pandas as pd
import logging

def make_prediction(model, model_features, req):

    logger = logging.getLogger(__name__)
    logger.info("Fazendo previsão...")
    income_per_age = req.income / req.age

    row = {
        "age": req.age,
        "income": req.income,
        "income_per_age": income_per_age,
        "city_Rio": 1 if req.city == "Rio" else 0,
        "city_Sao Paulo": 1 if req.city == "Sao Paulo" else 0,
    }

    X = pd.DataFrame([row])

    if model_features is not None:
        X = X.reindex(columns=model_features, fill_value=0)

    prediction = int(model.predict(X)[0])

    return prediction
