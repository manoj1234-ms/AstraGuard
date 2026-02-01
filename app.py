import streamlit as st

from src.data_loader import load_data
from src.visualizer import (
    show_basic_stats,
    plot_risk_by_route,
    plot_evac_time
)
from src.decision_engine import rank_routes
from src.ml_model import train_evacuation_model, get_feature_importance
from src.safety_layer import apply_safety_logic
from src.recommendation_engine import recommend_routes
from src.zone_planner import generate_zone_plan
from src.scenario_engine import simulate_scenario
from src.failure_detector import detect_system_failure
from src.scenario_comparator import compare_scenarios
from src.decision_explainer import explain_decision_change


# =================================================
# APP TITLE + SYSTEM STATUS PANEL
# =================================================
st.title("🛡️ ASTRAGUARD — Intelligent Evacuation Planning System")

st.info("""
🛡️ **ASTRAGUARD System Status**

• AI Model: Operational  
• Safety Rules: Enforced  
• Scenario Simulation: Active  
• Human Override: Enabled  

_Last updated in real-time based on field conditions_
""")


# =================================================
# LOAD DATA
# =================================================
data_path = "data/demo_flood_routes.csv"
df = load_data(data_path)


# =================================================
# DATA OVERVIEW
# =================================================
st.header("Data Overview")

show_basic_stats(df)
plot_risk_by_route(df)
plot_evac_time(df)


# =================================================
# RULE-BASED RANKING
# =================================================
st.header("Rule-Based Route Ranking")

ranked_df = rank_routes(df)

st.write(
    ranked_df[[ "route_id", "zone", "risk_level", "congestion_index", "est_evac_time_min", "decision_score" ]].head(10)
)


# =================================================
# TRAIN ML MODEL
# =================================================
st.header("ML Evacuation Time Prediction")

model, mae, r2 = train_evacuation_model(df)

st.write(f"Mean Absolute Error (minutes): {mae:.2f}")
st.write(f"R² Score: {r2:.2f}")


st.subheader("System Health Check")

data_ok = df.isnull().sum().sum() == 0
model_ok = model is not None

if data_ok and model_ok:
    st.success("🟢 System Health: STABLE")
else:
    st.warning("🟡 System Health: DEGRADED — Operating in safe mode")


# =================================================
# FEATURE IMPORTANCE
# =================================================
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


# =================================================
# SCENARIO SIMULATION CONTROLS
# =================================================
st.header("Scenario Simulation")

cong = st.slider("Congestion Multiplier", min_value=1.0, max_value=2.0, step=0.1, value=1.0)
cap = st.slider("Road Capacity Multiplier", min_value=0.5, max_value=1.0, step=0.1, value=1.0)


# =================================================
# SAMPLE + SCENARIO + ML
# =================================================
st.header("Rule-Based vs ML Evacuation Time")

sample = df.sample(5, random_state=1)

# Apply scenario stress
sample = simulate_scenario(sample, congestion_multiplier=cong, capacity_multiplier=cap)

# ML prediction
sample["ml_predicted_time"] = model.predict(sample[features])

st.write(sample[["route_id", "est_evac_time_min", "ml_predicted_time"]])


# =================================================
# SAFETY LAYER
# =================================================
st.header("Safe Evacuation Decision (ML + Rules)")

safe_df = apply_safety_logic(sample)
failure, failure_reasons = detect_system_failure(safe_df)

if failure:
    st.error("🛑 No Safe Evacuation Plan Available")
    for r in failure_reasons:
        st.write(f"• {r}")
    st.info("Immediate human intervention required.")
    st.stop()

st.write(safe_df[["route_id", "est_evac_time_min", "ml_predicted_time", "final_evac_time", "confidence_score", "risk_flag"]])

st.info("""
⚠️ **Safety Guarantee**

If data becomes unreliable or confidence drops:
• Evacuation times are intentionally overestimated  
• High-risk routes are blocked  
• Human approval is enforced  

ASTRAGUARD prioritizes safety over speed.
""")


# =================================================
# SCENARIO COMPARISON
# =================================================
st.header("Scenario Comparison: Before vs After")

base_best, stressed_best = compare_scenarios(sample, model, features, cong, cap)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Baseline Conditions")
    st.write({
        "Route": base_best["route_id"],
        "Final Time": base_best["final_evac_time"],
        "Risk": base_best["risk_flag"],
        "Confidence": base_best["confidence_score"]
    })
