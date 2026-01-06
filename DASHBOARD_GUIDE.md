# Complete Dashboard Guide
## Activity Recognition & Motion-Based Safety Monitoring System

---

# 📊 Dashboard Overview

Your system has **4 main dashboards**, each serving a different purpose:

1. **📊 Historical Dashboard** - View past activity logs and analysis
2. **🔴 Live Simulation** - Real-time activity monitoring with alerts
3. **📈 Dataset Explorer** - Explore the raw sensor data
4. **🚨 Safety Alert System** - Analyze safety alerts from current session

Let me explain each one in complete detail.

---

# 1️⃣ Historical Dashboard
## 📊 "View past activity tracking and patterns"

### **Purpose:**
Review historical activity data that has been logged during previous simulations or real-time monitoring sessions.

### **When to Use:**
- After running simulations to review what happened
- To analyze patterns in recorded activities
- To track fall events over time
- To understand risk level distributions

---

## 🎯 Dashboard Sections Explained

### **Section 1: Top Metrics Row**

Located at the very top, shows 4 key metrics:

#### **Metric 1: Current Activity**
```
🏃 Current Activity
WALKING
```
- **What it shows**: The activity from the most recent log entry
- **Possible values**: WALKING, SITTING, STANDING, LAYING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS
- **Why it matters**: Quick glance at the last recorded state

#### **Metric 2: Fall Detected**
```
🚨 Fall Detected
NO ✓
```
- **What it shows**: Whether the last entry detected a fall
- **Possible values**: 
  - `NO ✓` (green) - Safe, no fall
  - `YES ⚠️` (red) - Fall detected in last entry
- **Why it matters**: Immediate safety status check

#### **Metric 3: Risk Level**
```
⚡ Risk Level
Low
```
- **What it shows**: Risk assessment of the last entry
- **Possible values**:
  - `Low` - Safe conditions (risk 0-30)
  - `Medium` - Caution needed (risk 30-60)
  - `High` - Dangerous conditions (risk 60-100)
- **Why it matters**: Quick safety assessment

#### **Metric 4: Total Records**
```
📝 Total Records
1,247
```
- **What it shows**: Total number of logged activities
- **Why it matters**: Dataset size indicator

---

### **Section 2: Recent Activity Log**

Shows a data table of recent activities.

#### **Features:**

**Interactive Slider:**
```
Number of records to display: [5 ←──────○────→ 50]
Currently showing: 20
```
- Adjustable from 5 to 50 records
- Default: 20 records

**Data Table Columns:**
| Column | Description | Example |
|--------|-------------|---------|
| **timestamp** | When activity was recorded | 2026-01-06 10:30:15 |
| **predicted_activity** | What activity was detected | WALKING |
| **risk_level** | Safety assessment | Low |
| **fall_detected** | Fall status | False |
| **acc_mag** | Acceleration magnitude | 0.845 |
| **subject** | Person ID (if available) | 1 |

**Table Features:**
- ✅ Scrollable
- ✅ Sortable by clicking column headers
- ✅ Full-width display
- ✅ Fixed height (300px)

---

### **Section 3: Risk Distribution Chart**

A bar chart showing how many activities fall into each risk category.

#### **What It Shows:**
```
        Risk Distribution
        
  300 ┤     ███
      │     ███
  200 │     ███  ███
      │     ███  ███
  100 │     ███  ███  ███
      │     ███  ███  ███
    0 └─────────────────────
          Low  Med  High
```

**Color Coding:**
- 🟢 **Green bar** = Low risk (good!)
- 🟡 **Yellow bar** = Medium risk (caution)
- 🔴 **Red bar** = High risk (danger)

**What to Look For:**
- **Ideal**: Tall green bar, short/no red bar
- **Concerning**: Tall red bar = many high-risk activities logged

---

### **Section 4: Activity Tracking Over Time**

Line chart showing activity changes across sample indices.

#### **Features:**

**Interactive Slider:**
```
Select data range: [50 ←─────○──────→ 500]
Currently viewing: 200 samples
```

**The Chart:**
```
Activity
   │
 6 ┤           ●
   │     ●           ●
 4 ┤ ●       ●           ●
   │     ●       ●
 2 ┤ ●       ●       ●
   │
 0 └─────────────────────────→ Time
     0    50   100  150  200
```

**Y-Axis**: Different activities (numbered)
**X-Axis**: Sample index (time progression)

