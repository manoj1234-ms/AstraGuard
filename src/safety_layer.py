import numpy as np

def compute_confidence(rule_time, ml_time):
    diff_ratio = abs(rule_time - ml_time) / rule_time

    # Confidence decreases as disagreement increases
    confidence = max(0, 1 - diff_ratio)

    return round(confidence, 2)


def apply_safety_logic(df):
    df = df.copy()

    df["final_evac_time"] = df[
        ["est_evac_time_min", "ml_predicted_time"]
    ].max(axis=1)

    df["confidence_score"] = df.apply(
        lambda row: compute_confidence(
            row["est_evac_time_min"],
            row["ml_predicted_time"]
        ),
        axis=1
    )

    df["risk_flag"] = df["confidence_score"].apply(
        lambda c: "HIGH" if c < 0.7 else "NORMAL"
    )

    return df
