# Cloud Computing Final Project: Flight Cancellation Prediction API

## Project Status
✅ **COMPLETED** - All APIs implemented, tested locally, and ready for Google Cloud Run deployment.

- Predictor API: Running on port 8000 with `/predict` and `/predict-and-suggest` endpoints
- Alternatives API: Running on port 8001 with `/alternatives` endpoint
- Docker containers configured for Cloud Run
- All endpoints tested and returning expected responses

## Project Overview
This project implements a Google Cloud Run-based API system for predicting flight cancellation risks and suggesting alternative flights. It consists of two microservices: a prediction API and an alternatives API, both deployed on Google Cloud Run.

## Architecture
- **predictor_api**: FastAPI service that predicts flight cancellation probability based on flight details, weather, and scheduling factors.
- **alternatives_api**: FastAPI service that provides alternative flight options for high-risk routes.
- Both services are containerized with Docker and deployed to Google Cloud Run.

## Risk Assessment Logic
The prediction model uses a simple rule-based scoring system:
- **LOW**: Probability < 0.30 (minimal cancellation risk)
- **MEDIUM**: Probability 0.30-0.59 (moderate risk)
- **HIGH**: Probability ≥ 0.60 (high risk - alternatives suggested)

Factors considered: airline type, departure hour, weather score, day of week.

## Folder Structure
```
Cloud_Computing_Final_Project/
├── predictor_api/
│   ├── app.py              # Main FastAPI application
│   ├── model.py            # Simple rule-based prediction model
│   ├── requirements.txt    # Python dependencies
│   ├── alternative_flights.csv  # Alternative flight data
│   ├── sample_flights.csv  # Sample flight data for testing
│   └── Dockerfile          # Docker configuration
├── alternatives_api/
│   ├── app.py              # Main FastAPI application
│   ├── requirements.txt    # Python dependencies
│   ├── alternative_flights.csv  # Alternative flight data
│   └── Dockerfile          # Docker configuration
└── README.md               # This file
```

## Local Setup

### Prerequisites
- Python 3.11+
- Docker (for containerization)
- Google Cloud SDK (for deployment)

### Running Locally

#### Predictor API
```bash
cd predictor_api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### Alternatives API
```bash
cd alternatives_api
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001 --reload
```

## API Endpoints

### Predictor API (Port 8000)

#### GET /
Returns API status.
**Response:**
```json
{
  "message": "Flight Cancellation Prediction API is running"
}
```

#### POST /predict
Predicts cancellation risk for a flight.
**Request:**
```json
{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "United",
  "departure_hour": 22,
  "weather_score": 0.3,
  "day_of_week": 6
}
```
**Response:**
```json
{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "United",
  "cancellation_probability": 0.65,
  "risk_level": "HIGH",
  "message": "Use alternatives API if risk is HIGH"
}
```

#### POST /predict-and-suggest
Predicts cancellation risk and suggests alternatives if risk is HIGH.
**Request:**
```json
{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "budgetair",
  "departure_hour": 0,
  "weather_score": 0.1,
  "day_of_week": 6
}
```
**Response:**
```json
{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "budgetair",
  "cancellation_probability": 0.85,
  "risk_level": "HIGH",
  "alternatives": [
    {
      "flight_number": "UA710",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "United",
      "departure_time": "09:00",
      "arrival_time": "12:00",
      "price": "290"
    },
    {
      "flight_number": "AA711",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "American",
      "departure_time": "12:30",
      "arrival_time": "15:30",
      "price": "310"
    },
    {
      "flight_number": "DL712",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "Delta",
      "departure_time": "17:00",
      "arrival_time": "20:10",
      "price": "305"
    }
  ]
}
```

### Alternatives API (Port 8001)

#### GET /
Returns API status.
**Response:**
```json
{
  "message": "Alternative Flights API is running"
}
```

#### POST /alternatives
Returns up to 3 alternative flights for the given route.
**Request:**
```json
{
  "origin": "SAT",
  "destination": "ORD"
}
```
**Response:**
```json
{
  "origin": "SAT",
  "destination": "ORD",
  "count": 3,
  "alternatives": [
    {
      "flight_number": "UA710",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "United",
      "departure_time": "09:00",
      "arrival_time": "12:00",
      "price": "290"
    },
    {
      "flight_number": "AA711",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "American",
      "departure_time": "12:30",
      "arrival_time": "15:30",
      "price": "310"
    },
    {
      "flight_number": "DL712",
      "origin": "SAT",
      "destination": "ORD",
      "airline": "Delta",
      "departure_time": "17:00",
      "arrival_time": "20:10",
      "price": "305"
    }
  ]
}
```

## Google Cloud Run Deployment

### Build and Push Docker Images
```bash
# Predictor API
cd predictor_api
docker build -t gcr.io/YOUR_PROJECT_ID/flight-predictor:v1 .
docker push gcr.io/YOUR_PROJECT_ID/flight-predictor:v1

# Alternatives API
cd alternatives_api
docker build -t gcr.io/YOUR_PROJECT_ID/flight-alternatives:v1 .
docker push gcr.io/YOUR_PROJECT_ID/flight-alternatives:v1
```

### Deploy to Cloud Run
```bash
# Predictor API
gcloud run deploy flight-predictor \
  --image gcr.io/YOUR_PROJECT_ID/flight-predictor:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000

# Alternatives API
gcloud run deploy flight-alternatives \
  --image gcr.io/YOUR_PROJECT_ID/flight-alternatives:v1 \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000
```

## Testing Instructions

### Local Testing
```bash
# Test Predictor API
curl http://127.0.0.1:8000/

curl -X POST http://127.0.0.1:8000/predict \
-H "Content-Type: application/json" \
-d '{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "United",
  "departure_hour": 22,
  "weather_score": 0.3,
  "day_of_week": 6
}'

# Test Alternatives API
curl -X POST http://127.0.0.1:8001/alternatives \
-H "Content-Type: application/json" \
-d '{
  "origin": "SAT",
  "destination": "ORD"
}'

# Test Combined Endpoint
curl -X POST http://127.0.0.1:8000/predict-and-suggest \
-H "Content-Type: application/json" \
-d '{
  "flight_number": "UA220",
  "origin": "SAT",
  "destination": "ORD",
  "airline": "budgetair",
  "departure_hour": 0,
  "weather_score": 0.1,
  "day_of_week": 6
}'
```

### Cloud Run Testing
Replace the URLs with your deployed service URLs and test similarly.