**What It Shows:**
- Pattern of activity changes over time
- Frequency of activity switches
- Stability vs. variability

**How to Read:**
- **Flat horizontal lines** = Prolonged single activity (e.g., sleeping)
- **Frequent changes** = Active period with multiple activities
- **Jumps** = Activity transitions

---

### **Section 5: Fall Detection Analysis**

Comprehensive analysis of fall events in the logged data.

#### **5A: Fall Statistics Metrics**

Four key metrics displayed in a row:

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 🚨 Total    │ 📊 Total    │ 📈 Fall     │ ⚡ Status    │
│ Falls       │ Samples     │ Rate        │             │
│             │             │             │             │
│     15      │   1,247     │   1.20%     │ 🟡 WARNING  │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Metric Breakdowns:**

1. **Total Falls**
   - Count of detected fall events
   - Higher = more falls detected

2. **Total Samples**
   - Total number of activity samples in log
   - Context for fall rate

3. **Fall Rate**
   - Percentage of samples that are falls
   - Formula: `(Total Falls / Total Samples) × 100`
   - Example: 15 falls in 1,247 samples = 1.20%

4. **Status**
   - 🟢 `SAFE` - 0 falls
   - 🟡 `WARNING` - 1-5 falls
   - 🔴 `CRITICAL` - More than 5 falls

---

#### **5B: Fall Events Timeline**

Visual timeline showing where falls occurred in the sample sequence.

```
Fall Events Timeline

Normal │ ○○○○○○○○○○○●○○○○○○○○○●○○○○○○○○
       └────────────────────────────────→
       0        100       200       300
              Sample Index
       
○ = Normal activity
● = Fall detected (X marker)
```

**What It Shows:**
- Horizontal scatter plot of all samples
- Red X markers indicate fall events
- Gray dots show normal activities

**What to Look For:**
- **Clusters of falls** = Dangerous period
- **Isolated falls** = Random incidents
- **No falls** = Safe monitoring period

---

#### **5C: Risk Level Distribution**

Bar chart showing distribution across all risk levels.

```
     Distribution of Risk Levels
        
1000 ┤ ███
     │ ███
 750 │ ███
     │ ███      ███
 500 │ ███      ███
     │ ███      ███
 250 │ ███      ███      ███
     │ ███      ███      ███
   0 └──────────────────────
       Low    Medium   High
```

**With Value Labels:**
- Each bar shows exact count on top
- Colors: Green (Low), Yellow (Medium), Red (High)

**Interpretation:**
- Shows safety profile of entire log
- Ideal: Most samples in Low category

---

#### **5D: Detailed Fall Events Table**

If any falls are detected, shows detailed information.

```
📋 Detailed Fall Events

Index | Timestamp           | Activity | Risk Level
──────┼─────────────────────┼──────────┼───────────
  1   | 2026-01-06 09:15:32 | WALKING  | High
  2   | 2026-01-06 09:18:45 | STAIRS   | High
  3   | 2026-01-06 10:02:11 | RUNNING  | Critical
...
```

**Features:**
- Shows first 20 fall events
- Includes timestamp, activity, risk level
- Helps identify when/what caused falls

**If No Falls:**
```
✅ No fall events detected in the activity log!
```

---

### **When Historical Dashboard is Empty:**

If no log file exists:
```
⚠️ Fall detection data not available in the log file
```

---

# 2️⃣ Live Simulation
## 🔴 "Real-time activity monitoring with safety alerts"

### **Purpose:**
Simulate real-time activity recognition using test data, generate safety alerts, and monitor risk in real-time.

### **When to Use:**
- To test the system with new data
- To generate safety alerts for analysis
- To demonstrate the system's capabilities
- To validate model performance

---

## 🎯 Dashboard Sections Explained

### **Section 1: Model Loading Status**

Shows confirmation that the ML model loaded successfully:

```
✅ Model loaded successfully!
```

Or if there's an issue:
```
❌ Model file 'activity_model.pkl' not found! Please train the model first.
💡 Run the Jupyter notebook 'activity_recognition.ipynb' to train and save the model.
```

Also shows additional info:
```
ℹ️ Using supervised fall detection model from fall_detection.ipynb
```
or
```
⚠️ Supervised fall detection model not found, using motion-based heuristic
```

---

### **Section 2: Control Panel**

