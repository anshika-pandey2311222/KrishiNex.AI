import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_PATH = os.path.join(ROOT, "data", "crop_training.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
os.makedirs(MODEL_DIR, exist_ok=True)

# 1) Load data
df = pd.read_csv(DATA_PATH)
feature_cols = ["N", "P", "K", "pH", "temperature", "humidity", "rainfall"]
X = df[feature_cols].values
y_raw = df["crop"].values

# 2) Encode labels
le = LabelEncoder()
y = le.fit_transform(y_raw)

# 3) Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42, stratify=y)

# 4) Pipeline: scaler + RF
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("rf", RandomForestClassifier(n_estimators=150, random_state=42))
])

pipeline.fit(X_train, y_train)

# 5) Evaluate
y_pred_train = pipeline.predict(X_train)
y_pred_test = pipeline.predict(X_test)
print("Train accuracy:", accuracy_score(y_train, y_pred_train))
print("Test accuracy:", accuracy_score(y_test, y_pred_test))
print("\nClassification report (test):\n", classification_report(y_test, y_pred_test, target_names=le.classes_))

# 6) Save model pipeline + label encoder
model_path = os.path.join(MODEL_DIR, "crop_pipeline.joblib")
le_path = os.path.join(MODEL_DIR, "label_encoder.joblib")

joblib.dump(pipeline, model_path)
joblib.dump(le, le_path)

print(f"Saved pipeline to: {model_path}")
print(f"Saved label encoder to: {le_path}")
