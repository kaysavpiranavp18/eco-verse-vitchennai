# Activity Recognition Notebook - Complete Explanation

## Overview
The `activity_recognition.ipynb` notebook is a comprehensive machine learning project that trains a model to recognize different human activities (like WALKING, SITTING, STANDING, etc.) using sensor data from smartphones or wearable devices.

---

## Part 1: Environment Setup and Library Installation

### Cell 1: Installing Required Libraries
```python
!pip install pandas numpy matplotlib scikit-learn openpyxl
```

**Purpose:** Installs all necessary Python libraries for the project.

**Libraries Explained:**
- **pandas**: For data manipulation and CSV file handling
- **numpy**: For numerical computations and array operations
- **matplotlib**: For creating visualizations and plots
- **scikit-learn**: Machine learning library containing classification algorithms
- **openpyxl**: For reading/writing Excel files

---

## Part 2: Importing Libraries

### Cell 2: Import Statements
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
```

**Purpose:** Import all the libraries we'll use in the notebook.

**What Each Library Does:**
- `pandas as pd`: Data manipulation (read CSV, create DataFrames)
- `numpy as np`: Numerical operations (arrays, math functions)
- `matplotlib.pyplot as plt`: Creating charts and visualizations
- `train_test_split`: Splits data into training and testing sets
- `RandomForestClassifier`: The machine learning algorithm we use
- `accuracy_score, classification_report, confusion_matrix`: Evaluate model performance
- `joblib`: Save and load trained models

---

## Part 3: Loading the Dataset

### Cell 3: Load Training Data
```python
# Load the training dataset
train_data = pd.read_csv('data/train.csv')

# Display first few rows
print("Training data shape:", train_data.shape)
print("\\nFirst 5 rows:")
display(train_data.head())
```

**Purpose:** Load the training data from a CSV file.

**What It Does:**
1. Reads the `train.csv` file from the `data` folder
2. Stores it in a DataFrame called `train_data`
3. Shows the shape (number of rows and columns)
4. Displays the first 5 rows to inspect the data

**Understanding the Data:**
- **Rows**: Each row represents one time window of sensor readings
- **Columns**: Features extracted from accelerometer and gyroscope sensors
  - `tBodyAcc-mean()-X`: Mean body acceleration in X-axis
  - `tBodyAcc-mean()-Y`: Mean body acceleration in Y-axis
  - `tBodyAcc-std()-Z`: Standard deviation of body acceleration in Z-axis
  - And many more sensor features...
  - `Activity`: The target variable (what activity the person was doing)
  - `subject`: Which person (1-30) performed the activity

---

## Part 4: Data Exploration

### Cell 4: Explore the Data
```python
# Check data info
print("Dataset Information:")
print(train_data.info())

# Check for missing values
print("\\nMissing Values:")
print(train_data.isnull().sum().sum())