Four interactive controls for simulation configuration:

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│ ▶️ Start     │ Speed        │ Max Samples  │ 🚨 Enable    │
│ Simulation   │              │              │ Alerts       │
│              │              │              │              │
│   [Button]   │  ──○────     │    [100]     │    [✓]       │
│              │   0.5        │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

#### **Control 1: Start Simulation Button**
```
▶️ Start Simulation
```
- **Type**: Primary action button (purple/blue)
- **Function**: Begins the simulation
- **Effect**: Clears previous session, starts processing samples
- **Full width**: Easy to click

#### **Control 2: Speed Slider**
```
Speed: ──────○──────
Options: 0.1 | 0.3 | 0.5 | 1.0 | 2.0
Current: 0.5
```
- **What it does**: Controls simulation playback speed
- **Options explained**:
  - `0.1` = Very slow (10x slower, 10 seconds per sample)
  - `0.3` = Slow (3x slower, good for observation)
  - `0.5` = Normal (default, good balance) ⭐
  - `1.0` = Fast (real-time speed)
  - `2.0` = Very fast (2x speed, quick runs)
- **Default**: 0.5 seconds per sample

#### **Control 3: Max Samples Input**
```
Max Samples
  [  100  ]
Min: 10, Max: (dataset size)
```
- **What it does**: Sets how many samples to simulate
- **Range**: 10 to total test dataset size
- **Default**: 100 samples
- **Effect on runtime**: 
  - 10 samples @ 0.5 speed = ~5 seconds
  - 100 samples @ 0.5 speed = ~50 seconds
  - 500 samples @ 0.5 speed = ~4 minutes

#### **Control 4: Enable Alerts Checkbox**
```
🚨 Enable Alerts ☑
```
- **What it does**: Toggles safety alert generation
- **Default**: Checked (ON)
- **When ON**: 
  - Generates alerts during simulation
  - Stores alerts in session state
  - Critical alerts saved to log automatically
- **When OFF**:
  - No alerts generated
  - Faster processing
  - No data for Safety Alert System

---

### **Section 3: Live Monitoring Display**

Appears only while simulation is running.

#### **3A: Real-Time Metrics**

Four metrics updating every sample:

```
┌─────────────┬─────────────┬─────────────┬─────────────┐
│ 🏃 Activity │ 📊 Motion   │ 🛡️ Risk    │ 📍 Sample   │
│             │             │ Score       │             │
│  WALKING    │   0.842     │   45/100    │  23/100     │
│             │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┘
```

**Metric Updates:**
- **Activity**: Changes based on model prediction
- **Motion**: Shows current acceleration magnitude
- **Risk Score**: 0-100 scale, color-coded
- **Sample**: Progress (current/total)

---

#### **3B: Status Messages**

Dynamic status based on current sample analysis:

**Normal Status:**
```
✅ NORMAL: Movement within safe parameters
🟢 Low Risk - Stable condition
```

**Anomaly Detected:**
```
🔎 CAUTION: Unusual movement pattern
🟡 Medium Risk - Monitor closely
```

**High Risk Alert:**
```
⚠️ HIGH RISK: Significant motion spike detected
🟠 High Risk - Potential danger
```

**Fall Detected:**
```
🚨 CRITICAL: Likely FALL detected!
🔴 CRITICAL - Immediate attention required!
```

---

#### **3C: Progress Bar**

```
Simulation Progress:
[████████████░░░░░░░░] 60%
```
- Updates with each sample
- Visual indication of completion
- Color: Blue/Purple

---

### **Section 4: Alert Summary**

Appears after simulation completes (if alerts enabled).

#### **4A: Summary Metrics**

```
🚨 Alert Summary

┌─────────────┬─────────────┬─────────────┐
│ 📢 Total    │ 🔴 Critical/│ 💾 Save All │
│ Alerts      │ Emergency   │ Alerts      │
│             │             │             │
│     47      │      8      │  [Button]   │
└─────────────┴─────────────┴─────────────┘
```

**Metrics:**
1. **Total Alerts**: All alerts generated (INFO + WARNING + CRITICAL + EMERGENCY)
2. **Critical/Emergency**: High-severity alerts only
3. **Save Button**: Manually save all alerts to historical log

---

#### **4B: Alerts by Severity Chart**

Bar chart showing breakdown:

```
Alerts by Severity

40 ┤          ███
   │          ███
30 │          ███
   │  ███     ███
20 │  ███     ███
   │  ███     ███     ███
10 │  ███     ███     ███     ███
   │  ███     ███     ███     ███
 0 └───────────────────────────────
    INFO   WARNING CRITICAL EMERGENCY
```

