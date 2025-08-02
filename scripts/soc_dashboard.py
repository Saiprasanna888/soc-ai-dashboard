import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from ml_triage import load_and_preprocess, load_model
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Config
DATASET_FILE = "data/incident_event_log.csv"

# Auto-refresh every 60 seconds
count = st_autorefresh(interval=60 * 1000, key="data_refresh")

# Page setup
st.set_page_config(page_title="SOC AI Agent Dashboard", layout="wide")
st.title("🚨 SOC AI Agent Dashboard")

# Load data
df = load_and_preprocess(DATASET_FILE)

# Load model
model = load_model()
if model:
    feature_cols = ['priority_num', 'urgency_num']
    predictions = model.predict(df[feature_cols])
    df['ml_triage_label'] = predictions
else:
    st.error("❌ Model not found. Please train the model first.")
    st.stop()

# Track new alerts
if "prev_count" not in st.session_state:
    st.session_state.prev_count = 0

new_alerts = len(df) - st.session_state.prev_count
if new_alerts > 0:
    st.markdown(
        f"""
        <div style="background-color:#ff4d4d;padding:10px;border-radius:8px;text-align:center;color:white;font-size:18px;">
            🚨 <b>{new_alerts} New Alerts Detected!</b> (Auto-refreshed)
        </div>
        """,
        unsafe_allow_html=True
    )

st.session_state.prev_count = len(df)

# Tabs for navigation
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔥 High Priority Alerts", "📁 All Alerts"])

with tab1:
    st.subheader("📊 Dashboard Overview")

    total_alerts = len(df)
    high_priority = df['ml_triage_label'].sum()
    last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Alerts", total_alerts)
    col2.metric("High Priority Alerts", high_priority)
    col3.metric("Last Update", last_update)

    # Chart - Distribution of Alerts
    alert_counts = df['ml_triage_label'].value_counts().reset_index()
    alert_counts.columns = ['Alert Type', 'Count']
    alert_counts['Alert Type'] = alert_counts['Alert Type'].map({0: 'Normal', 1: 'High Priority'})

    fig = px.bar(
        alert_counts,
        x='Alert Type',
        y='Count',
        labels={'Alert Type': 'Alert Type', 'Count': 'Number of Alerts'},
        title="Distribution of Alerts",
        color='Alert Type',
        text='Count'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("🔥 High Priority Alerts")
    high_priority_alerts = df[df['ml_triage_label'] == 1]

    if not high_priority_alerts.empty:
        st.dataframe(high_priority_alerts[['number', 'priority', 'urgency', 'incident_state', 'opened_at']], use_container_width=True)
    else:
        st.info("✅ No high priority alerts at the moment.")

with tab3:
    st.subheader("📁 All Alerts")

    # Incident state filter
    states = df['incident_state'].dropna().unique().tolist()
    selected_state = st.selectbox("Filter by Incident State", ["All"] + states)

    filtered_df = df if selected_state == "All" else df[df['incident_state'] == selected_state]

    st.dataframe(filtered_df[['number', 'priority', 'urgency', 'incident_state', 'opened_at']], use_container_width=True)