# Check activity distribution
print("\\nActivity Distribution:")
print(train_data['Activity'].value_counts())
```

**Purpose:** Understand the structure and quality of the data.

**What It Shows:**
1. **Data types**: All features should be numeric (float64)
2. **Missing values**: Ideally should be 0
3. **Activity distribution**: How many samples for each activity

**Activity Types** (usually 6):
- WALKING
- WALKING_UPSTAIRS
- WALKING_DOWNSTAIRS
- SITTING
- STANDING
- LAYING

---

## Part 5: Data Visualization

### Cell 5: Visualize Activity Distribution
```python
# Create a bar chart of activities
plt.figure(figsize=(12, 6))
activity_counts = train_data['Activity'].value_counts()
plt.bar(activity_counts.index, activity_counts.values, color='skyblue', edgecolor='black')
plt.xlabel('Activity Type', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Distribution of Activities in Training Data', fontsize=14, fontweight='bold')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.show()
```

**Purpose:** Visualize how balanced the dataset is across different activities.

**What to Look For:**
- **Balanced dataset**: All bars should be roughly the same height
- **Imbalanced dataset**: Some activities have significantly more/fewer samples
  - This can affect model performance

---

## Part 6: Feature Engineering

### Cell 6: Prepare Features and Target
```python
# Separate features (X) and target (y)
X = train_data.drop(columns=['Activity', 'subject'], errors='ignore')
y = train_data['Activity']

print("Features shape:", X.shape)
print("Target shape:", y.shape)
print("\\nNumber of features:", X.shape[1])
print("Number of samples:", X.shape[0])
```

**Purpose:** Prepare the data for machine learning.

**What It Does:**
1. **X (Features)**: All sensor data columns (561 features typically)
   - Removes 'Activity' column (this is what we're predicting)
   - Removes 'subject' column (person ID is not a useful feature)

2. **y (Target)**: Just the 'Activity' column
   - This is what we want the model to predict

**Why We Do This:**
- Machine learning models need to be trained on features (X) to predict targets (y)
- We don't include the target or subject ID as features

---

## Part 7: Splitting the Data

### Cell 7: Train-Test Split
```python
# Split data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(
    X, y, 
    test_size=0.2,  # 20% for validation
    random_state=42,  # For reproducibility
    stratify=y  # Keep same activity distribution in both sets
)

print("Training set size:", X_train.shape[0])
print("Validation set size:", X_val.shape[0])
```

**Purpose:** Create separate datasets for training and evaluation.

**Parameters Explained:**
- `test_size=0.2`: Use 20% of data for validation, 80% for training
- `random_state=42`: Makes the split reproducible (same split every time)
- `stratify=y`: Ensures both sets have similar activity distributions

**Why We Do This:**
- **Training set**: Used to teach the model
- **Validation set**: Used to test how well the model learned
- This prevents "overfitting" (memorizing instead of learning)

---

## Part 8: Model Training

### Cell 8: Train Random Forest Classifier
```python
# Create and train the model
model = RandomForestClassifier(
    n_estimators=100,  # Number of decision trees
    random_state=42,  # For reproducibility
    n_jobs=-1,  # Use all CPU cores
    max_depth=None,  # Trees can grow to full depth
    min_samples_split=2,  # Minimum samples to split a node
    verbose=1  # Show progress
)

print("Training Random Forest model...")
model.fit(X_train, y_train)
print("✓ Training completed!")
```

**Purpose:** Create and train the machine learning model.

**Random Forest Explained:**
- An ensemble of decision trees (100 trees in this case)
- Each tree makes a prediction
- Final prediction is the majority vote

**Parameters:");
- `n_estimators=100`: Creates 100 decision trees
- `n_jobs=-1`: Uses all available CPU cores for faster training
- `max_depth=None`: Trees can grow as deep as needed
- `random_state=42`: Makes results reproducible

**What Happens During Training:**
- The model analyzes patterns in the sensor data
- Learns which feature values correspond to which activities
- Takes a few minutes depending on dataset size

--- ## Part 9: Model Evaluation

### Cell 9: Evaluate on Validation Set
```python
# Make predictions on validation set
y_pred = model.predict(X_val)

# Calculate accuracy
accuracy = accuracy_score(y_val, y_pred)
print(f"\\n✓ Model Accuracy: {accuracy * 100:.2f}%")

# Classification report
print("\\nClassification Report:")
print(classification_report(y_val, y_pred))
```

**Purpose:** Test how well the model performs on unseen data.

**Metrics Explained:**

1. **Accuracy**: Percentage of correct predictions
   - Example: 95% means 95 out of 100 predictions are correct

2. **Classification Report** shows for each activity:
   - **Precision**: Of all predictions for this activity, how many were correct?
   - **Recall**: Of all actual instances of this activity, how many did we find?
   - **F1-Score**: Harmonic mean of precision and recall (overall quality)
   - **Support**: Number of actual occurrences in validation set

**Good Performance Indicators:**
- Accuracy > 90%
- F1-scores > 0.85 for all activities

---

## Part 10: Confusion Matrix Visualization

### Cell 10: Plot Confusion Matrix
```python
# Create confusion matrix
cm = confusion_matrix(y_val, y_pred)

