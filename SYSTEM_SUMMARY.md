# Complete System Summary - Session Alerts Update

## Recent Updates (Latest Session)

### What Changed?
I've modified the system so that the **Safety Alert System** now shows **only current simulation alerts** instead of historical data.

### Key Changes:

1. **Session State Management**
   - Added `st.session_state.current_session_alerts` - Stores alerts from current simulation
   - Added `st.session_state.current_session_samples` - Tracks number of samples simulated
   - Added `st.session_state.simulation_completed` - Marks if simulation finished

2. **Live Simulation Updates**
   - When you start a simulation,it clears previous session alerts
   - All generated alerts are stored in session state
   - Critical alerts are still saved to log file automatically

3. **Safety Alert System Updates**
   - Now displays alerts from the current session only
   - Shows notification panel based on **samples** not total alerts
   - Calculates: `critical_percentage = (critical_emergency_count / total_samples) * 100`
   - If no simulation has run, shows instructions and option to view historical alerts

4. **Notification Panel Logic**
   - **Threshold**: 10% of simulated samples
   - **Triggers when**: (Critical + Emergency alerts) > 10% of samples
   - **Example**: If you simulate 100 samples and get 11+ critical/emergency alerts, you'll see a warning

---

## How to Use the Updated System

### Step 1: Run a Simulation
1. Go to **🔴 Live Simulation** mode
2. Enable **🚨 Enable Alerts** checkbox
3. Set your Max Samples (e.g., 100)
4. Click **▶️ Start Simulation**

### Step 2: View Current Session Alerts
1. Go to **🚨 Safety Alert System** mode
2. You'll see:
   - Overview metrics from your simulation
   - Alert breakdowns by severity and activity
   - Recent alerts table
   - **🔔 System Notifications panel** at the bottom

### Step 3: Understand the Notification Panel

**If Critical/Emergency alerts > 10% of samples:**
```
🚨 CRITICAL ALERT THRESHOLD EXCEEDED
Warning: Critical and Emergency alerts have exceeded the 10% threshold!
• Current Level: 15.00% (15 critical/emergency alerts out of 100 samples)
• Threshold: 10.0% of samples
• Recommended Action: Review safety protocols and increase monitoring frequency
```

**If Critical/Emergency alerts ≤ 10% of samples:**
```
✅ SYSTEM STATUS NORMAL
Critical and Emergency alerts are within acceptable limits.
• Current Level: 5.00% (5 critical/emergency alerts out of 100 samples)
• Threshold: 10.0% of samples
• Status: Continue regular monitoring
```

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Activity Recognition System               │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌──────────────────┐
│  Data Layer   │  │  Model Layer   │  │  Application     │
│               │  │                │  │  Layer           │
│ • train.csv   │  │ • Training     │  │ • Streamlit App  │
│ • test.csv    │  │   Notebook     │  │ • Live Sim       │
│               │  │ • Model .pkl   │  │ • Alerts System  │
└───────────────┘  └────────────────┘  └──────────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                ┌───────────┴────────────┐
                │                        │
                ▼                        ▼
        ┌──────────────┐        ┌──────────────┐
        │ Alert System │        │ Session State│
        │              │        │              │
        │ • Generate   │        │ • Alerts     │
        │ • Log        │        │ • Samples    │
        │ • Analyze    │        │ • Status     │
        └──────────────┘        └──────────────┘
```

---

## File Structure

```
ecoverse/
├── activity_recognition.ipynb    # ML model training notebook
├── app.py                        # Main Streamlit application
├── alert_system.py              # Safety alert generation logic
├── train_model.py               # Python script version of training
├── data/
│   ├── train.csv               # Training dataset
│   └── test.csv                # Test dataset
├── activity_model.pkl          # Saved trained model
├── activity_tracking_log.csv   # Historical activity log
├── safety_alerts.csv           # Historical alerts log
└── Documentation/
    ├── ACTIVITY_RECOGNITION_EXPLAINED.md
    ├── ALERT_SYSTEM_README.md
    └── ALERT_IMPLEMENTATION_SUMMARY.md
```

---

## Complete Workflow

### 1. Training Phase (One-time)
```
activity_recognition.ipynb
    ↓
Trains on train.csv
    ↓
Saves activity_model.pkl
```

### 2. Simulation Phase (Repeatable)
```
app.py → Live Simulation
    ↓
Loads activity_model.pkl
    ↓
Reads test.csv
    ↓
For each sample:
    - Predict activity
    - Calculate risk
    - Generate alerts
    - Store in session_state
    ↓
Mark simulation complete
```

### 3. Analysis Phase
```
Safety Alert System
    ↓
Read session_state.current_session_alerts
    ↓
