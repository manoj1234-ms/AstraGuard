def rank_routes(df):
    df = df.copy()

    # Lower score = better
    df["decision_score"] = (
        0.5 * df["risk_level"]
        + 0.3 * df["congestion_index"]
        + 0.2 * (df["est_evac_time_min"] / df["est_evac_time_min"].max())
    )

    return df.sort_values("decision_score")
