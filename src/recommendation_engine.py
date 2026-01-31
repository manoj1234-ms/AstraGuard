def recommend_routes(df):
    df = df.copy()

    # Assign numeric risk score
    df["risk_score"] = df["risk_flag"].map({
        "NORMAL": 0,
        "HIGH": 1
    })

    # Sort: safest first, then fastest
    ranked = df.sort_values(
        by=["risk_score", "final_evac_time"],
        ascending=[True, True]
    )

    return ranked
