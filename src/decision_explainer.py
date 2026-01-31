def explain_decision_change(base, stressed):
    reasons = []

    if base["route_id"] != stressed["route_id"]:
        reasons.append("Primary evacuation route changed due to scenario stress.")

    if stressed["final_evac_time"] > base["final_evac_time"]:
        reasons.append("Estimated evacuation time increased due to congestion or capacity reduction.")

    if stressed["risk_flag"] != base["risk_flag"]:
        reasons.append("Risk level increased, triggering stricter safety constraints.")

    if stressed["confidence_score"] < base["confidence_score"]:
        reasons.append("AI confidence dropped as predictions diverged under stress.")

    return reasons
