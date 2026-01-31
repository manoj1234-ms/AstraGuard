import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    
    #derived features
    df["load_factor"] = df["population"] / df["road_capacity"]
    df["congestion_index"] = df["load_factor"] * df["risk_level"]

    # Estimated evacuation time (minutes)
    df["est_evac_time_min"] = ((df["distance_km"] / df["avg_speed_kmph"]) * 60 * (1 + df["congestion_index"])).round(1)

    return df

