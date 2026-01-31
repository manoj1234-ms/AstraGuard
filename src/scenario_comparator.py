from src.scenario_engine import simulate_scenario
from src.safety_layer import apply_safety_logic
from src.recommendation_engine import recommend_routes

def compare_scenarios(df, model, features, cong, cap):
    # Baseline
    base = simulate_scenario(df.copy(), 1.0, 1.0)
    base["ml_predicted_time"] = model.predict(base[features])
    base_safe = apply_safety_logic(base)
    base_best = recommend_routes(base_safe).iloc[0]

    # Stressed
    stressed = simulate_scenario(df.copy(), cong, cap)
    stressed["ml_predicted_time"] = model.predict(stressed[features])
    stressed_safe = apply_safety_logic(stressed)
    stressed_best = recommend_routes(stressed_safe).iloc[0]

    return base_best, stressed_best
