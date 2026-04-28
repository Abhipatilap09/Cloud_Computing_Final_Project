def predict_cancellation_risk(airline: str, departure_hour: int, weather_score: float, day_of_week: int) -> float:
    """
    Very simple rule-based scoring model.
    Returns probability between 0 and 1.
    """

    score = 0.10

    # worse weather -> higher cancellation chance
    if weather_score < 0.3:
        score += 0.45
    elif weather_score < 0.6:
        score += 0.20
    else:
        score += 0.05

    # late night / early morning flights
    if departure_hour < 6 or departure_hour > 21:
        score += 0.10

    # weekends slightly more uncertain
    if day_of_week in [6, 7]:
        score += 0.08

    # example airline factor
    airline = airline.lower()
    if airline in ["budgetair", "lowcostx"]:
        score += 0.12
    else:
        score += 0.04

    # keep between 0 and 1
    score = min(max(score, 0.0), 1.0)
    return score