from fastapi import FastAPI
from src.preprocessing.feature_generator import generate_features
from src.models.model import CropModel

app = FastAPI(title="KrishiNex Crop Recommendation API")

# Load trained model
model = CropModel()

@app.get("/")
def home():
    return {
        "message": "KrishiNex API is running!",
        "usage": "/predict?state=Uttar Pradesh&district=Kanpur"
    }

@app.get("/predict")
def predict_crop(state: str, district: str):
    # Generate automatic features (soil + weather)
    features = generate_features(state, district)

    if "error" in features:
        return {"status": "failed", "message": features["error"]}

    # Convert feature dict → list in correct order
    ordered = [
        features["N"],
        features["P"],
        features["K"],
        features["pH"],
        features["temperature"],
        features["humidity"],
        features["rainfall"],
    ]

    # Get model prediction
    crop = model.predict(ordered)

    return {
        "status": "success",
        "location": {
            "state": state,
            "district": district
        },
        "recommended_crop": crop,
        "features_used": features
    }
