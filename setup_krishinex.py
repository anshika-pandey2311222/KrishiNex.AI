import os

project_name = "KrishiNex"

folders = [
    "data",
    "notebooks",
    "src",
    "src/preprocessing",
    "src/models",
    "src/utils",
    "app"
]

files_with_content = {
    "README.md": "# KrishiNex\nA location-based crop recommendation system.\n",

    "src/__init__.py": "",
    
    "src/preprocessing/__init__.py": "",
    "src/preprocessing/data_loader.py": """# Loads soil, weather, and location data

def load_soil_data():
    # TODO: implement soil dataset import
    return None

def load_weather_data():
    # TODO: implement weather dataset import
    return None
""",

    "src/preprocessing/feature_generator.py": """# Generates automatic features (N, P, K, pH, rainfall, temperature)

def generate_features(state, district):
    # TODO: fetch soil + weather features automatically
    features = {
        \"N\": None,
        \"P\": None,
        \"K\": None,
        \"pH\": None,
        \"rainfall\": None,
        \"temperature\": None
    }
    return features
""",

    "src/models/__init__.py": "",
    "src/models/model.py": """# ML model training & prediction

from sklearn.ensemble import RandomForestClassifier

class CropModel:
    def __init__(self):
        self.model = RandomForestClassifier()

    def train(self, X, y):
        self.model.fit(X, y)

    def predict(self, features):
        return self.model.predict([features])[0]
""",

    "src/utils/__init__.py": "",
    "src/utils/helpers.py": """# Utility functions here

def normalize(value):
    # TODO: add proper scaling
    return value
""",

    "app/__init__.py": "",
    "app/main.py": """# FastAPI backend for KrishiNex

from fastapi import FastAPI
from src.preprocessing.feature_generator import generate_features
from src.models.model import CropModel

app = FastAPI()
model = CropModel()  # Load trained model later

@app.get("/")
def home():
    return {"message": "KrishiNex API Running"}

@app.get("/predict")
def predict_crop(state: str, district: str):
    features = generate_features(state, district)

    # Convert dict → list for model
    ordered_features = [
        features['N'],
        features['P'],
        features['K'],
        features['pH'],
        features['rainfall'],
        features['temperature']
    ]

    prediction = model.predict(ordered_features)
    return {
        "state": state,
        "district": district,
        "predicted_crop": prediction
    }
"""
}

# ---- Create folders ----
os.makedirs(project_name, exist_ok=True)
for folder in folders:
    os.makedirs(os.path.join(project_name, folder), exist_ok=True)

# ---- Create files with content ----
for filepath, content in files_with_content.items():
    full_path = os.path.join(project_name, filepath)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("KrishiNex project created successfully with starter code!")