# Visualize as heatmap
plt.figure(figsize=(10, 8))
plt.imshow(cm, interpolation='nearest', cmap='Blues')
plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
plt.colorbar()

# Add labels
classes = model.classes_
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)

# Add values to cells
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        plt.text(j, i, format(cm[i, j], 'd'),
                ha="center", va="center",
                color="white" if cm[i, j] > cm.max() / 2 else "black")

plt.ylabel('True label')
plt.xlabel('Predicted label')
plt.tight_layout()
plt.show()
```

**Purpose:** Visualize where the model makes mistakes.

**How to Read It:**
- **Rows**: Actual activities
- **Columns**: Predicted activities
- **Diagonal** (top-left to bottom-right): Correct predictions
- **Off-diagonal**: Mistakes

**Example:**
- If row "SITTING" and column "STANDING" has value 15:
  - 15 times the model predicted STANDING when the person was actually SITTING

**What to Look For:**
- Dark blue diagonal = good (many correct predictions)
- Light colors off diagonal = bad (many mistakes)

---

## Part 11: Feature Importance

### Cell 11: Analyze Feature Importance
```python
# Get feature importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

# Plot top 20 features
plt.figure(figsize=(12, 8))
top_n = 20
plt.barh(range(top_n), importances[indices[:top_n]], color='teal')
plt.yticks(range(top_n), X.columns[indices[:top_n]])
plt.xlabel('Importance Score')
plt.title(f'Top {top_n} Most Important Features', fontsize=14, fontweight='bold')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()
```

**Purpose:** Understand which sensor features are most useful for predictions.

**What It Shows:**
- Features ranked by importance (how much they help the model decide)
- Higher score = more important for classification

**Common Important Features:**
- Body acceleration statistics (mean, std, max, min)
- Gravity acceleration components
- Angular velocity from gyroscope
- Frequency domain features

---

## Part 12: Save the Model

### Cell 12: Export Trained Model
```python
# Save model to file
model_filename = 'activity_model.pkl'
joblib.dump(model, model_filename)
print(f"✓ Model saved successfully as '{model_filename}'")

# Show model size
import os
model_size = os.path.getsize(model_filename) / (1024 * 1024)  # Convert to MB
print(f"Model file size: {model_size:.2f} MB")
```

**Purpose:** Save the trained model so it can be used in other applications.

**File Format:**
- `.pkl` (pickle): Python serialization format
- Can be loaded later without retraining

**Usage:**
- This saved model is used in `app.py` for the live simulation
- Can be deployed in production applications

---

## Part 13: Test on New Data

### Cell 13: Load and Test on Test Set
```python
# Load test data
test_data = pd.read_csv('data/test.csv')
print("Test data shape:", test_data.shape)

# Prepare test features
X_test = test_data.drop(columns=['Activity', 'subject'], errors='ignore')
y_test = test_data['Activity']

# Make predictions
test_predictions = model.predict(X_test)

# Evaluate
test_accuracy = accuracy_score(y_test, test_predictions)
print(f"\\nTest Set Accuracy: {test_accuracy * 100:.2f}%")
```

**Purpose:** Final evaluation on completely unseen data.

**Why This Matters:**
- Validation set was used during model development
- Test set is truly unseen - best indicator of real-world performance
- Gap between validation and test accuracy indicates overfitting

---

## Part 14: Create Sample Predictions

### Cell 14: Demonstrate Real Predictions
```python
# Take 10 random samples from test set
sample_indices = np.random.choice(len(X_test), 10, replace=False)
samples = X_test.iloc[sample_indices]
actual = y_test.iloc[sample_indices]
predicted = model.predict(samples)