---

#### **4C: Critical Alerts Detail**

If critical/emergency alerts were generated:

```
⚠️ 8 Critical/Emergency Alerts Detected

▼ View Critical Alerts (expandable)

Alert #1
🚨 EMERGENCY - FALL_DETECTED
Activity: WALKING
Risk Score: 95/100
Motion Intensity: 2.834
Message: 🚨 EMERGENCY: Fall detected during WALKING
Action Required: Immediate medical assistance required
───────────────────────────────────

Alert #2
🔴 CRITICAL - HIGH_RISK_MOTION
...
```

**Features:**
- Collapsible expander (doesn't clutter screen)
- Shows detailed info for each critical alert
- Easy to review dangerous events

---

### **Section 5: Simulation Summary**

Statistics for the simulated samples only.

```
📊 Simulation Summary

📍 Analysis based on 100 simulated samples (out of 2,947 total)
```

#### **5A: Three-Column Summary**

```
┌─────────────────┬─────────────────┬─────────────────┐
│ 🔎 Anomaly      │ 🚨 Fall         │ ⚠️ Safety       │
│ Detection       │ Detection       │ Alerts          │
│                 │                 │                 │
│ Unusual         │ Fall Events     │ High-Risk       │
│ Movements: 12   │ Detected: 3     │ Alerts: 8       │
│ 12.0% of        │ 3.0% of         │ 8.0% of         │
│ samples         │ samples         │ samples         │
│ [Progress Bar]  │ ✅ Status       │ [Warning]       │
└─────────────────┴─────────────────┴─────────────────┘
```

**Each Column Explains:**
- **Count**: Number of events
- **Percentage**: Relative to simulated samples
- **Progress bar or status** indicator

---

#### **5B: Activity Distribution**

Shows what activities were predicted during simulation.

```
📈 Activity Distribution
Distribution of activities in the 100 simulated samples

        Bar Chart:
10 ┤ ███
   │ ███
 8 │ ███  ███
   │ ███  ███
 6 │ ███  ███  ███
   │ ███  ███  ███
 4 │ ███  ███  ███  ███
   │ ███  ███  ███  ███  ███
 2 │ ███  ███  ███  ███  ███  ███
   │ ███  ███  ███  ███  ███  ███
 0 └──────────────────────────────────
    WALK  SIT  STAND LAY  STAIR  RUN
```

---

#### **5C: Detailed Activity Breakdown**

```
📋 Detailed Activity Breakdown

┌────────────────┬────────────┬────────────────┐
│ Activity       │ Count      │ Percentage     │
├────────────────┼────────────┼────────────────┤
│ WALKING        │ 35         │ 35.00%         │
│ SITTING        │ 28         │ 28.00%         │
│ STANDING       │ 20         │ 20.00%         │
│ LAYING         │ 12         │ 12.00%         │
│ WALKING_UP     │ 3          │ 3.00%          │
│ WALKING_DOWN   │ 2          │ 2.00%          │
└────────────────┴────────────┴────────────────┘
```

Plus summary metrics:
```
┌─────────────────┬─────────────────┬─────────────────┐
│ Total Activities│ Most Common     │ Least Common    │
│        6        │    WALKING      │  WALKING_DOWN   │
└─────────────────┴─────────────────┴─────────────────┘
```

---

# 3️⃣ Dataset Explorer
## 📈 "Explore the raw sensor data"

### **Purpose:**
Examine the raw test dataset to understand the data structure, features, and distributions before simulation.

### **When to Use:**
- To understand what data you're working with
- To check dataset quality
- To see available features
- To verify activity distributions

---

## 🎯 Dashboard Sections Explained

### **Section 1: Dataset Information**

Top-level summary:

```
✅ Loaded 2,947 samples from test dataset

┌─────────────┬─────────────┬─────────────┐
│ Total       │ Features    │ Activities  │
│ Samples     │             │             │
│             │             │             │
│   2,947     │     563     │      6      │
└─────────────┴─────────────┴─────────────┘
```

**Metrics Explained:**
- **Total Samples**: Number of rows in dataset
- **Features**: Number of columns (sensor measurements + metadata)
- **Activities**: Number of unique activity types

---

### **Section 2: Sample Data**

Shows first 20 rows of the dataset:

```
📋 Sample Data

[Interactive Scrollable Table]

Row | tBodyAcc-X | tBodyAcc-Y | tBodyAcc-Z | ... | Activity | subject
────┼────────────┼────────────┼────────────┼─────┼──────────┼────────
1   | 0.257      | -0.023     | -0.014     | ... | WALKING  | 1
2   | 0.286      | -0.013     | -0.119     | ... | WALKING  | 1
3   | 0.275      | -0.026     | -0.067     | ... | WALKING  | 1
...
20  | 0.298      | -0.031     | -0.124     | ... | SITTING  | 2
```

**Features:**
- Scrollable horizontally (many columns)
- Shows actual sensor values
- Gives sense of data scale and format

---

### **Section 3: Activity Distribution**

Visual breakdown of activity types in dataset:

```
🎯 Activity Distribution

        Bar Chart:
800 ┤ ███
    │ ███
600 │ ███
    │ ███  ███
400 │ ███  ███  ███
    │ ███  ███  ███  ███
200 │ ███  ███  ███  ███  ███
    │ ███  ███  ███  ███  ███  ███
  0 └──────────────────────────────────
     WALK  SIT  STAND LAY  UP   DOWN
```

**What to Look For:**
- **Balanced bars** = Good dataset (all activities well-represented)
- **Unbalanced bars** = Some activities over/under-represented
  - Can affect model performance
  - Model may be better at predicting common activities

---

### **Section 4: Feature Statistics**

Statistical summary of all features:

```
📊 Feature Statistics

[Scrollable Table]

Feature        | count  | mean    | std     | min     | 25%     | 50%     | 75%     | max
───────────────┼────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────
tBodyAcc-X     | 2947.0 | 0.274   | 0.166   | -0.876  | 0.221   | 0.277   | 0.318   | 0.823
tBodyAcc-Y     | 2947.0 | -0.017  | 0.097   | -0.542  | -0.024  | -0.017  | -0.010  | 0.542
tBodyAcc-Z     | 2947.0 | -0.109  | 0.098   | -0.623  | -0.121  | -0.109  | -0.098  | 0.456
...
```

**Columns Explained:**
- **count**: Number of non-null values
- **mean**: Average value
- **std**: Standard deviation (variability)
- **min**: Minimum value
- **25%/50%/75%**: Quartiles
- **max**: Maximum value

**What to Look For:**
- **No missing values** (count = 2947 for all)
- **Reasonable ranges** (not all zeros, no extreme outliers)
- **Meaningful variation** (std > 0)

---

### **When Dataset Not Found:**

```
❌ Test dataset not found!
```

---

# 4️⃣ Safety Alert System
## 🚨 "Analyze safety alerts from current session"

### **Purpose:**
Comprehensive analysis of safety alerts generated during the current (most recent) live simulation session, with intelligent notification panel.

### **When to Use:**
- After running a live simulation with alerts enabled
- To review what triggered alerts
- To assess overall safety of the simulation
- To decide if safety protocols need adjustment

---

## 🎯 Dashboard Sections Explained

### **Section 1: Current Session Overview**

Top-level metrics from the simulation you just ran:

```
📊 Current Session Overview

┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│ 📢 Total    │ 🚨 Emerg.   │ 🔴 Critical │ ⚡ Avg Risk  │ 📊 Samples  │
│ Alerts      │             │             │             │             │
│             │             │             │             │             │
│     47      │      2      │      6      │   38.5/100  │     100     │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

**Metrics Explained:**
1. **Total Alerts**: All alerts (INFO + WARNING + CRITICAL + EMERGENCY)
2. **Emergencies**: Fall-detected alerts only (highest severity)
3. **Critical**: Dangerous motion spikes
4. **Avg Risk**: Average risk score of all samples (0-100)
5. **Samples**: Number of samples you simulated

---

### **Section 2: Visual Analytics**

Two side-by-side charts:

#### **2A: Alerts by Severity (Left)**

```
📊 Alerts by Severity

40 ┤          ███
   │          ███
30 │          ███
   │  ███     ███
20 │  ███     ███
   │  ███     ███     ███
10 │  ███     ███     ███     ███
   │  ███     ███     ███     ███
 0 └───────────────────────────────
    INFO   WARNING CRITICAL EMERGENCY

Values shown on bars: 25, 14, 6, 2
```

**Colors:**
- 🔵 INFO = Blue
- 🟡 WARNING = Orange
- 🔴 CRITICAL = Red
- ⚫ EMERGENCY = Dark Red

**What to Look For:**
- Most alerts should be INFO/WARNING
- Few CRITICAL/EMERGENCY = good
- Many EMERGENCY = serious safety concern

---

#### **2B: Alerts by Activity (Right)**

```
🎯 Alerts by Activity

Top 10 Activities with Alerts

WALKING_UPSTAIRS   ████████████ 15
WALKING            ██████████ 12
RUNNING            ████████ 9
STAIRS             ██████ 7
SITTING            ████ 5
...
```

**What It Shows:**
- Which activities triggered most alerts
- Horizontal bar chart
- Only top 10 shown

**What to Look For:**
- High-risk activities (stairs, running) should have more alerts - normal
- SITTING/LAYING with many alerts = concerning (shouldn't be risky)

---

### **Section 3: Alert Types Breakdown**

```
📋 Alert Types

[Bar Chart - Left Column]                [Metrics - Right Column]

FALL_DETECTED        ███                  Fall Detected: 2
HIGH_RISK_MOTION     ██████               High Risk Motion: 6
ANOMALY_DETECTED     ██████████           Anomaly Detected: 14
ELEVATED_RISK        ████████████████     Elevated Risk: 25
```

**Alert Types Explained:**
1. **FALL_DETECTED**: Model detected a fall event
2. **HIGH_RISK_MOTION**: Acceleration spike > 3.5 std devs
3. **ANOMALY_DETECTED**: Unusual movement pattern
4. **ELEVATED_RISK**: Risk score ≥ 60

---

### **Section 4: Recent Alerts Table**

Detailed table of alerts with filters:

#### **4A: Alert Display Slider**
```
Number of alerts to display: [5 ←───○──────→ 50]
Currently showing: 20
```

#### **4B: Filter Controls**

```
┌──────────────────────────┬──────────────────────────┐
│ Filter by Severity:      │ Filter by Type:          │
│                          │                          │
│ ☑ INFO                   │ ☑ FALL_DETECTED          │
│ ☑ WARNING                │ ☑ HIGH_RISK_MOTION       │
│ ☑ CRITICAL               │ ☑ ANOMALY_DETECTED       │
│ ☑ EMERGENCY              │ ☑ ELEVATED_RISK          │
└──────────────────────────┴──────────────────────────┘
```

**How to Use:**
- Uncheck severities/types you don't want to see
- Table updates automatically
- Helps focus on specific alert types

#### **4C: Alerts Data Table**

```
[Scrollable Table - Height: 400px]

Timestamp           | Severity  | Type              | Activity | Risk | Message
────────────────────┼───────────┼───────────────────┼──────────┼──────┼────────────────────
2026-01-06 10:15:32 | EMERGENCY | FALL_DETECTED     | WALKING  | 95   | 🚨 EMERGENCY: Fall...
2026-01-06 10:15:45 | CRITICAL  | HIGH_RISK_MOTION  | STAIRS   | 87   | ⚠️ CRITICAL: Dang...
2026-01-06 10:16:02 | WARNING   | ANOMALY_DETECTED  | JOGGING  | 65   | 🔎 WARNING: Unusu...
...
```

**Features:**
- Shows most recent alerts (based on slider)
- Full-width, scrollable
- Can sort by clicking columns

---

### **Section 5: Export and Save Options**

```
┌───────────────────────────────┬───────────────────────────────┐
│ 📥 Export Current Session     │ 💾 Save All Session Alerts    │
│ Alerts to CSV                 │ to Historical Log             │
│                               │                               │
│ [Button]                      │ [Button]                      │
└───────────────────────────────┴───────────────────────────────┘
```

#### **Export Button:**
- Downloads CSV file of current session alerts
- Filename format: `session_alerts_20260106_103015.csv`
- Contains all alert details

#### **Save Button:**
- Saves alerts to permanent `safety_alerts.csv` log
- Shows confirmation: `✅ Saved 47 alerts to historical log!`
- Alerts then appear in historical view

---

### **Section 6: 🔔 SYSTEM NOTIFICATIONS PANEL** ⭐

**THE MOST IMPORTANT SECTION**

This is the intelligent threshold-based notification system.

#### **Panel Purpose:**
- Automatically checks if critical/emergency alerts exceed 10% of simulated samples
- Provides clear visual warning if safety is concernedthreshold exceeded
- Helps assess overall safety of the monitoring session

---

#### **Scenario A: THRESHOLD EXCEEDED** 🚨

When `(Critical + Emergency) > 10% of samples`:

```
╔══════════════════════════════════════════════════════════════╗
║  🚨 CRITICAL ALERT THRESHOLD EXCEEDED                        ║
╠══════════════════════════════════════════════════════════════╣
║  Warning: Critical and Emergency alerts have exceeded the   ║
║  10% threshold!                                              ║
║                                                              ║
║  • Current Level: 15.00% (15 critical/emergency alerts      ║
║    out of 100 samples)                                       ║
║  • Threshold: 10.0% of samples                              ║
║  • Recommended Action: Review safety protocols and          ║
║    increase monitoring frequency                             ║
╚══════════════════════════════════════════════════════════════╝
```

**Additional Warning:**
```
⚠️ ATTENTION REQUIRED: 15 CRITICAL/EMERGENCY alerts in 100 samples
(15.00% - Threshold: 10.0%)
```

**Progress Bar:**
```
[███████████████░░░░░] 15%
```
- Shows how far above 0% you are
- Red/orange color to indicate danger

**Bottom Metrics:**
```
┌─────────────────┬─────────────┬─────────────┬─────────────┐
│ Critical/Emerg. │ Threshold   │ Status      │ Margin      │
│ %               │             │             │             │
│                 │             │             │             │
│ 15.00%          │ 10.0%       │ 🔴 EXCEEDED │ -5.00%      │
│ ▲ +5.00%        │             │             │             │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

**Delta Explanation:**
- `▲ +5.00%` = You're 5% ABOVE threshold (bad, shows in red)
- **Status**: 🔴 EXCEEDED
- **Margin**: -5.00% (negative = over threshold)

---

#### **Scenario B: NORMAL STATUS** ✅

When `(Critical + Emergency) ≤ 10% of samples`:

```
╔══════════════════════════════════════════════════════════════╗
║  ✅ SYSTEM STATUS NORMAL                                     ║
╠══════════════════════════════════════════════════════════════╣
║  Critical and Emergency alerts are within acceptable limits. ║
║                                                              ║
║  • Current Level: 5.00% (5 critical/emergency alerts        ║
║    out of 100 samples)                                       ║
║  • Threshold: 10.0% of samples                              ║
║  • Status: Continue regular monitoring                       ║
╚══════════════════════════════════════════════════════════════╝
```

**Success Message:**
```
✓ System operating normally - 5.00% critical/emergency rate
(Below 10.0% threshold)
```

**Progress Bar:**
```
[████████░░░░░░░░░] 5%
```
- Green color
- Shows current percentage

**Bottom Metrics:**
```
┌─────────────────┬─────────────┬─────────────┬─────────────┐
│ Critical/Emerg. │ Threshold   │ Status      │ Margin      │
│ %               │             │             │             │
│                 │             │             │             │
│ 5.00%           │ 10.0%       │ 🟢 NORMAL   │  5.00%      │
│ ▼ -5.00%        │             │             │             │
└─────────────────┴─────────────┴─────────────┴─────────────┘
```

**Delta Explanation:**
- `▼ -5.00%` = You're 5% BELOW threshold (good, shows in green)
- **Status**: 🟢 NORMAL
- **Margin**: 5.00% (positive = safety buffer)

---

#### **Notification Panel Math:**

```python
# Example Calculation:
total_samples = 100          # You simulated 100 samples
emergency_count = 2          # 2 fall detections
critical_count = 6           # 6 high-risk motion spikes

critical_emergency_count = 2 + 6 = 8
critical_percentage = (8 / 100) × 100 = 8.00%

THRESHOLD = 10.0%

if 8.00% > 10.0%:
    # Show RED warning panel
else:
    # Show GREEN normal panel ✓
```

---

### **When No Simulation Has Been Run:**

```
📝 No alerts from current simulation session. Run a simulation
with alerts enabled to generate safety alerts.

### How to Generate Alerts:

1. Go to 🔴 Live Simulation mode
2. Enable the 🚨 Enable Alerts checkbox
3. Run the simulation
4. Return to this Safety Alert System to view the alerts
   from your simulation

The system will detect and alert for:
- 🚨 EMERGENCY: Fall events
- 🔴 CRITICAL: Dangerous motion spikes
- ⚠️ WARNING: Anomalies and high-risk activities
- ℹ️ INFO: Elevated risk levels
```

**Optional Historical View:**
```
───────────────────────────────────────────

📜 Historical Alerts (Previous Sessions)

☐ Show historical alerts from log file
   (Click to view alerts from previous sessions)
```

---

# 🎯 Dashboard Navigation

### **Sidebar:**

```
┌──────────────────────────────┐
│  [Icon: Activity History]    │
│                              │
│  Navigation                  │
│  ───────────                 │
│                              │
│  Select Mode:                │
│  ○ 📊 Historical Dashboard   │
│  ○ 🔴 Live Simulation        │
│  ○ 📈 Dataset Explorer       │
│  ● 🚨 Safety Alert System    │
│                              │
│  ───────────────────────────│
│                              │
│  ℹ️ This system monitors     │
│  human activities and        │
│  detects safety risks in     │
│  real-time using advanced    │
│  ML algorithms.              │
│                              │
│  ───────────────────────────│
│                              │
│  📊 Total Records: 1,247     │
│  🚨 Falls Detected: 15       │
│                              │
└──────────────────────────────┘
```

---

# 📋 Dashboard Comparison Table

| Feature | Historical | Live Sim | Dataset Explorer | Safety Alerts |
|---------|-----------|----------|------------------|---------------|
| **View past data** | ✅ | ❌ | ❌ | Partial |
| **Real-time monitoring** | ❌ | ✅ | ❌ | ❌ |
| **Generate alerts** | ❌ | ✅ | ❌ | ❌ |
| **View raw data** | Partial | ❌ | ✅ | ❌ |
| **Alert analysis** | ❌ | Partial | ❌ | ✅ |
| **Notification panel** | ❌ | ❌ | ❌ | ✅ |
| **Export data** | ❌ | ✅ | ❌ | ✅ |
| **Visualizations** | ✅ | ✅ | ✅ | ✅ |
| **Requires simulation** | ❌ | ✅ | ❌ | ✅ |

---

# 🎯 Recommended Workflow

### For New Users:
1. **Dataset Explorer** - Understand your data
2. **Live Simulation** - Run a test with 100 samples
3. **Safety Alert System** - Review alerts and notification
4. **Historical Dashboard** - Compare with past data

### For Regular Monitoring:
1. **Live Simulation** - Run monitoring session
2. **Safety Alert System** - Check notification panel
3. If threshold exceeded → Investigate further
4. **Historical Dashboard** - Track trends over time

---

# 💡 Tips and Best Practices

### Dashboard Usage Tips:

1. **Start Small**: Begin with 50-100 samples in Live Simulation
2. **Watch the Notification Panel**: It's your primary safety indicator
3. **Enable Alerts**: Always keep "Enable Alerts" checked
4. **Save Important Sessions**: Use "Save to Historical Log" for critical sessions
5. **Compare Sessions**: Run multiple simulations to see patterns

### Interpretation Tips:

1. **10% Threshold**: Treat as a serious warning, not absolute danger
2. **Context Matters**: High-risk activities naturally generate more alerts
3. **Trends**: Multiple sessions with high alerts = pattern to investigate
4. **Distribution**: Look at severity distribution, not just totals

---

# ❓ Frequently Asked Questions

### Q1: Why don't I see any dashboards?
**A:** Make sure you have the required files:
- `activity_model.pkl` for Live Simulation
- `activity_tracking_log.csv` for Historical Dashboard
- `data/test.csv` for Dataset Explorer

### Q2: What's the difference between Historical and Safety Alert dashboards?
**A:** 
- **Historical** = Past activity logs from all simulations
- **Safety Alerts** = Current session alerts only

### Q3: Why is the notification panel showing 0%?
**A:** No critical/emergency alerts were generated. This is good! It means your simulation was safe.

### Q4: Can I change the 10% threshold?
**A:** Currently hardcoded to 10%, but you can modify `CRITICAL_THRESHOLD` in `app.py` line ~873.

### Q5: What happens when I start a new simulation?
**A:** Previous session alerts are cleared. The Safety Alert System resets to show only new simulation data.

---

# 📚 Summary

You now have **4 powerful dashboards** for comprehensive activity monitoring:

1. **📊 Historical** - Review past performance
2. **🔴 Live Sim** - Monitor in real-time
3. **📈 Dataset Explorer** - Understand your data
4. **🚨 Safety Alerts** - Intelligent safety assessment

Each serves a unique purpose in the complete monitoring workflow!
