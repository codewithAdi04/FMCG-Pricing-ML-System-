# backend/app/services/feature_service.py
import numpy as np
from datetime import datetime

CURRENT_YEAR = datetime.now().year

class FeatureEngineeringService:
    def transform(self, data) -> list[float]:
        features = []

 
        weight = float(data.weight or 1.0)
        features.append(weight)

        visibility = max(float(data.visibility or 0.01), 1e-6)
        features.append(np.log1p(visibility))

        est_year = int(data.establishment_year or CURRENT_YEAR)
        features.append(max(CURRENT_YEAR - est_year, 0))

        product_type = (data.product_type or "").lower()

        is_snack = 1 if "snack" in product_type else 0
        is_dairy = 1 if "dairy" in product_type else 0
        is_bakery = 1 if "bakery" in product_type else 0
        is_beverage = 1 if "beverage" in product_type else 0

        features.extend([is_snack, is_dairy, is_bakery, is_beverage])

        return features