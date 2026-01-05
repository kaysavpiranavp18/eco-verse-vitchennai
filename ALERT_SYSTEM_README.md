# Safety Alert Generation System

## Overview
The Safety Alert Generation System is a comprehensive module for detecting and managing safety risks during activity monitoring. It automatically generates alerts based on activity patterns, risk scores, and motion characteristics.

## Features

### 🚨 Alert Severity Levels
1. **EMERGENCY** (Highest Priority)
   -Fall events detected
   - Requires immediate medical assistance
   - Automatically logged to persistent storage

2. **CRITICAL**
   - Dangerous motion spikes
   - Prepare for intervention
   - Automatically logged to persistent storage

3. **WARNING**
   - Anomalous movement patterns
   - High-risk activities (stairs, running)
   - Increase monitoring frequency

4. **INFO**
   - Elevated risk levels (60+)
   - Continue monitoring

### 📊 Alert Types
- **FALL_DETECTED**: Fall events with spike + stillness pattern
- **HIGH_RISK_MOTION**: Dangerous motion intensity spikes
- **ANOMALY_DETECTED**: Unusual movement patterns
- **HIGH_RISK_ACTIVITY**: Activities known to be risky (stairs, running)
- **ELEVATED_RISK**: High risk scores without immediate danger

## How to Use

### In Live Simulation
1. Navigate to **🔴 Live Simulation** mode
2. Enable **🚨 Enable Alerts** checkbox in control panel
3. Run the simulation
4. Alerts will be generated in real-time
5. Critical/Emergency alerts are automatically logged
6. After simulation, view alert summary
7. Optionally save all alerts to log

### In Alert Management System
1. Navigate to **🚨 Safety Alert System** mode
2. View comprehensive statistics:
   - Total alerts
   - Emergency/Critical counts
   - Average risk score
3. Explore visualizations:
   - Alerts by severity
   - Alerts by activity type
   - Alert type breakdown
4. Review recent alerts with filtering
5. Export alerts to CSV

## Alert Structure

Each alert contains:
```python
{
    'timestamp': '2026-01-06T00:30:45.123456',
    'severity': 'CRITICAL',
    'alert_type': 'FALL_DETECTED',
    'activity': 'WALKING',
    'risk_score': 95,
    'motion_intensity': 2.456,
    'message': '🚨 EMERGENCY: Fall detected during WALKING',
    'action_required': 'Immediate medical assistance required',
    'sample_index': 42
}
```

## Alert Generation Logic

### Fall Detection
```python
if is_fall:
    severity = 'EMERGENCY'
    message = 'Fall detected'
    action = 'Immediate medical assistance required'
```

### High-Risk Motion
```python
if high_alert (motion > mean + 3.5×std):
    severity = 'CRITICAL'
    message = 'Dangerous motion spike'
    action = 'Monitor closely, prepare for intervention'
```

### Anomaly Detection
```python
if anomaly (motion > mean + 2×std):
    severity = 'WARNING'
    message = 'Unusual movement pattern'
    action = 'Increase monitoring frequency'
```

### High-Risk Activity
```python
if activity in ['STAIRS', 'RUNNING', 'JOGGING']:
    severity = 'WARNING'
    message = 'Performing high-risk activity'
    action = 'Ensure safety measures in place'
```

### Elevated Risk
```python
if risk_score >= 60:
    severity = 'INFO'
    message = 'Elevated risk level'
    action = 'Continue monitoring'
```

## Storage

- **Session Alerts**: Stored in memory during simulation
- **Persistent Log**: `safety_alerts.csv` file
- **Auto-Save**: Critical/Emergency alerts saved immediately
- **Manual Save**: Other alerts can be saved after simulation

## API Reference

### SafetyAlertSystem Class

#### Methods

**`generate_alert(activity, risk_score, motion_intensity, is_fall, is_anomaly, is_high_alert, sample_index)`**
- Generates alert based on current conditions
- Returns alert dict or None

**`save_alert_to_log(alert)`**
- Saves alert to CSV log file
- Creates file if doesn't exist

**`get_session_summary()`**
- Returns statistics for current session:
  - total_alerts
  - by_severity breakdown
  - by_type breakdown
  - critical_count

**`get_recent_alerts(n=10)`**
- Returns n most recent alerts from log
- Returns pandas DataFrame

**`get_alert_statistics()`**
- Returns overall statistics from log:
  - total_alerts
  - severity_breakdown
  - type_breakdown
  - activity_breakdown
  - average_risk_score
  - emergency_count
  - critical_count

**`clear_session_alerts()`**
- Clears current session alerts from memory

### format_alert_message(alert)
- Formats alert for display in Streamlit
- Returns formatted markdown string

## Configuration

### Risk Thresholds
```python
RISK_THRESHOLDS = {
    'LOW': (0, 30),
    'MEDIUM': (30, 60),
    'HIGH': (60, 85),
    'CRITICAL': (85, 100)
}
```

### High-Risk Activities
```python
HIGH_RISK_ACTIVITIES = {
    'STAIRS': 'WARNING',
    'RUNNING': 'INFO',
    'JOGGING': 'INFO'
}
```

## Example Workflow

1. **Start Simulation with Alerts**
   ```
   Enable alerts checkbox → Run simulation
   ```

2. **Alert Generated During Simulation**
   ```
   Sample #42 → Fall detected → EMERGENCY alert created → Auto-saved to log
   ```

3. **View Alert Summary**
   ```
   Total: 15 alerts
   - 2 EMERGENCY
   - 3 CRITICAL
   - 7 WARNING
   - 3 INFO
   ```

4. **Review in Alert System**
   ```
   Navigate to Alert System → View statistics → Filter by severity → Export
   ```

## Benefits

✅ **Real-time Detection**: Alerts generated during simulation  
✅ **Prioritization**: Severity levels ensure critical issues get attention  
✅ **Persistence**: Important alerts never lost  
✅ **Analytics**: Comprehensive statistics and visualizations  
✅ **Export**: Download alerts for external analysis  
✅ **Filtering**: Find specific alerts quickly  
✅ **Actionable**: Each alert includes recommended action  

## Files

- `alert_system.py`: Core alert generation and management logic
- `safety_alerts.csv`: Persistent alert log (auto-created)
- `app.py`: Integration with Streamlit dashboard

## Future Enhancements

- Email/SMS notifications for critical alerts
- Alert acknowledgment system
- Custom alert rules configuration
- Real-time streaming to external systems
- Machine learning for alert prediction
- Alert clustering and pattern recognition
