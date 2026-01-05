"""
Safety Alert Generation System
Generates and manages safety alerts for high-risk activities
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
import json

class SafetyAlertSystem:
    """Manages safety alerts for activity monitoring"""
    
    def __init__(self, alert_log_file="safety_alerts.csv"):
        self.alert_log_file = alert_log_file
        self.current_session_alerts = []
        
        # Alert severity levels
        self.SEVERITY_LEVELS = {
            'INFO': 0,
            'WARNING': 1,
            'CRITICAL': 2,
            'EMERGENCY': 3
        }
        
        # Risk thresholds
        self.RISK_THRESHOLDS = {
            'LOW': (0, 30),
            'MEDIUM': (30, 60),
            'HIGH': (60, 85),
            'CRITICAL': (85, 100)
        }
        
        # High-risk activities that trigger immediate alerts
        self.HIGH_RISK_ACTIVITIES = {
            'STAIRS': 'WARNING',
            'RUNNING': 'INFO',
            'JOGGING': 'INFO'
        }
    
    def generate_alert(self, activity, risk_score, motion_intensity, 
                      is_fall=False, is_anomaly=False, is_high_alert=False,
                      sample_index=None):
        """
        Generate a safety alert based on current conditions
        
        Returns: dict with alert information or None if no alert needed
        """
        alert = None
        timestamp = datetime.now().isoformat()
        
        # EMERGENCY: Fall detected
        if is_fall:
            alert = {
                'timestamp': timestamp,
                'severity': 'EMERGENCY',
                'alert_type': 'FALL_DETECTED',
                'activity': activity,
                'risk_score': risk_score,
                'motion_intensity': motion_intensity,
                'message': f'🚨 EMERGENCY: Fall detected during {activity}',
                'action_required': 'Immediate medical assistance required',
                'sample_index': sample_index
            }
        
        # CRITICAL: High-risk alert (very dangerous motion)
        elif is_high_alert:
            alert = {
                'timestamp': timestamp,
                'severity': 'CRITICAL',
                'alert_type': 'HIGH_RISK_MOTION',
                'activity': activity,
                'risk_score': risk_score,
                'motion_intensity': motion_intensity,
                'message': f'⚠️ CRITICAL: Dangerous motion spike during {activity}',
                'action_required': 'Monitor closely, prepare for intervention',
                'sample_index': sample_index
            }
        
        # WARNING: Anomaly detected or high-risk activity
        elif is_anomaly or activity.upper() in self.HIGH_RISK_ACTIVITIES:
            if is_anomaly:
                alert_type = 'ANOMALY_DETECTED'
                message = f'🔎 WARNING: Unusual movement pattern during {activity}'
                action = 'Increase monitoring frequency'
            else:
                alert_type = 'HIGH_RISK_ACTIVITY'
                message = f'⚡ WARNING: Performing high-risk activity: {activity}'
                action = 'Ensure safety measures in place'
            
            alert = {
                'timestamp': timestamp,
                'severity': 'WARNING',
                'alert_type': alert_type,
                'activity': activity,
                'risk_score': risk_score,
                'motion_intensity': motion_intensity,
                'message': message,
                'action_required': action,
                'sample_index': sample_index
            }
        
        # INFO: High risk score without immediate danger
        elif risk_score >= 60:
            alert = {
                'timestamp': timestamp,
                'severity': 'INFO',
                'alert_type': 'ELEVATED_RISK',
                'activity': activity,
                'risk_score': risk_score,
                'motion_intensity': motion_intensity,
                'message': f'ℹ️ INFO: Elevated risk level during {activity}',
                'action_required': 'Continue monitoring',
                'sample_index': sample_index
            }
        
        # Add to current session if alert generated
        if alert:
            self.current_session_alerts.append(alert)
        
        return alert
    
    def save_alert_to_log(self, alert):
        """Save alert to persistent log file"""
        if alert is None:
            return
        
        # Create DataFrame from alert
        alert_df = pd.DataFrame([{
            'timestamp': alert['timestamp'],
            'severity': alert['severity'],
            'alert_type': alert['alert_type'],
            'activity': alert['activity'],
            'risk_score': alert['risk_score'],
            'motion_intensity': alert['motion_intensity'],
            'message': alert['message'],
            'action_required': alert['action_required'],
            'sample_index': alert.get('sample_index', -1)
        }])
        
        # Append to existing log or create new one
        if Path(self.alert_log_file).exists():
            existing_df = pd.read_csv(self.alert_log_file)
            combined_df = pd.concat([existing_df, alert_df], ignore_index=True)
            combined_df.to_csv(self.alert_log_file, index=False)
        else:
            alert_df.to_csv(self.alert_log_file, index=False)
    
    def get_session_summary(self):
        """Get summary of alerts generated in current session"""
        if not self.current_session_alerts:
            return {
                'total_alerts': 0,
                'by_severity': {},
                'by_type': {},
                'critical_count': 0
            }
        
        df = pd.DataFrame(self.current_session_alerts)
        
        return {
            'total_alerts': len(self.current_session_alerts),
            'by_severity': df['severity'].value_counts().to_dict(),
            'by_type': df['alert_type'].value_counts().to_dict(),
            'critical_count': len(df[df['severity'].isin(['CRITICAL', 'EMERGENCY'])])
        }
    
    def get_recent_alerts(self, n=10):
        """Get n most recent alerts from log"""
        if not Path(self.alert_log_file).exists():
            return pd.DataFrame()
        
        df = pd.read_csv(self.alert_log_file)
        return df.tail(n).sort_values('timestamp', ascending=False)
    
    def clear_session_alerts(self):
        """Clear current session alerts"""
        self.current_session_alerts = []
    
    def get_alert_statistics(self):
        """Get overall alert statistics from log file"""
        if not Path(self.alert_log_file).exists():
            return None
        
        df = pd.read_csv(self.alert_log_file)
        
        return {
            'total_alerts': len(df),
            'severity_breakdown': df['severity'].value_counts().to_dict(),
            'type_breakdown': df['alert_type'].value_counts().to_dict(),
            'activity_breakdown': df['activity'].value_counts().to_dict(),
            'average_risk_score': df['risk_score'].mean(),
            'emergency_count': len(df[df['severity'] == 'EMERGENCY']),
            'critical_count': len(df[df['severity'] == 'CRITICAL'])
        }


def format_alert_message(alert):
    """Format alert for display in Streamlit"""
    severity_icons = {
        'INFO': 'ℹ️',
        'WARNING': '⚠️',
        'CRITICAL': '🔴',
        'EMERGENCY': '🚨'
    }
    
    icon = severity_icons.get(alert['severity'], '📢')
    
    return f"""
    **{icon} {alert['severity']}** - {alert['alert_type'].replace('_', ' ').title()}
    
    **Activity:** {alert['activity']}  
    **Risk Score:** {alert['risk_score']}/100  
    **Motion Intensity:** {alert['motion_intensity']:.3f}
    
    **Message:** {alert['message']}  
    **Action Required:** {alert['action_required']}
    """
