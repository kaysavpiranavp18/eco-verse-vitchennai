import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title= "Activity & Safety Monitor",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🏃 Activity Recognition & Motion-Based Safety Monitoring System</h1>', unsafe_allow_html=True)

# Check for required files
model_exists = Path("activity_model.pkl").exists()
log_exists = Path("activity_tracking_log.csv").exists()
test_exists = Path("data/test.csv").exists() or Path("test.csv").exists()

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/activity-history.png", width=80)
    st.title("Navigation")
    
    # Mode selection
    available_modes = []
    
    if log_exists:
        available_modes.append("📊 Historical Dashboard")
    
    if model_exists and test_exists:
        available_modes.append("🔴 Live Simulation")
    
    if test_exists:
        available_modes.append("📈 Dataset Explorer")
    
    if not available_modes:
        st.error("No data sources available!")
        st.stop()
    
    mode = st.radio("Select Mode:", available_modes)
    
    st.divider()
    st.info("This system monitors human activities and detects safety risks in real-time using advanced ML algorithms.")
    
    # Statistics
    if log_exists:
        log_data = pd.read_csv("activity_tracking_log.csv")
        st.metric("Total Records", len(log_data))
        if "fall_detected" in log_data.columns:
            st.metric("Falls Detected", log_data["fall_detected"].sum())


# ====================================
# MODE 1: HISTORICAL DASHBOARD
# ====================================
if mode == "📊 Historical Dashboard":
    st.header("📊 Historical Activity Dashboard")
    
    log = pd.read_csv("activity_tracking_log.csv")
    
    # Top metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    latest = log.iloc[-1]
    
    with col1:
        st.metric("🏃 Current Activity", latest.get("predicted_activity", "N/A"))
    
    with col2:
        fall_status = "YES ⚠️" if latest.get("fall_detected", False) else "NO ✓"
        st.metric("🚨 Fall Detected", fall_status)
    
    with col3:
        risk = latest.get("risk_level", "Unknown")
        st.metric("⚡ Risk Level", risk)
    
    with col4:
        st.metric("📝 Total Records", len(log))
    
    st.divider()
    
    # Two column layout
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("📋 Recent Activity Log")
        display_count = st.slider("Number of records to display:", 5, 50, 20)
        st.dataframe(log.head(display_count), use_container_width=True, height=300)
    
    with col_right:
        st.subheader("📊 Risk Distribution")
        if "risk_level" in log.columns:
            risk_counts = log["risk_level"].value_counts()
            fig_risk, ax_risk = plt.subplots(figsize=(6, 4))
            colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
            ax_risk.bar(risk_counts.index, risk_counts.values, 
                       color=[colors.get(x, '#6366f1') for x in risk_counts.index])
            ax_risk.set_xlabel('Risk Level')
            ax_risk.set_ylabel('Count')
            ax_risk.set_title('Risk Level Distribution')
            plt.xticks(rotation=45)
            st.pyplot(fig_risk)
    
    st.divider()
    
    # Activity tracking over time
    st.subheader("⏱️ Activity Tracking Over Time")
    
    chart_range = st.slider("Select data range:", 50, min(500, len(log)), min(200, len(log)))
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    if "timestamp" in log.columns:
        timestamps = log["timestamp"][:chart_range]
        activities = log["predicted_activity"][:chart_range]
        
        # Create numeric mapping for activities
        unique_activities = activities.unique()
        activity_map = {act: i for i, act in enumerate(unique_activities)}
        numeric_activities = [activity_map[act] for act in activities]
        
        ax.plot(range(len(timestamps)), numeric_activities, marker="o", markersize=3, linewidth=1)
        ax.set_yticks(range(len(unique_activities)))
        ax.set_yticklabels(unique_activities)
        ax.set_xlabel('Time Index')
        ax.set_ylabel('Activity')
        ax.grid(True, alpha=0.3)
    else:
        ax.plot(log["predicted_activity"][:chart_range].value_counts())
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    
    # Fall detection visualization
    st.divider()
    st.subheader("🚨 Fall Detection Visualization")
    
    if Path("fall_detection_dashboard.png").exists():
        st.image("fall_detection_dashboard.png", use_container_width=True)
    else:
        st.info("Fall detection visualization image not found.")