Calculate statistics
    ↓
Display visualizations
    ↓
Check notification threshold
    ↓
Show appropriate notification
```

---

## Alert Severity Levels

| Severity | Icon | Trigger Condition | Action Required |
|----------|------|-------------------|-----------------|
| INFO | ℹ️ | Risk score ≥ 60 | Continue monitoring |
| WARNING | ⚠️ | Anomaly OR high-risk activity | Increase monitoring frequency |
| CRITICAL | 🔴 | Dangerous motion spike | Monitor closely, prepare intervention |
| EMERGENCY | 🚨 | Fall detected | Immediate medical assistance |

---

## Mathematical Formulas

### Risk Score Calculation:
```python
risk = 0
risk += min((motion / mean_mag) * 25, 25)  # Motion component (0-25)
risk += 25 if is_anomaly else 0            # Anomaly component (0 or 25)
risk += 25 if is_high_alert else 0         # High alert component (0 or 25)
risk += 25 if is_fall else 0               # Fall component (0 or 25)
total_risk = min(risk, 100)                # Cap at 100
```

### Notification Threshold:
```python
critical_emergency_count = emergency_count + critical_count
critical_percentage = (critical_emergency_count / total_samples) * 100
threshold_exceeded = critical_percentage > 10.0
```

### Motion Magnitude:
```python
acc_mag = sqrt(tBodyAcc-mean()-X² + tBodyAcc-mean()-Y² + tBodyAcc-mean()-Z²)
```

### Anomaly Detection:
```python
threshold = mean_magnitude + (2 × std_magnitude)
is_anomaly = acc_mag > threshold
```

---

## Performance Metrics

### Model Performance:
- **Accuracy**: Typically 90-95%
- **Activities Recognized**: 6 (WALKING, SITTING, STANDING, LAYING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS)
- **Features Used**: ~561 sensor measurements

### System Performance:
- **Simulation Speed**: Adjustable (0.1x to 2.0x)
- **Alert Generation**: Real-time during simulation
- **Data Processing**: Handles 1000+ samples efficiently

---

## Common User Scenarios

### Scenario 1: High Alert Rate
**User runs simulation with 100 samples, gets 20 critical alerts**

Result:
- Notification panel shows: 🚨 CRITICAL ALERT THRESHOLD EXCEEDED
- Percentage: 20.00% (above 10% threshold)
- Recommendation: Review safety protocols

### Scenario 2: Normal Operation
**User runs simulation with 100 samples, gets 5 critical alerts**

Result:
- Notification panel shows: ✅ SYSTEM STATUS NORMAL
- Percentage: 5.00% (below 10% threshold)
- Status: Continue regular monitoring

### Scenario 3  New Session
**User starts new simulation**

Result:
- Previous alerts are cleared
- Fresh session starts
- New notification calculation based on new data

---

## Troubleshooting

### Issue: "No alerts from current simulation session"
**Solution:** You haven't run a simulation yet or forgot to enable alerts
- Go to Live Simulation
- Check "Enable Alerts"
- Run simulation

### Issue: Notification panel shows 0%
**Solution:** No critical/emergency alerts were generated
- This is good! It means the simulated activities were low-risk
- Try simulating more samples to get diverse data

### Issue: Historical alerts still showing
**Solution:** You might be looking at historical alerts option
- Make sure you've run a new simulation
- Check that simulation_completed is True
- Historical alerts only show if you check the optional  checkbox

---

## Future Enhancements (Possible)

1. **Multi-Session Comparison**
   - Compare current session with previous sessions
   - Track trends over time

2. **Custom Thresholds**
   - Allow user to adjust 10% threshold
   - Set different thresholds per activity type

3. **Export Session Reports**
   - Generate PDF reports of current session
   - Include all charts and metrics

4. **Real-time Notifications**
   - Email/SMS alerts when threshold exceeded
   - Integration with monitoring systems

5. **Session History**
   - Keep track of last N sessions
   - Compare performance across sessions

---

## Quick Reference Commands

### Run Streamlit App:
```bash
streamlit run app.py
```

### Train Model (if needed):
```bash
python train_model.py
```

### Check Model Accuracy:
```bash
# Run activity_recognition.ipynb
# Check final accuracy cell
```

---

## Summary

The updated system provides:
✅ **Session-based alert tracking** - Only shows current simulation data
✅ **Sample-based notifications** - Calculates % based on samples, not alerts
✅ **Clear separation** - Current vs historical alerts
✅ **Real-time feedback** - Know immediately if safety thresholds exceeded
✅ **Actionable insights** - Clear recommendations when thresholds exceeded

**Result**: A more intuitive and accurate safety monitoring system that helps users understand risks in the context of their current simulation.
