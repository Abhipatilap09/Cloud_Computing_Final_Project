from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_cancellation_risk
import csv

app = FastAPI(title="Flight Cancellation Prediction API")

class FlightRequest(BaseModel):
    flight_number: str
    origin: str
    destination: str
    airline: str
    departure_hour: int
    weather_score: float   # 0 = very bad weather, 1 = very good weather
    day_of_week: int       # 1=Mon, 7=Sun

def load_alternatives():
    flights = []
    with open("alternative_flights.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            flights.append(row)
    return flights

@app.get("/")
def home():
    return {"message": "Flight Cancellation Prediction API is running"}

@app.post("/predict")
def predict_flight(request: FlightRequest):
    probability = predict_cancellation_risk(
        airline=request.airline,
        departure_hour=request.departure_hour,
        weather_score=request.weather_score,
        day_of_week=request.day_of_week
    )

    if probability < 0.30:
        risk = "LOW"
    elif probability < 0.60:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "flight_number": request.flight_number,
        "origin": request.origin,
        "destination": request.destination,
        "airline": request.airline,
        "cancellation_probability": round(probability, 3),
        "risk_level": risk,
        "message": "Use alternatives API if risk is HIGH"
    }

@app.post("/predict-and-suggest")
def predict_and_suggest(request: FlightRequest):
    probability = predict_cancellation_risk(
        airline=request.airline,
        departure_hour=request.departure_hour,
        weather_score=request.weather_score,
        day_of_week=request.day_of_week
    )

    if probability < 0.30:
        risk = "LOW"
    elif probability < 0.60:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    alternatives = []
    if risk == "HIGH":
        flights = load_alternatives()
        matches = [
            f for f in flights
            if f["origin"].upper() == request.origin.upper()
            and f["destination"].upper() == request.destination.upper()
        ]
        alternatives = matches[:3]

    return {
        "flight_number": request.flight_number,
        "origin": request.origin,
        "destination": request.destination,
        "airline": request.airline,
        "cancellation_probability": round(probability, 3),
        "risk_level": risk,
        "alternatives": alternatives
    }