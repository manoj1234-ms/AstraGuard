def detect_system_failure(df):
    """
    Detects when the system should refuse to recommend.
    Returns (failure_flag, reasons)
    """
    reasons = []

    # Rule 1: All routes are HIGH risk
    if (df["risk_flag"] == "HIGH").all():
        reasons.append("All available routes are high risk.")

    # Rule 2: Final evacuation time too large
    if df["final_evac_time"].min() > 180:
        reasons.append("Minimum evacuation time exceeds safe threshold.")

    # Rule 3: Confidence too low across the board
    if df["confidence_score"].max() < 0.5:
        reasons.append("AI confidence is too low for all routes.")

    failure = len(reasons) > 0
    return failure, reasons
