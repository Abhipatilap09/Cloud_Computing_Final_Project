from fastapi import FastAPI
from pydantic import BaseModel
import csv

app = FastAPI(title="Alternative Flights API")

class AlternativeRequest(BaseModel):
    origin: str
    destination: str

def load_alternatives():
    flights = []
    with open("alternative_flights.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            flights.append(row)
    return flights

@app.get("/")
def home():
    return {"message": "Alternative Flights API is running"}

@app.post("/alternatives")
def get_alternatives(request: AlternativeRequest):
    flights = load_alternatives()

    matches = [
        f for f in flights
        if f["origin"].upper() == request.origin.upper()
        and f["destination"].upper() == request.destination.upper()
    ]

    return {
        "origin": request.origin,
        "destination": request.destination,
        "count": min(len(matches), 3),
        "alternatives": matches[:3]
    }