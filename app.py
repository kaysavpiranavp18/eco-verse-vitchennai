import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
import os
from pathlib import Path
from alert_system import SafetyAlertSystem, format_alert_message

# Initialize session state for current simulation alerts
if 'current_session_alerts' not in st.session_state:
    st.session_state.current_session_alerts = []
if 'current_session_samples' not in st.session_state:
    st.session_state.current_session_samples = 0
if 'simulation_completed' not in st.session_state:
    st.session_state.simulation_completed = False

# Initialize session state for Health Trend Dashboard (accumulates across all sessions)
if 'health_history' not in st.session_state:
    st.session_state.health_history = pd.DataFrame()
if 'simulation_active' not in st.session_state:
    st.session_state.simulation_active = False

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
    
    # Alert system is always available
    available_modes.append("🚨 Safety Alert System")
    
    # Health Trend Dashboard is always available
    available_modes.append("📅 Health Trend Dashboard")
    
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
            ax_risk.bar(risk_counts.index, risk_counts.values.astype(int), 
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
    st.subheader("🚨 Fall Detection Analysis")
    
    # Check if fall_detected column exists
    if "fall_detected" in log.columns:
        fall_data = log.copy()
        
        # Convert fall_detected to boolean if needed
        if fall_data["fall_detected"].dtype == 'object':
            fall_data["fall_detected"] = fall_data["fall_detected"].map({True: True, 'True': True, 1: True, False: False, 'False': False, 0: False})
        
        # Fall statistics
        total_falls = fall_data["fall_detected"].sum()
        total_samples = len(fall_data)
        fall_percentage = (total_falls / total_samples * 100) if total_samples > 0 else 0
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🚨 Total Falls", int(total_falls))
        
        with col2:
            st.metric("📊 Total Samples", total_samples)
        
        with col3:
            st.metric("📈 Fall Rate", f"{fall_percentage:.2f}%")
        
        with col4:
            fall_status = "🔴 CRITICAL" if total_falls > 5 else "🟡 WARNING" if total_falls > 0 else "🟢 SAFE"
            st.metric("⚡ Status", fall_status)
        
        st.divider()
        
        # Create visualizations
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📍 Fall Events Timeline")
            
            # Get subset for visualization
            viz_range = min(500, len(fall_data))
            viz_data = fall_data.head(viz_range)
            
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            
            # Plot all data points
            indices = range(len(viz_data))
            fall_indices = viz_data[viz_data["fall_detected"] == True].index.tolist()
            
            # Background line showing all samples
            ax1.plot(indices, [0.5] * len(indices), 'o', markersize=2, color='lightgray', alpha=0.3, label='Normal')
            
            # Highlight fall events
            if fall_indices:
                fall_positions = [i for i in indices if i in fall_indices]
                ax1.scatter(fall_positions, [0.5] * len(fall_positions), 
                           color='red', s=100, marker='X', label='Fall Detected', zorder=5)
            
            ax1.set_xlabel('Sample Index')
            ax1.set_ylabel('Event')
            ax1.set_title(f'Fall Events in First {viz_range} Samples')
            ax1.set_ylim(0, 1)
            ax1.set_yticks([0.5])
            ax1.set_yticklabels(['Activity Stream'])
            ax1.legend(loc='upper right')
            ax1.grid(True, alpha=0.3, axis='x')
            
            st.pyplot(fig1)
        
        with col_right:
            st.subheader("⚡ Risk Level Distribution")
            
            if "risk_level" in fall_data.columns:
                risk_counts = fall_data["risk_level"].value_counts()
                
                fig2, ax2 = plt.subplots(figsize=(8, 5))
                
                # Color mapping
                colors = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#ef4444'}
                bar_colors = [colors.get(level, '#6366f1') for level in risk_counts.index]
                
                bars = ax2.bar(risk_counts.index, risk_counts.values.astype(int), color=bar_colors, edgecolor='black', linewidth=1.5)
                
                # Add value labels on bars
                for bar in bars:
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width()/2., height,
                            f'{int(height)}',
                            ha='center', va='bottom', fontsize=12, fontweight='bold')
                
                ax2.set_xlabel('Risk Level', fontsize=12)
                ax2.set_ylabel('Count', fontsize=12)
                ax2.set_title('Distribution of Risk Levels', fontsize=14, fontweight='bold')
                ax2.grid(True, alpha=0.3, axis='y')
                
                st.pyplot(fig2)
            else:
                st.info("Risk level data not available")
        
        # Detailed fall event list
        if total_falls > 0:
            st.divider()
            st.subheader("📋 Detailed Fall Events")
            
            fall_events = fall_data[fall_data["fall_detected"] == True].copy()
            fall_events = fall_events.reset_index(drop=True)
            fall_events.index = fall_events.index + 1  # Start from 1
            
            # Display table
            st.dataframe(
                fall_events[["timestamp", "predicted_activity", "risk_level"]].head(20),
                use_container_width=True
            )
            
            if len(fall_events) > 20:
                st.info(f"Showing first 20 of {len(fall_events)} fall events")
        else:
            st.success("✅ No fall events detected in the activity log!")
    else:
        st.warning("⚠️ Fall detection data not available in the log file")


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
    
    # Initialize alert system
    alert_system = SafetyAlertSystem()
    alert_system.clear_session_alerts()  # Clear previous session alerts
    
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
    
    # Fall detection using supervised model from fall_detection.ipynb
    fall_model_path = "fall_detection_model.pkl" if Path("fall_detection_model.pkl").exists() else None
    
    if fall_model_path and Path(fall_model_path).exists():
        try:
            # Load the trained fall detection model
            fall_model = joblib.load(fall_model_path)
            
            # Extract features for fall detection (using same features as training)
            FEATURE_COLS = [
                "tBodyAcc-mean()-X", "tBodyAcc-mean()-Y", "tBodyAcc-mean()-Z",
                "tBodyAcc-std()-X", "tBodyAcc-std()-Y", "tBodyAcc-std()-Z",
                "tBodyAcc-max()-X", "tBodyAcc-max()-Y", "tBodyAcc-max()-Z",
                "tBodyAcc-min()-X", "tBodyAcc-min()-Y", "tBodyAcc-min()-Z",
                "tGravityAcc-mean()-X", "tGravityAcc-mean()-Y", "tGravityAcc-mean()-Z"
            ]
            
            # Use available features that match the model's training features
            available_cols = [col for col in FEATURE_COLS if col in df.columns]
            
            if available_cols:
                X_fall = df[available_cols].values
                df["Fall_Event"] = fall_model.predict(X_fall).astype(bool)
                st.success("✅ Using supervised fall detection model from fall_detection.ipynb")
            else:
                # Fallback to heuristic if features not available
                df["Fall_Event"] = False
                for i in range(1, len(df)-1):
                    if df["Possible_Fall"].iloc[i] and df["acc_mag"].iloc[i+1] < mean_mag:
                        df.loc[i, "Fall_Event"] = True
                st.warning("⚠️ Required features not available, using heuristic fall detection")
                
        except Exception as e:
            # Fallback to motion-based heuristic if model fails
            st.warning(f"⚠️ Could not load fall model ({e}), using heuristic detection")
            df["Fall_Event"] = False
            for i in range(1, len(df)-1):
                if df["Possible_Fall"].iloc[i] and df["acc_mag"].iloc[i+1] < mean_mag:
                    df.loc[i, "Fall_Event"] = True
    else:
        # Fallback to motion-based heuristic
        st.info("ℹ️ Supervised fall detection model not found, using motion-based heuristic")
        df["Fall_Event"] = False
        for i in range(1, len(df)-1):
            if df["Possible_Fall"].iloc[i] and df["acc_mag"].iloc[i+1] < mean_mag:
                df.loc[i, "Fall_Event"] = True
    
    # Control panel
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        start_simulation = st.button("▶️ Start Simulation", type="primary", use_container_width=True)
    
    with col2:
        simulation_speed = st.select_slider("Speed", options=[0.1, 0.3, 0.5, 1.0, 2.0], value=0.5)
    
    with col3:
        max_samples = st.number_input("Max Samples", min_value=10, max_value=len(df), value=min(100, len(df)))
    
    with col4:
        enable_alerts = st.checkbox("🚨 Enable Alerts", value=True, help="Generate and log safety alerts during simulation")
    
    st.divider()
    
    # Live monitoring placeholder
    if start_simulation:
        # Clear previous session data when starting new simulation
        st.session_state.current_session_alerts = []
        st.session_state.current_session_samples = 0
        st.session_state.simulation_completed = False
        
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
            
            # Generate safety alert if enabled
            current_alert = None
            if enable_alerts:
                current_alert = alert_system.generate_alert(
                    activity=activity,
                    risk_score=risk,
                    motion_intensity=motion,
                    is_fall=is_fall,
                    is_anomaly=is_anomaly,
                    is_high_alert=is_alert,
                    sample_index=i
                )
                
                # Store alert in session state for later viewing
                if current_alert:
                    st.session_state.current_session_alerts.append(current_alert)
                
                # Save critical alerts to log immediately
                if current_alert and current_alert['severity'] in ['CRITICAL', 'EMERGENCY']:
                    alert_system.save_alert_to_log(current_alert)
            
            # Append to Health Trend Dashboard history
            health_entry = pd.DataFrame([{
                'timestamp': pd.Timestamp.now(),
                'activity': activity,
                'risk': risk,
                'motion': motion,
                'fall': is_fall,
                'alert': is_alert,
                'anomaly': is_anomaly
            }])
            st.session_state.health_history = pd.concat(
                [st.session_state.health_history, health_entry], 
                ignore_index=True
            )
            
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
        
        # Mark simulation as completed and store sample count
        st.session_state.simulation_completed = True
        st.session_state.current_session_samples = max_samples
        
        st.success("✅ Simulation completed!")
        
        # Display alert summary if alerts were enabled
        if enable_alerts:
            st.divider()
            st.subheader("🚨 Alert Summary")
            
            session_summary = alert_system.get_session_summary()
            
            if session_summary['total_alerts'] > 0:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📢 Total Alerts", session_summary['total_alerts'])
                
                with col2:
                    st.metric("🔴 Critical/Emergency", session_summary['critical_count'])
                
                with col3:
                    if st.button("💾 Save All Alerts to Log"):
                        for alert in alert_system.current_session_alerts:
                            alert_system.save_alert_to_log(alert)
                        st.success("Alerts saved to log!")
                
                # Show breakdown by severity
                st.write("**Alerts by Severity:**")
                severity_df = pd.DataFrame({
                    'Severity': list(session_summary['by_severity'].keys()),
                    'Count': list(session_summary['by_severity'].values())
                })
                st.bar_chart(severity_df.set_index('Severity'))
                
                # Show critical alerts
                critical_alerts = [a for a in alert_system.current_session_alerts 
                                 if a['severity'] in ['CRITICAL', 'EMERGENCY']]
                
                if critical_alerts:
                    st.error(f"**⚠️ {len(critical_alerts)} Critical/Emergency Alerts Detected**")
                    
                    with st.expander("View Critical Alerts"):
                        for idx, alert in enumerate(critical_alerts, 1):
                            st.markdown(f"### Alert #{idx}")
                            st.markdown(format_alert_message(alert))
                            st.divider()
            else:
                st.success("✅ No safety alerts were generated during this simulation")
    
    # Summary statistics - Only for simulated samples
    st.divider()
    st.header("📊 Simulation Summary")
    
    # Get the range that will be/was simulated
    simulated_range = min(max_samples, len(df))
    simulated_data = df.head(simulated_range)
    
    st.info(f"📍 Analysis based on **{simulated_range}** simulated samples (out of {len(df)} total)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🔎 Anomaly Detection")
        anomaly_count = int(simulated_data['Possible_Fall'].sum())
        anomaly_rate = (anomaly_count / len(simulated_data) * 100) if len(simulated_data) > 0 else 0
        st.metric("Unusual Movements", anomaly_count)
        st.caption(f"{anomaly_rate:.1f}% of simulated samples")
        st.progress(min(anomaly_count / len(simulated_data), 1.0))
    
    with col2:
        st.subheader("🚨 Fall Detection")
        fall_count = int(simulated_data["Fall_Event"].sum())
        fall_rate = (fall_count / len(simulated_data) * 100) if len(simulated_data) > 0 else 0
        if fall_count > 0:
            st.error(f"⚠️ {fall_count} fall events")
            st.caption(f"{fall_rate:.1f}% of simulated samples")
        else:
            st.success("✅ No falls detected")
            st.caption("0% fall rate")
    
    with col3:
        st.subheader("⚠️ Safety Alerts")
        alert_count = int(simulated_data["High_Risk_Alert"].sum())
        alert_rate = (alert_count / len(simulated_data) * 100) if len(simulated_data) > 0 else 0
        if alert_count > 0:
            st.warning(f"📢 {alert_count} high-risk alerts")
            st.caption(f"{alert_rate:.1f}% of simulated samples")
        else:
            st.success("✅ No alerts")
            st.caption("0% alert rate")
    
    st.divider()
    st.subheader("📈 Activity Distribution")
    st.caption(f"Distribution of activities in the {simulated_range} simulated samples")
    
    # Create activity distribution chart
    activity_dist = simulated_data["Predicted Activity"].value_counts()
    st.bar_chart(activity_dist)
    
    # Show detailed breakdown
    st.subheader("📋 Detailed Activity Breakdown")
    col_a, col_b = st.columns(2)
    
    with col_a:
        activity_df = pd.DataFrame({
            'Activity': activity_dist.index,
            'Count': activity_dist.values.astype(int),
            'Percentage': (activity_dist.values.astype(float) / len(simulated_data) * 100).round(2)
        })
        st.dataframe(activity_df, use_container_width=True, hide_index=True)
    
    with col_b:
        # Summary statistics
        st.metric("Total Activities", len(activity_dist))
        st.metric("Most Common", activity_dist.index[0])
        st.metric("Least Common", activity_dist.index[-1])


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
            ax.bar(activity_counts.index, activity_counts.values.astype(int), color='#667eea')
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


