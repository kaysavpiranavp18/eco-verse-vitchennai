"""
Train Activity Recognition Model
This script trains a Random Forest classifier on the training data
and saves it for use in the Streamlit dashboard.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
from pathlib import Path

print("=" * 60)
print("Activity Recognition Model Training")
print("=" * 60)

# Load training data
train_path = Path("data/train.csv") if Path("data/train.csv").exists() else Path("train.csv")
test_path = Path("data/test.csv") if Path("data/test.csv").exists() else Path("test.csv")

if not train_path.exists():
    print("❌ Error: Training data not found!")
    print(f"   Looking for: {train_path}")
    exit(1)

if not test_path.exists():
    print("❌ Error: Test data not found!")
    print(f"   Looking for: {test_path}")
    exit(1)

print(f"\n📂 Loading training data from: {train_path}")
train_df = pd.read_csv(train_path)

print(f"📂 Loading test data from: {test_path}")
test_df = pd.read_csv(test_path)

print(f"\n✅ Training samples: {len(train_df)}")
print(f"✅ Test samples: {len(test_df)}")

# Prepare features and labels
print("\n🔧 Preparing features...")

X_train = train_df.drop(columns=["Activity", "subject"], errors='ignore')
y_train = train_df["Activity"]

X_test = test_df.drop(columns=["Activity", "subject"], errors='ignore')
y_test = test_df["Activity"]

print(f"   Features: {X_train.shape[1]}")
print(f"   Classes: {y_train.nunique()}")
print(f"   Activity types: {', '.join(y_train.unique())}")

# Train model
print("\n🤖 Training Random Forest Classifier...")
print("   This may take a few minutes...")

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=10,
    min_samples_leaf=4,
    random_state=42,
    n_jobs=-1,
    verbose=1
)

model.fit(X_train, y_train)

print("\n✅ Training completed!")

# Evaluate model
print("\n📊 Evaluating model performance...")

y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

train_accuracy = accuracy_score(y_train, y_pred_train)
test_accuracy = accuracy_score(y_test, y_pred_test)

print(f"\n🎯 Training Accuracy: {train_accuracy:.2%}")
print(f"🎯 Test Accuracy: {test_accuracy:.2%}")

print("\n📋 Detailed Classification Report:")
print(classification_report(y_test, y_pred_test))

# Feature importance
print("\n🔝 Top 10 Most Important Features:")
feature_importance = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

for idx, row in feature_importance.head(10).iterrows():
    print(f"   {row['feature']}: {row['importance']:.4f}")

# Save model
model_path = "activity_model.pkl"
print(f"\n💾 Saving model to: {model_path}")

joblib.dump(model, model_path)

print(f"✅ Model saved successfully!")
print(f"   File size: {Path(model_path).stat().st_size / 1024:.2f} KB")

print("\n" + "=" * 60)
print("🎉 Training Complete!")
print("=" * 60)
print("\nYou can now use the Live Simulation mode in the dashboard!")
print("Run: streamlit run app.py")
print("=" * 60)
