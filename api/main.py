"""
main.py
@TODO: provide four distinct endpoints: health check, predict sentiment, predict with probability, get training example
"""

import joblib
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import pandas as pd
import json
import time

app = FastAPI(title="Movie Sentiment Prediction API")


@app.get("/")
def read_root():
    return 0


try:
    model = joblib.load("sentiment_model.pkl")
    print("Model loaded successfully")
except FileNotFoundError:
    print("Error: Model file not found!")
    model = None


class PredictionInput(BaseModel):
    text: str
    true_sentiment: str


@app.on_event("startup")
def startup_event():
    """
    A startup event handler. It checks if the model was loaded corretly.
    If not, it prints a persistent warning
    """
    if model is None:
        print("WARNING: Model is not loaded. Prediction endpoints will not work")


@app.get("/health")
def health_check():
    """
    Health Check Endpoint
    This endpoint is used to verify that the API server is running and responsive.
    It's a common practice for monitoring services
    """
    return {"Status": "ok", "message": "API is running"}


LOG_FILE = "/logs/prediction_logs.json"


@app.post("/predict")
def predict(input_data: PredictionInput):
    """
    Prediction Endpoint
    Takes a movie review and returns a binary prediction negative or positive.
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Coannot make predictions",
        )
    # features_array = np.array(input_data.review_text).reshape(1,-1)
    prediction = model.predict([input_data.text])

    # Create a Python dictionary
    log_entry = {
        "timestamp": time.asctime(),
        "request_text": input_data.text,
        "predicted_sentiment": prediction[0],
        "true_sentiment": input_data.true_sentiment,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    return {"sentiment": (prediction[0])}


@app.post("/predict_proba")
def predict_with_probability(input_data: PredictionInput):
    """
    Prediction with Probability Endpoint
    Takes a review and returns the prediction along with the probability for the predicted class
    """
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model is not loaded. Cannot make predictions",
        )

    # features_array = np.array(input_data.features).reshape(1,-1)

    # probabilities = model.predict_proba(features_array)
    prediction = model.predict([input_data.text])
    prediction_probabilties = model.predict_proba([input_data.text])

    # The probabilties for class 0 and class 1
    prob_class_0 = prediction_probabilties[0][0]
    prob_class_1 = prediction_probabilties[0][1]
    class_probability = 0
    if prob_class_0 > prob_class_1:
        class_probability = prediction_probabilties[0][0]
    else:
        class_probability = prediction_probabilties[0][1]

    return {"sentiment": (prediction[0]), "probability": round(class_probability, 4)}


@app.get("/example")
def get_training_example():
    """
    Randomly gets a single IMDB review from the dataset and returns that review
    """
    reviews = pd.read_csv("IMDB_Dataset.csv")
    random_row = reviews.sample(n=1)
    row_series = random_row
    json_string = row_series.to_json(orient="split")
    parsed = json.loads(json_string)
    review_text = parsed["data"][0][parsed["columns"].index("review")]
    review_json = {"text": review_text}

    return review_json