# ====================================
# MODE 4: SAFETY ALERT SYSTEM
# ====================================
elif mode == "🚨 Safety Alert System":
    st.header("🚨 Safety Alert Management System")
    st.subheader("Current Session Alerts")
    
    # Initialize alert system
    alert_system = SafetyAlertSystem()
    
    # Check if there are alerts from current simulation session
    if not st.session_state.simulation_completed or len(st.session_state.current_session_alerts) == 0:
        st.info("📝 No alerts from current simulation session. Run a simulation with alerts enabled to generate safety alerts.")
        
        st.markdown("""
        ### How to Generate Alerts:
        
        1. Go to **🔴 Live Simulation** mode
        2. Enable the **🚨 Enable Alerts** checkbox
        3. Run the simulation
        4. Return to this **Safety Alert System** to view the alerts from your simulation
        
        The system will detect and alert for:
        - 🚨 **EMERGENCY**: Fall events
        - 🔴 **CRITICAL**: Dangerous motion spikes
        - ⚠️ **WARNING**: Anomalies and high-risk activities
        - ℹ️ **INFO**: Elevated risk levels
        """)
        
        # Option to view historical alerts
        st.divider()
        st.subheader("📜 Historical Alerts (Previous Sessions)")
        
        if Path(alert_system.alert_log_file).exists():
            if st.checkbox("Show historical alerts from log file"):
                historical_alerts = pd.read_csv(alert_system.alert_log_file)
                st.dataframe(historical_alerts.tail(50), use_container_width=True, height=300)
                st.caption(f"Showing last 50 of {len(historical_alerts)} historical alerts")
        else:
            st.info("No historical alert log file found")
    else:
        # Convert session alerts to DataFrame for analysis
        df_alerts = pd.DataFrame(st.session_state.current_session_alerts)
        
        # Calculate statistics
        total_alerts = len(df_alerts)
        emergency_count = len(df_alerts[df_alerts['severity'] == 'EMERGENCY'])
        critical_count = len(df_alerts[df_alerts['severity'] == 'CRITICAL'])
        warning_count = len(df_alerts[df_alerts['severity'] == 'WARNING'])
        info_count = len(df_alerts[df_alerts['severity'] == 'INFO'])
        avg_risk = df_alerts['risk_score'].mean() if total_alerts > 0 else 0
        
        # Top metrics
        st.subheader("📊 Current Session Overview")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("📢 Total Alerts", total_alerts)
        
        with col2:
            st.metric("🚨 Emergencies", emergency_count)
        
        with col3:
            st.metric("🔴 Critical", critical_count)
        
        with col4:
            st.metric("⚡ Avg Risk", f"{avg_risk:.1f}/100")
        
        with col5:
            st.metric("📊 Samples", st.session_state.current_session_samples)
        
        st.divider()
        
        # Visualizations
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("📊 Alerts by Severity")
            
            severity_counts = df_alerts['severity'].value_counts()
            severity_data = pd.DataFrame({
                'Severity': severity_counts.index,
                'Count': severity_counts.values
            })
            
            fig1, ax1 = plt.subplots(figsize=(8, 5))
            
            colors_map = {
                'INFO': '#3b82f6',
                'WARNING': '#f59e0b',
                'CRITICAL': '#ef4444',
                'EMERGENCY': '#991b1b'
            }
            
            bar_colors = [colors_map.get(s, '#6b7280') for s in severity_data['Severity']]
            bars = ax1.bar(severity_data['Severity'], severity_data['Count'], 
                          color=bar_colors, edgecolor='black', linewidth=1.5)
            
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            ax1.set_xlabel('Severity Level', fontsize=12)
            ax1.set_ylabel('Count', fontsize=12)
            ax1.set_title('Alert Distribution by Severity', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3, axis='y')
            plt.xticks(rotation=0)
            
            st.pyplot(fig1)
        
        with col_right:
            st.subheader("🎯 Alerts by Activity")
            
            activity_counts = df_alerts['activity'].value_counts().head(10)
            activity_data = pd.DataFrame({
                'Activity': activity_counts.index,
                'Count': activity_counts.values
            })
            
            fig2, ax2 = plt.subplots(figsize=(8, 5))
            
            ax2.barh(activity_data['Activity'], activity_data['Count'], color='#8b5cf6')
            ax2.set_xlabel('Alert Count', fontsize=12)
            ax2.set_ylabel('Activity', fontsize=12)
            ax2.set_title('Top 10 Activities with Alerts', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='x')
            
            st.pyplot(fig2)
        
        st.divider()
        
        # Alert type breakdown
        st.subheader("📋 Alert Types")
        
        type_counts = df_alerts['alert_type'].value_counts()
        type_data = pd.DataFrame({
            'Alert Type': type_counts.index,
            'Count': type_counts.values
        })
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.bar_chart(type_data.set_index('Alert Type'))
        
        with col2:
            for _, row in type_data.iterrows():
                st.metric(row['Alert Type'].replace('_', ' ').title(), row['Count'])
        
        st.divider()
        
        # Recent alerts table
        st.subheader("🕐 Recent Alerts from Current Session")
        
        num_recent = st.slider("Number of alerts to display:", 5, min(50, total_alerts), min(20, total_alerts))
        
        # Add filter options
        col1, col2 = st.columns(2)
        
        with col1:
            severity_filter = st.multiselect(
                "Filter by Severity:",
                options=df_alerts['severity'].unique(),
                default=df_alerts['severity'].unique()
            )
        
        with col2:
            type_filter = st.multiselect(
                "Filter by Type:",
                options=df_alerts['alert_type'].unique(),
                default=df_alerts['alert_type'].unique()
            )
        
        # Apply filters
        filtered_alerts = df_alerts[
            (df_alerts['severity'].isin(severity_filter)) &
            (df_alerts['alert_type'].isin(type_filter))
        ].tail(num_recent)
        
        # Display table
        display_columns = ['timestamp', 'severity', 'alert_type', 'activity', 
                          'risk_score', 'message']
        
        st.dataframe(
            filtered_alerts[display_columns],
            use_container_width=True,
            height=400
        )
        
        st.caption(f"Showing {len(filtered_alerts)} of {total_alerts} alerts from current simulation")
        
        # Export option
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Export Current Session Alerts to CSV"):
                csv = df_alerts.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"session_alerts_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("💾 Save All Session Alerts to Historical Log"):
                for alert in st.session_state.current_session_alerts:
                    alert_system.save_alert_to_log(alert)
                st.success(f"✅ Saved {total_alerts} alerts to historical log!")
        
        # ====================================
        # NOTIFICATION PANEL
        # ====================================
        st.divider()
        st.subheader("🔔 System Notifications")
        
        # Calculate critical/emergency alert percentage based on samples
        total_samples = st.session_state.current_session_samples
        critical_emergency_count = emergency_count + critical_count
        critical_percentage = (critical_emergency_count / total_samples * 100) if total_samples > 0 else 0
        
        # Define threshold
        CRITICAL_THRESHOLD = 10.0
        
        # Display notification panel
        st.markdown("""
        <style>
            .notification-panel {
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 5px solid;
            }
            .notification-critical {
                background-color: #fee2e2;
                border-left-color: #dc2626;
            }
            .notification-safe {
                background-color: #dcfce7;
                border-left-color: #16a34a;
            }
        </style>
        """, unsafe_allow_html=True)
        
        if critical_percentage > CRITICAL_THRESHOLD:
            # Critical notification
            st.markdown(f"""
            <div class="notification-panel notification-critical">
                <h3 style="color: #991b1b; margin-top: 0;">🚨 CRITICAL ALERT THRESHOLD EXCEEDED</h3>
                <p style="color: #7f1d1d; font-size: 1.1rem; margin: 0.5rem 0;">
                    <strong>Warning:</strong> Critical and Emergency alerts have exceeded the 10% threshold!
                </p>
                <p style="color: #7f1d1d; margin: 0.5rem 0;">
                    • <strong>Current Level:</strong> {critical_percentage:.2f}% ({critical_emergency_count} critical/emergency alerts out of {total_samples} samples)
                </p>
                <p style="color: #7f1d1d; margin: 0.5rem 0;">
                    • <strong>Threshold:</strong> {CRITICAL_THRESHOLD}% of samples
                </p>
                <p style="color: #7f1d1d; margin: 0.5rem 0;">
                    • <strong>Recommended Action:</strong> Review safety protocols and increase monitoring frequency
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Additional visual indicator
            st.error(f"⚠️ **ATTENTION REQUIRED**: {critical_emergency_count} CRITICAL/EMERGENCY alerts in {total_samples} samples ({critical_percentage:.2f}% - Threshold: {CRITICAL_THRESHOLD}%)")
            
            # Progress bar showing severity
            st.progress(min(critical_percentage / 100, 1.0))
            
        else:
            # Safe notification
            st.markdown(f"""
            <div class="notification-panel notification-safe">
                <h3 style="color: #166534; margin-top: 0;">✅ SYSTEM STATUS NORMAL</h3>
                <p style="color: #14532d; font-size: 1.1rem; margin: 0.5rem 0;">
                    Critical and Emergency alerts are within acceptable limits.
                </p>
                <p style="color: #14532d; margin: 0.5rem 0;">
                    • <strong>Current Level:</strong> {critical_percentage:.2f}% ({critical_emergency_count} critical/emergency alerts out of {total_samples} samples)
                </p>
                <p style="color: #14532d; margin: 0.5rem 0;">
                    • <strong>Threshold:</strong> {CRITICAL_THRESHOLD}% of samples
                </p>
                <p style="color: #14532d; margin: 0.5rem 0;">
                    • <strong>Status:</strong> Continue regular monitoring
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.success(f"✓ System operating normally - {critical_percentage:.2f}% critical/emergency rate (Below {CRITICAL_THRESHOLD}% threshold)")
            
            # Progress bar showing current level
            st.progress(critical_percentage / 100)
        
        # Summary metrics for notification panel
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Critical/Emergency %",
                f"{critical_percentage:.2f}%",
                delta=f"{critical_percentage - CRITICAL_THRESHOLD:.2f}%",
                delta_color="inverse"
            )
        
        with col2:
            st.metric("Threshold", f"{CRITICAL_THRESHOLD}%")
        
        with col3:
            status = "🔴 EXCEEDED" if critical_percentage > CRITICAL_THRESHOLD else "🟢 NORMAL"
            st.metric("Status", status)
        
        with col4:
            remaining = max(0, CRITICAL_THRESHOLD - critical_percentage)
            st.metric("Margin", f"{remaining:.2f}%")


