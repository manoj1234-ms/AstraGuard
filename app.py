import streamlit as st
from src.data_loader import load_data
from src.visualizer import show_basic_stats , plot_risk_by_route ,plot_evac_time
from src.decision_engine import rank_routes
from src.ml_model import train_evacuation_model , get_feature_importance
from src.safety_layer import apply_safety_logic
from src.recommendation_engine import recommend_routes
from src.zone_planner import generate_zone_plan


st.title("ASTRAGUARD — Data Ingestion")

data_path = "data/demo_flood_routes.csv"

df = load_data(data_path)

show_basic_stats(df)
plot_risk_by_route(df)
plot_evac_time(df)

st.subheader("Recommended Routes")


ranked_df = rank_routes(df)

st.write(
    ranked_df[[
        "route_id",
        "zone",
        "risk_level",
        "congestion_index",
        "est_evac_time_min",
        "decision_score"
    ]].head(10)
)

st.subheader("ML Evacuation Time Prediction")

model, mae, r2 = train_evacuation_model(df)

st.write(f"Mean Absolute Error (minutes): {mae:.2f}")
st.write(f"R² Score: {r2:.2f}")

st.subheader("Why the Model Decides This")

features = [
    "population",
    "risk_level",
    "road_capacity",
    "distance_km",
    "avg_speed_kmph",
    "load_factor",
    "congestion_index",
]

importance = get_feature_importance(model, features)

st.write("Feature Importance (High → Low):")
st.write(importance)


st.subheader("Rule-Based vs ML Evacuation Time")

sample = df.sample(5, random_state=1)

sample["ml_predicted_time"] = model.predict(sample[features])

comparison = sample[[
    "route_id",
    "est_evac_time_min",
    "ml_predicted_time"
]]

st.write(comparison)

st.subheader("Safe Evacuation Decision (ML + Rules)")

sample = df.sample(5, random_state=1)
sample["ml_predicted_time"] = model.predict(sample[features])

safe_df = apply_safety_logic(sample)

st.write(
    safe_df[[
        "route_id",
        "est_evac_time_min",
        "ml_predicted_time",
        "final_evac_time",
        "confidence_score",
        "risk_flag"
    ]]
)

st.subheader("Human Approval Required")

high_risk = safe_df[safe_df["risk_flag"] == "HIGH"]

if not high_risk.empty:
    st.warning("⚠️ Some routes require manual approval due to low confidence.")
    st.write(high_risk)
else:
    st.success("✅ All recommendations are within safe confidence limits.")


st.subheader("Recommended Evacuation Plan")

ranked_routes = recommend_routes(safe_df)

best_route = ranked_routes.iloc[0]

st.success(
    f"""
    🟢 Recommended Route: {best_route['route_id']}
    
    Final Evacuation Time: {best_route['final_evac_time']} minutes  
    Risk Level: {best_route['risk_flag']}  
    Confidence Score: {best_route['confidence_score']}
    """
)

st.write("Full Ranked List")
st.write(
    ranked_routes[[
        "route_id",
        "final_evac_time",
        "risk_flag",
        "confidence_score"
    ]]
)

st.subheader("Zone-Level Evacuation Plan")

zone_plans = generate_zone_plan(safe_df)

for zone, plan in zone_plans.items():
    st.markdown(f"### 📍 Zone {zone}")

    primary = plan.iloc[0]
    backup = plan.iloc[1] if len(plan) > 1 else None

    st.success(
        f"""
        **Primary Route:** {primary['route_id']}  
        Final Time: {primary['final_evac_time']} min  
        Risk: {primary['risk_flag']}  
        Confidence: {primary['confidence_score']}
        """
    )

    if backup is not None:
        st.info(
            f"""
            **Backup Route:** {backup['route_id']}  
            Final Time: {backup['final_evac_time']} min  
            Risk: {backup['risk_flag']}  
            Confidence: {backup['confidence_score']}
            """
        )

st.subheader("Executive Summary")

st.markdown("""
**ASTRAGUARD Evacuation Recommendation Summary**

• Routes are selected using a combination of physical safety rules and AI predictions  
• The system never underestimates evacuation time  
• Low-confidence AI recommendations require human approval  
• Each zone receives a primary and backup evacuation route  

This ensures safe, explainable, and practical evacuation planning.
""")
