import streamlit as st
from src.data_loader import load_data
from src.visualizer import show_basic_stats , plot_risk_by_route ,plot_evac_time
from src.decision_engine import rank_routes

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
