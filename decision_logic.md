# Decision Logic for Activity Recognition System

## 1. Static vs Dynamic Activity Decision

Input features:
- Accelerometer variance (accel_variance)
- Gyroscope RMS value (gyro_rms)

Decision logic:
IF accel_variance < T_static AND gyro_rms < T_gyro
    → Activity is STATIC
ELSE
    → Activity is DYNAMIC
## 2. Static Activity Classification (Sitting / Standing / Lying)

Input features:
- Gravity vector orientation
- Mean acceleration along vertical axis

Decision logic:
IF body orientation is vertical AND gravity aligned with Z-axis
    → Standing
ELSE IF body orientation is tilted but upright
    → Sitting
ELSE IF body orientation is horizontal
    → Lying
## 3. Dynamic Activity Classification (Walking / Jogging / Running)

Input features:
- Dominant frequency of motion
- RMS acceleration value

Decision logic:
IF dominant frequency is between 1–2 Hz AND RMS acceleration is low
    → Walking
ELSE IF dominant frequency is between 2–3 Hz AND RMS acceleration is moderate
    → Jogging
ELSE IF dominant frequency is greater than 3 Hz AND RMS acceleration is high
    → Running

Purpose:
This step differentiates locomotion intensity based on motion rhythm and energy.
## 4. Stair Climbing Detection

Input features:
- Vertical (Z-axis) acceleration energy
- Periodic motion pattern
- Dominant frequency

Decision logic:
IF periodic motion detected
AND vertical acceleration energy is significantly higher than horizontal acceleration energy
    → Stair Climbing

Purpose:
Stair climbing produces stronger vertical motion compared to level ground walking.
## 5. Fall Detection Logic

Input features:
- Acceleration magnitude
- Sudden body orientation change
- Post-impact inactivity duration

Decision logic:
IF acceleration magnitude exceeds fall impact threshold
AND sudden body orientation change is detected
AND acceleration variance remains very low for a short duration after impact
    → Fall Detected

Purpose:
Falls are identified using a combination of impact, posture change, and lack of recovery movement.
## 6. Safety Alert Generation

Input:
- Activity classification result
- Fall detection result
- Anomaly score
- Inactivity duration

Decision logic:
IF fall detected
    → Trigger immediate emergency alert
ELSE IF high anomaly score detected during risky activity
    → Trigger warning alert
ELSE IF prolonged inactivity exceeds defined threshold
    → Trigger wellness alert

Purpose:
This step decides when and how the system should notify caregivers or supervisors.
## 7. Risk Scoring Logic

Input:
- Number of detected falls
- Number of near-fall or anomalous events
- Duration of prolonged inactivity
- Amount of regular safe physical activity

Decision logic:
Risk score increases with falls, anomalies, and inactivity duration.
Risk score decreases with consistent safe activities such as walking.

Risk level classification:
- Low Risk
- Medium Risk
- High Risk

Purpose:
Risk scoring provides a long-term assessment of user safety based on activity history.