# ====================================
# MODE 2: LIVE SIMULATION
# ====================================
elif mode == "🔴 Live Simulation":
    st.header("🔴 Live Activity Monitoring Simulation")
    
    # Check for model
    if not model_exists:
        st.error("❌ Model file 'activity_model.pkl' not found! Please train the model first.")
        st.info("💡 Run the Jupyter notebook 'activity_recognition.ipynb' to train and save the model.")
        st.stop()
    
    import joblib
    
    # Load model
    try:
        model = joblib.load("activity_model.pkl")
        st.success("✅ Model loaded successfully!")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()
    
    # Load test data
    test_path = "data/test.csv" if Path("data/test.csv").exists() else "test.csv"
    df = pd.read_csv(test_path)
    
    st.info(f"🔄 Live simulation using {len(df)} samples from test dataset")
    
    # Feature prediction
    X = df.drop(columns=["Activity", "subject"], errors='ignore')
    df["Predicted Activity"] = model.predict(X)
    
    # Movement magnitude calculation
    df["acc_mag"] = np.sqrt(
        (df["tBodyAcc-mean()-X"] ** 2) +
        (df["tBodyAcc-mean()-Y"] ** 2) +
        (df["tBodyAcc-mean()-Z"] ** 2)
    )
    
    mean_mag = df["acc_mag"].mean()
    std_mag = df["acc_mag"].std()
    
    # Anomaly thresholds
    threshold = mean_mag + 2 * std_mag
    alert_threshold = mean_mag + 3.5 * std_mag
    
    df["Possible_Fall"] = df["acc_mag"] > threshold
    df["High_Risk_Alert"] = df["acc_mag"] > alert_threshold
    
    # Fall pattern detection
    df["Fall_Event"] = False
    for i in range(1, len(df)-1):
        if df["Possible_Fall"].iloc[i] and df["acc_mag"].iloc[i+1] < mean_mag:
            df.loc[i, "Fall_Event"] = True
    
    # Control panel
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        start_simulation = st.button("▶️ Start Simulation", type="primary", use_container_width=True)
    
    with col2:
        simulation_speed = st.select_slider("Speed", options=[0.1, 0.3, 0.5, 1.0, 2.0], value=0.5)
    
    with col3:
        max_samples = st.number_input("Max Samples", min_value=10, max_value=len(df), value=min(100, len(df)))
    
    st.divider()
    
    # Live monitoring placeholder
    if start_simulation:
        st.subheader("🎯 Live Monitoring")
        
        # Placeholders
        placeholder_metrics = st.empty()
        placeholder_status = st.empty()
        placeholder_chart = st.empty()
        progress_bar = st.progress(0)
        
        i = 0
        while i < min(max_samples, len(df)):
            current_row = df.iloc[i:i+1]
            
            activity = current_row["Predicted Activity"].iloc[0]
            motion = current_row["acc_mag"].iloc[0]
            is_anomaly = current_row["Possible_Fall"].iloc[0]
            is_alert = current_row["High_Risk_Alert"].iloc[0]
            is_fall = current_row["Fall_Event"].iloc[0]
            
            # Calculate risk score
            risk = 0
            risk += min((motion / mean_mag) * 25, 25)
            if is_anomaly:
                risk += 25
            if is_alert:
                risk += 25
            if is_fall:
                risk += 25
            risk = int(min(risk, 100))
            
            # Display metrics
            with placeholder_metrics.container():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🏃 Activity", activity)
                
                with col2:
                    st.metric("📊 Motion", f"{motion:.3f}")
                
                with col3:
                    st.metric("🛡️ Risk Score", f"{risk}/100")
                
                with col4:
                    st.metric("📍 Sample", f"{i+1}/{max_samples}")
            
            # Display status
            with placeholder_status.container():
                if is_fall:
                    st.error("🚨 **CRITICAL: Likely FALL detected!**")
                elif is_alert:
                    st.error("⚠️ **HIGH RISK: Significant motion spike detected**")
                elif is_anomaly:
                    st.warning("🔎 **CAUTION: Unusual movement pattern**")
                else:
                    st.success("✅ **NORMAL: Movement within safe parameters**")
                
                # Risk level indicator
                if risk < 30:
                    st.success("🟢 Low Risk - Stable condition")
                elif risk < 60:
                    st.warning("🟡 Medium Risk - Monitor closely")
                elif risk < 85:
                    st.error("🟠 High Risk - Potential danger")
                else:
                    st.error("🔴 CRITICAL - Immediate attention required!")
            
            # Update progress
            progress_bar.progress((i + 1) / max_samples)
            
            time.sleep(simulation_speed)
            i += 1
        
        st.success("✅ Simulation completed!")
    
    # Summary statistics
    st.divider()
    st.header("📊 Simulation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔎 Anomaly Detection")
        anomaly_count = df['Possible_Fall'].sum()
        st.metric("Unusual Movements", anomaly_count)
        st.progress(min(anomaly_count / len(df), 1.0))
    
    with col2:
        st.subheader("🚨 Fall Detection")
        fall_count = df["Fall_Event"].sum()
        if fall_count > 0:
            st.error(f"⚠️ {fall_count} fall events detected")
        else:
            st.success("✅ No falls detected")
    
    with col3:
        st.subheader("⚠️ Safety Alerts")
        alert_count = df["High_Risk_Alert"].sum()
        if alert_count > 0:
            st.warning(f"📢 {alert_count} high-risk alerts")
        else:
            st.success("✅ No alerts")
    
    st.divider()
    st.subheader("📈 Activity Distribution")
    st.bar_chart(df["Predicted Activity"].value_counts())


# ====================================
# MODE 3: DATASET EXPLORER
# ====================================
elif mode == "📈 Dataset Explorer":
    st.header("📈 Dataset Explorer")
    
    test_path = "data/test.csv" if Path("data/test.csv").exists() else "test.csv"
    
    if Path(test_path).exists():
        df = pd.read_csv(test_path)
        
        st.success(f"✅ Loaded {len(df)} samples from test dataset")
        
        # Dataset info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Samples", len(df))
        
        with col2:
            st.metric("Features", len(df.columns))
        
        with col3:
            if "Activity" in df.columns:
                st.metric("Activities", df["Activity"].nunique())
        
        st.divider()
        
        # Show sample data
        st.subheader("📋 Sample Data")
        st.dataframe(df.head(20), use_container_width=True)
        
        st.divider()
        
        # Activity distribution
        if "Activity" in df.columns:
            st.subheader("🎯 Activity Distribution")
            activity_counts = df["Activity"].value_counts()
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(activity_counts.index, activity_counts.values, color='#667eea')
            ax.set_xlabel('Activity Type')
            ax.set_ylabel('Count')
            ax.set_title('Distribution of Activities in Dataset')
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
        
        # Feature statistics
        st.divider()
        st.subheader("📊 Feature Statistics")
        st.dataframe(df.describe(), use_container_width=True)
        
    else:
        st.error("❌ Test dataset not found!")


# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Activity Recognition & Motion-Based Safety Monitoring System</strong></p>
    <p>Powered by Machine Learning | Real-time Activity Recognition & Fall Detection</p>
</div>
""", unsafe_allow_html=True)
