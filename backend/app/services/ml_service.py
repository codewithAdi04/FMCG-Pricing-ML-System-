import joblib
import numpy as np
from pathlib import Path

MODEL_PATH = Path("models/pricing_xgb.pkl")
SCALER_PATH = Path("models/scaler.pkl")

class PricingModelService:
    """
    ML PRICE ENGINE
    - Safe prediction
    - Handles bad model outputs
    """

    def __init__(self):
        if MODEL_PATH.exists():
            self.model = joblib.load(MODEL_PATH)
        else:
            self.model = None

        if SCALER_PATH.exists():
            self.scaler = joblib.load(SCALER_PATH)
        else:
            self.scaler = None

    def predict(self, features: np.ndarray) -> float:
        """
        Returns RAW ML price (before rules)
        """

        #  fallback if model missing
        if self.model is None:
            return float(np.mean(features) * 10)

        # scale if scaler exists
        if self.scaler is not None:
            features = self.scaler.transform([features])
        else:
            features = [features]

        price = float(self.model.predict(features)[0])

        # Safety guard
        if price <= 0 or price > 5000:
            price = max(10.0, min(price, 5000.0))

        return round(price, 2)