import os
import joblib
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), "saved_models")
PIPELINE_PATH = os.path.join(MODEL_DIR, "crop_pipeline.joblib")
LABEL_ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.joblib")

class CropModel:
    def __init__(self):
        self.pipeline = None
        self.label_encoder = None
        if os.path.exists(PIPELINE_PATH) and os.path.exists(LABEL_ENCODER_PATH):
            try:
                self.pipeline = joblib.load(PIPELINE_PATH)
                self.label_encoder = joblib.load(LABEL_ENCODER_PATH)
                print("Loaded trained crop pipeline and label encoder.")
            except Exception as e:
                print("Failed to load model:", e)
        else:
            print("Trained model not found. Please run training script: src/models/train_model.py")

    def train(self, X, y):
        """Optional helper if you want to train from code (not required if using train_model.py)"""
        self.pipeline.fit(X, y)

    def predict(self, features_list):
        """
        features_list: list or 1D-array in the order:
        [N, P, K, pH, temperature, humidity, rainfall]
        """
        if self.pipeline is None or self.label_encoder is None:
            raise RuntimeError("Model not loaded. Train the model first by running src/models/train_model.py")

        arr = np.array(features_list, dtype=float).reshape(1, -1)
        encoded = self.pipeline.predict(arr)[0]
        crop = self.label_encoder.inverse_transform([encoded])[0]
        return crop