# ====================================
# MODE 5: HEALTH TREND DASHBOARD
# ====================================
elif mode == "📅 Health Trend Dashboard":
    st.header("📅 Health Trend Dashboard")
    st.subheader("Cumulative Health Analytics Across All Simulations")
    
    # Check if there's any health history data
    if st.session_state.health_history.empty:
        st.info("📝 No health trend data available yet. Run a Live Simulation to start collecting health metrics.")
        
        st.markdown("""
        ### How to Start Tracking:
        
        1. Go to **🔴 Live Simulation** mode
        2. Run a simulation (alerts can be enabled or disabled)
        3. Return here to see cumulative health trends
        
        The dashboard will track:
        - 📊 Risk trends over time
        - 🚨 Fall events timeline
        - ⚠️ Alert frequency
        - 🏃 Activity distribution
        - 💪 Fatigue and overactivity patterns
        """)
    else:
        df_health = st.session_state.health_history
        
        # ====================================
        # TOP SUMMARY CARDS
        # ====================================
        st.subheader("📊 Overall Health Summary")
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            total_samples = len(df_health)
            st.metric("📍 Total Samples", total_samples)
        
        with col2:
            total_falls = df_health['fall'].sum() if 'fall' in df_health.columns else 0
            st.metric("🚨 Total Falls", int(total_falls))
        
        with col3:
            highest_risk = df_health['risk'].max() if 'risk' in df_health.columns and len(df_health) > 0 else 0
            st.metric("⚡ Highest Risk", f"{int(highest_risk)}/100")
        
        with col4:
            avg_risk = df_health['risk'].mean() if 'risk' in df_health.columns and len(df_health) > 0 else 0
            st.metric("📈 Avg Risk", f"{avg_risk:.1f}/100")
        
        with col5:
            total_alerts = df_health['alert'].sum() if 'alert' in df_health.columns else 0
            st.metric("⚠️ High-Risk Alerts", int(total_alerts))
        
        with col6:
            total_anomalies = df_health['anomaly'].sum() if 'anomaly' in df_health.columns else 0
            st.metric("🔎 Anomalies", int(total_anomalies))
        
        st.divider()
        
        # ====================================
        # TRENDS SECTION
        # ====================================
        st.subheader("📈 Live Trend Analytics")
        
        # 1️⃣ Risk Trend Over Time
        st.markdown("#### 1️⃣ Risk Trend Over Time")
        
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        
        if 'risk' in df_health.columns and len(df_health) > 0:
            # Plot risk as line chart
            ax1.plot(range(len(df_health)), df_health['risk'], 
                    color='#667eea', linewidth=2, label='Risk Score')
            
            # Highlight critical spikes (risk > 75)
            critical_indices = df_health[df_health['risk'] > 75].index
            if len(critical_indices) > 0:
                ax1.scatter(critical_indices, df_health.loc[critical_indices, 'risk'], 
                           color='red', s=100, zorder=5, label='Critical Spikes', marker='X')
            
            # Add threshold lines
            ax1.axhline(y=30, color='green', linestyle='--', alpha=0.5, label='Low Risk')
            ax1.axhline(y=60, color='orange', linestyle='--', alpha=0.5, label='Medium Risk')
            ax1.axhline(y=85, color='red', linestyle='--', alpha=0.5, label='High Risk')
            
            ax1.set_xlabel('Sample Index', fontsize=12)
            ax1.set_ylabel('Risk Score', fontsize=12)
            ax1.set_title('Risk Score Evolution', fontsize=14, fontweight='bold')
            ax1.legend(loc='upper right')
            ax1.grid(True, alpha=0.3)
            ax1.set_ylim(0, 100)
            
            st.pyplot(fig1)
        else:
            st.info("No risk data available yet")
        
        st.divider()
        
        # 2️⃣ Fall Trend Timeline
        st.markdown("#### 2️⃣ Fall Event Timeline")
        
        if 'fall' in df_health.columns:
            fall_events = df_health[df_health['fall'] == True]
            
            fig2, ax2 = plt.subplots(figsize=(12, 3))
            
            # Plot all samples as background
            ax2.scatter(range(len(df_health)), [0.5] * len(df_health), 
                       color='lightgray', s=10, alpha=0.3, label='Normal')
            
            # Mark fall events
            if len(fall_events) > 0:
                ax2.scatter(fall_events.index, [0.5] * len(fall_events), 
                           color='red', s=200, marker='X', zorder=5, label='Fall Detected')
                st.metric("🚨 Fall Event Count", len(fall_events))
            else:
                st.success("✅ No fall events detected across all simulations!")
            
            ax2.set_xlabel('Sample Index', fontsize=12)
            ax2.set_title('Fall Events Across All Simulations', fontsize=14, fontweight='bold')
            ax2.set_ylim(0, 1)
            ax2.set_yticks([0.5])
            ax2.set_yticklabels(['Timeline'])
            ax2.legend(loc='upper right')
            ax2.grid(True, alpha=0.3, axis='x')
            
            st.pyplot(fig2)
        else:
            st.info("No fall data available")
        
        st.divider()
        
        # 3️⃣ Alert Frequency Chart
        st.markdown("#### 3️⃣ Alert Frequency Over Time")
        
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Calculate alert counts
            alert_summary = {
                'INFO': 0,
                'WARNING': 0,
                'CRITICAL': 0,
                'EMERGENCY': 0
            }
            
            for idx, row in df_health.iterrows():
                if row.get('fall', False):
                    alert_summary['EMERGENCY'] += 1
                elif row.get('alert', False):
                    alert_summary['CRITICAL'] += 1
                elif row.get('anomaly', False):
                    alert_summary['WARNING'] += 1
                elif row.get('risk', 0) >= 60:
                    alert_summary['INFO'] += 1
            
            fig3, ax3 = plt.subplots(figsize=(8, 5))
            
            colors_map = {
                'INFO': '#3b82f6',
                'WARNING': '#f59e0b',
                'CRITICAL': '#ef4444',
                'EMERGENCY': '#991b1b'
            }
            
            severities = list(alert_summary.keys())
            counts = list(alert_summary.values())
            bar_colors = [colors_map[s] for s in severities]
            
            bars = ax3.bar(severities, counts, color=bar_colors, edgecolor='black', linewidth=1.5)
            
            # Add value labels
            for bar in bars:
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=12, fontweight='bold')
            
            ax3.set_xlabel('Alert Severity', fontsize=12)
            ax3.set_ylabel('Count', fontsize=12)
            ax3.set_title('Cumulative Alert Distribution', fontsize=14, fontweight='bold')
            ax3.grid(True, alpha=0.3, axis='y')
            
            st.pyplot(fig3)
        
        with col_right:
            st.markdown("**Alert Summary Statistics:**")
            total_alerts_all = sum(alert_summary.values())
            
            for severity, count in alert_summary.items():
                percentage = (count / total_alerts_all * 100) if total_alerts_all > 0 else 0
                st.metric(f"{severity} Alerts", count, f"{percentage:.1f}%")
        
        st.divider()
        
        # 4️⃣ Activity Distribution
        st.markdown("#### 4️⃣ Activity Distribution")
        
        if 'activity' in df_health.columns:
            activity_counts = df_health['activity'].value_counts()
            
            col_chart, col_table = st.columns([2, 1])
            
            with col_chart:
                fig4, ax4 = plt.subplots(figsize=(10, 6))
                
                # Create pie chart
                colors = plt.cm.Set3(range(len(activity_counts)))
                wedges, texts, autotexts = ax4.pie(
                    activity_counts.values, 
                    labels=activity_counts.index,
                    autopct='%1.1f%%',
                    colors=colors,
                    startangle=90
                )
                
                # Enhance text
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                
                ax4.set_title('Activity Distribution Across All Simulations', 
                             fontsize=14, fontweight='bold')
                
                st.pyplot(fig4)
            
            with col_table:
                st.markdown("**Activity Breakdown:**")
                activity_df = pd.DataFrame({
                    'Activity': activity_counts.index,
                    'Count': activity_counts.values,
                    'Percentage': (activity_counts.values / activity_counts.sum() * 100).round(1)
                })
                st.dataframe(activity_df, use_container_width=True, hide_index=True)
        else:
            st.info("No activity data available")
        
        st.divider()
        
        # ====================================
        # FATIGUE / OVERACTIVITY INSIGHT
        # ====================================
        st.subheader("💪 Fatigue & Activity Insights")
        
        # Rolling window analysis (last 50 samples)
        window_size = min(50, len(df_health))
        
        if len(df_health) >= 10:
            recent_data = df_health.tail(window_size)
            
            # Check for rising motion + risk trend
            if 'motion' in recent_data.columns and 'risk' in recent_data.columns:
                motion_trend = recent_data['motion'].rolling(window=10, min_periods=5).mean()
                risk_trend = recent_data['risk'].rolling(window=10, min_periods=5).mean()
                
                # Check if both are rising
                motion_rising = motion_trend.iloc[-1] > motion_trend.iloc[0] if len(motion_trend) >= 2 else False
                risk_rising = risk_trend.iloc[-1] > risk_trend.iloc[0] if len(risk_trend) >= 2 else False
                high_values = recent_data['motion'].mean() > df_health['motion'].mean() * 1.2
                
                if motion_rising and risk_rising and high_values:
                    st.warning("⚠️ **Possible Fatigue / Overexertion Detected**")
                    st.markdown("""
                    Recent samples show:
                    - Increasing motion intensity
                    - Rising risk scores
                    - Above-average activity levels
                    
                    **Recommendation:** Consider reducing activity intensity and taking rest breaks.
                    """)
                
                # Check for extended inactivity
                avg_motion = recent_data['motion'].mean()
                overall_avg = df_health['motion'].mean()
                
                if avg_motion < overall_avg * 0.5 and len(recent_data) >= 30:
                    st.info("ℹ️ **Extended Inactivity Detected**")
                    st.markdown(f"""
                    Last {window_size} samples show significantly reduced motion:
                    - Current average motion: {avg_motion:.3f}
                    - Overall average motion: {overall_avg:.3f}
                    
                    **Note:** Extended periods of low activity detected.
                    """)
                
                # Show trends chart
                fig5, (ax5a, ax5b) = plt.subplots(1, 2, figsize=(14, 4))
                
                # Motion trend
                ax5a.plot(range(len(recent_data)), recent_data['motion'], 
                         color='#8b5cf6', alpha=0.6, label='Motion')
                ax5a.plot(range(len(motion_trend)), motion_trend, 
                         color='#6366f1', linewidth=3, label='Trend')
                ax5a.set_xlabel('Recent Sample Index')
                ax5a.set_ylabel('Motion Magnitude')
                ax5a.set_title(f'Motion Trend (Last {window_size} Samples)')
                ax5a.legend()
                ax5a.grid(True, alpha=0.3)
                
                # Risk trend
                ax5b.plot(range(len(recent_data)), recent_data['risk'], 
                         color='#f59e0b', alpha=0.6, label='Risk')
                ax5b.plot(range(len(risk_trend)), risk_trend, 
                         color='#ef4444', linewidth=3, label='Trend')
                ax5b.set_xlabel('Recent Sample Index')
                ax5b.set_ylabel('Risk Score')
                ax5b.set_title(f'Risk Trend (Last {window_size} Samples)')
                ax5b.legend()
                ax5b.grid(True, alpha=0.3)
                
                plt.tight_layout()
                st.pyplot(fig5)
            else:
                st.info("Not enough data for trend analysis yet")
        else:
            st.info("Collect more samples (at least 10) for fatigue analysis")
        
        st.divider()
        
        # ====================================
        # PERSISTENCE - SAVE HEALTH TREND LOG
        # ====================================
        st.subheader("💾 Export Health Trend Data")
        
        col_save1, col_save2, col_save3 = st.columns(3)
        
        with col_save1:
            if st.button("💾 Save Health Trend Log", use_container_width=True):
                filename = "health_trend_log.csv"
                df_health.to_csv(filename, index=False)
                st.success(f"✅ Saved {len(df_health)} records to {filename}")
        
        with col_save2:
            if st.button("📥 Download Health Trend CSV", use_container_width=True):
                csv = df_health.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"health_trend_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col_save3:
            if st.button("🗑️ Clear Health History", use_container_width=True, type="secondary"):
                if st.session_state.get('confirm_clear', False):
                    st.session_state.health_history = pd.DataFrame()
                    st.session_state.confirm_clear = False
                    st.success("✅ Health history cleared!")
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("⚠️ Click again to confirm clearing all health trend data!")
        
        # Data summary
        st.markdown(f"""
        **Current Health Trend Database:**
        - Total Samples: {len(df_health)}
        - Date Range: {df_health['timestamp'].min()} to {df_health['timestamp'].max()}
        - Data Size: {df_health.memory_usage(deep=True).sum() / 1024:.2f} KB
        """)




# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p><strong>Activity Recognition & Motion-Based Safety Monitoring System</strong></p>
    <p>Powered by Machine Learning | Real-time Activity Recognition & Fall Detection</p>
</div>
""", unsafe_allow_html=True)
