import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.title("Activity Recognition & Safety Monitoring Dashboard")

log = pd.read_csv("activity_tracking_log.csv")

st.subheader("Recent Activity Log")
st.dataframe(log.head(20))
latest = log.iloc[-1]

st.metric("Current Activity", latest["predicted_activity"])
st.metric("Fall Detected", "YES" if latest["fall_detected"] else "NO")
st.metric("Risk Level", latest["risk_level"])
st.subheader("Activity Tracking Over Time")

fig, ax = plt.subplots(figsize=(10,4))
ax.plot(log["timestamp"][:200], log["predicted_activity"][:200], marker="o")
plt.xticks(rotation=45)

st.pyplot(fig)
st.subheader("Fall Detection Visualization")
st.image("fall_detection_dashboard.png")
st.subheader("Risk Level Distribution")
st.bar_chart(log["risk_level"].value_counts())
