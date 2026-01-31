import matplotlib.pyplot as plt
import streamlit as st

def show_basic_stats(df):
    st.subheader("Dataset Overview")
    st.write(df)

    st.subheader("Summary Statistics")
    st.write(df.describe())

def plot_risk_by_route(df):
    st.subheader("Risk Level by Route")
    fig, ax = plt.subplots()
    ax.bar(df["route_id"], df["risk_level"])
    st.pyplot(fig)

def plot_evac_time(df):
    st.subheader("Estimated Evacuation Time (minutes)")
    fig, ax = plt.subplots()
    ax.bar(df["route_id"], df["est_evac_time_min"])
    ax.set_ylabel("Minutes")
    st.pyplot(fig)