# Display results
results_df = pd.DataFrame({
    'Sample #': range(1, 11),
    'Actual Activity': actual.values,
    'Predicted Activity': predicted,
    'Correct?': actual.values == predicted
})

print("\\nSample Predictions:")
display(results_df)
print(f"\\nCorrect: {results_df['Correct?'].sum()}/10")
```

**Purpose:** Show real examples of the model making predictions.

**What It Shows:**
- Side-by-side comparison of actual vs predicted activities
- Helps understand model behavior on individual samples

---

## Key Takeaways

### What This Notebook Accomplishes:
1. **Loads sensor data** from smartphones/wearables
2. **Prepares the data** by separating features and targets
3. **Trains a Random Forest model** to recognize activities
4. **Evaluates performance** using accuracy, precision, recall
5. **Visualizes results** with confusion matrices and charts
6. **Saves the model** for use in production applications

### Machine Learning Workflow:
1. **Load Data** → 2. **Explore Data** → 3. **Prepare Features** → 
4. **Split Data** → 5. **Train Model** → 6. **Evaluate** → 
7. **Save Model** → 8. **Deploy**

### Typical Performance:
- **Expected Accuracy**: 90-95%
- **Training Time**: 2-5 minutes
- **Number of Features**: ~561 sensor measurements
- **Number of Activities**: 6 (WALKING, SITTING, STANDING, etc.)

### Real-World Applications:
- **Fitness tracking**: Automatic activity logging
- **Health monitoring**: Detect falls or unusual patterns
- **Smart homes**: Context-aware automation
- **Elderly care**: Monitor activity levels

---

## Common Issues and Solutions

### Issue 1: Low Accuracy (<80%)
**Possible Causes:**
- Not enough training data
- Imbalanced classes
- Poor feature quality

**Solutions:**
- Collect more data
- Use class weights
- Try different features

### Issue 2: Model Too Slow
**Solutions:**
- Reduce `n_estimators` (e.g., 50 instead of 100)
- Use feature selection to reduce dimensions
- Try a different algorithm (e.g., SVM, Gradient Boosting)

### Issue 3: Overfitting (Training accuracy >> Test accuracy)
**Solutions:**
- Increase `min_samples_split`
- Set `max_depth` to limit tree depth
- Use cross-validation
- Collect more diverse training data

---

## Next Steps

After completing this notebook, you can:

1. **Optimize hyperparameters** using GridSearchCV
2. **Try different algorithms** (SVM, Neural Networks, XGBoost)
3. **Collect more data** to improve accuracy
4. **Deploy the model** in a mobile app or web service
5. **Add more activities** to recognize
6. **Create an API** for real-time predictions

---

## File Dependencies

**Input Files:**
- `data/train.csv`: Training dataset with sensor features
- `data/test.csv`: Test dataset for evaluation

**Output Files:**
- `activity_model.pkl`: Saved trained model
- Various plots and visualizations

**Required Libraries:**
- pandas, numpy, matplotlib, scikit-learn, joblib

---

## Mathematical Concepts Used

### Random Forest Algorithm:
- **Ensemble method**: Combines multiple decision trees
- **Bootstrap aggregating** (bagging): Each tree trained on random sample
- **Feature randomness**: Each split considers random subset of features
- **Voting**: Final prediction is majority vote of all trees

### Evaluation Metrics:
- **Accuracy** = (Correct Predictions) / (Total Predictions)
- **Precision** = (True Positives) / (True Positives + False Positives)
- **Recall** = (True Positives) / (True Positives + False Negatives)
- **F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)

---

## Summary

The `activity_recognition.ipynb` notebook is a complete end-to-end machine learning pipeline that:
- Takes raw sensor data from smartphones
- Processes and prepares it for machine learning
- Trains a Random Forest classifier
- Evaluates performance with multiple metrics
- Saves the model for use in production

**The result**: A trained model that can recognize human activities from sensor data with high accuracy, which is then used in the Streamlit application (`app.py`) for real-time activity monitoring and safety alerting.