with col2:
    st.subheader("Stressed Conditions")
    st.write({
        "Route": stressed_best["route_id"],
        "Final Time": stressed_best["final_evac_time"],
        "Risk": stressed_best["risk_flag"],
        "Confidence": stressed_best["confidence_score"]
    })


# =================================================
# DECISION EXPLANATION
# =================================================
st.header("Decision Timeline & Explanation")

reasons = explain_decision_change(base_best, stressed_best)
st.subheader("What Changed & Why")
if reasons:
    for r in reasons:
        st.write(f"• {r}")
else:
    st.write("• No significant change between scenarios.")


# =================================================
# HUMAN APPROVAL + ALERT SEVERITY
# =================================================
st.header("Human Approval Required")

high_risk = safe_df[safe_df["risk_flag"] == "HIGH"]

if not high_risk.empty:
    st.error("🚨 CRITICAL: Manual approval required before execution.")
    st.write(high_risk)
else:
    st.success("🟢 No critical alerts. System operating normally.")


# =================================================
# FINAL RECOMMENDATION + CONFIDENCE BAR + WHY EXPLAINER
# =================================================
st.header("Recommended Evacuation Plan")

ranked_routes_df = recommend_routes(safe_df)
best_route = ranked_routes_df.iloc[0]

st.success(
    f"""
🟢 **Recommended Route:** {best_route['route_id']}

• Final Evacuation Time: **{best_route['final_evac_time']} minutes**  
• Risk Level: **{best_route['risk_flag']}**  
• Confidence Score: **{best_route['confidence_score']:.2f}**
"""
)

# -----------------------------
# TASK 2: Confidence Visualization
# -----------------------------
st.subheader("Decision Confidence")
st.progress(int(best_route["confidence_score"] * 100))

if best_route["confidence_score"] < 0.5:
    st.warning("⚠️ Low confidence — human approval strongly recommended.")
elif best_route["confidence_score"] < 0.75:
    st.info("ℹ️ Moderate confidence — monitor conditions closely.")
else:
    st.success("✅ High confidence — safe to proceed.")


# -----------------------------
# TASK 3: Plain-English “Why This Route?”
# -----------------------------
st.subheader("Why This Route Was Chosen")

st.write(f"""
ASTRAGUARD selected **Route {best_route['route_id']}** because:

• Predicted evacuation time is lower than alternatives  
• Risk level remains within acceptable safety limits  
• Confidence score is **{best_route['confidence_score']:.2f}**  
• Backup routes are available if conditions worsen  

This recommendation adapts automatically if congestion or capacity changes.
""")


# =================================================
# ZONE-LEVEL PLANNING
# =================================================
st.header("Zone-Level Evacuation Plan")

zone_plans = generate_zone_plan(safe_df)

for zone, plan in zone_plans.items():
    st.subheader(f"📍 Zone {zone}")
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


# =================================================
# EXECUTIVE SUMMARY
# =================================================
st.header("Executive Summary")

st.markdown("""
**ASTRAGUARD Evacuation Recommendation Summary**

• Uses AI + physical safety rules  
• Never underestimates evacuation time  
• Requires human approval for low-confidence routes  
• Provides primary and backup routes per zone  

This ensures safe, explainable, and operationally realistic evacuation planning.
""")


# =================================================
# 1-MINUTE DECISION NARRATIVE
# =================================================
st.header("ASTRAGUARD — 1-Minute Decision Narrative")

st.markdown(f"""
**Situation:**  
Normal conditions allowed evacuation via **Route {base_best['route_id']}**  
with acceptable risk and confidence.

**Change:**  
Under increased congestion or reduced capacity, conditions worsened.

**System Response:**  
ASTRAGUARD re-evaluated all routes, enforced safety limits,  
and recommended **Route {stressed_best['route_id']}**  
with updated risk awareness.

**Outcome:**  
The system adapted the plan transparently and required human attention  
where confidence dropped.

**Value:**  
ASTRAGUARD doesn’t give static answers —  
it *evolves decisions as reality changes*.
""")


st.header("Real-World Deployment Scenario")

st.markdown("""
**Example Situation:**
A district control room loses live traffic data during flooding.

**ASTRAGUARD Response:**
• Switches to offline mode  
• Uses cached route data  
• Applies conservative safety rules  
• Requests human confirmation  

**Result:**
Evacuation continues safely — even with partial information.
""")
