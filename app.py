import streamlit as st
from src.data_loader import load_data
from src.visualizer import show_basic_stats , plot_risk_by_route ,plot_evac_time


st.title("ASTRAGUARD — Data Ingestion")

data_path = "data/demo_flood_routes.csv"

df = load_data(data_path)

show_basic_stats(df)
plot_risk_by_route(df)
plot_evac_time(df)