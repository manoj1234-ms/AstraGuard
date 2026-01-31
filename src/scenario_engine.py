def simulate_scenario(df, congestion_multiplier=1.0, capacity_multiplier=1.0):
    df = df.copy()

    # Simulate congestion increase
    df["congestion_index"] *= congestion_multiplier

    # Simulate road capacity reduction
    df["road_capacity"] *= capacity_multiplier

    # Recalculate rule-based evacuation time
    df["est_evac_time_min"] = (
        (df["distance_km"] / df["avg_speed_kmph"]) *
        (1 + df["congestion_index"])
    ) * 60

    return df
