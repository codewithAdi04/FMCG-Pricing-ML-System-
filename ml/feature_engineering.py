import pandas as pd
import numpy as np
from pathlib import Path

DATA_PATH = Path("ml/data/master_pricing_dataset.csv")
FEATURE_OUTPUT = Path("ml/data/processed_features.csv")


def build_features():
    df = pd.read_csv(DATA_PATH)

    df = df[df["price"] > 0]
    df["weight"] = df["weight"].fillna(0.5).clip(0.01, 10)
    df["target_price"] = np.log1p(df["price"])
    df["weight_log"] = np.log1p(df["weight"])
    df["visibility"] = df["visibility"].fillna(0.1).clip(0.01, 1)

    CURRENT_YEAR = 2025
    df["outlet_age"] = CURRENT_YEAR - df["establishment_year"]
    df["outlet_age"] = df["outlet_age"].clip(0, 50)

    category_map = {
        "snack": 1,
        "dairy": 2,
        "oil": 3,
        "bakery": 4,
        "beverage": 5,
        "electronics": 6,
        "clothing": 7,
        "footwear": 8,
        "furniture": 9,
        "retail": 10
    }

    brand_map = {
        "generic": 0,
        "mid": 1,
        "premium": 2
    }

    outlet_type_map = {
        "grocery store": 0,
        "supermarket type1": 1,
        "supermarket type2": 2,
        "online": 3
    }

    location_map = {
        "tier 1": 2,
        "tier 2": 1,
        "tier 3": 0
    }

    df["category_encoded"] = df["category"].map(category_map).fillna(0)
    df["brand_encoded"] = df["brand"].map(brand_map).fillna(0)
    df["outlet_type_encoded"] = df["outlet_type"].map(outlet_type_map).fillna(0)
    df["location_encoded"] = df["location_type"].map(location_map).fillna(1)

    
    features = [
        "weight_log",
        "visibility",
        "outlet_age",
        "category_encoded",
        "brand_encoded",
        "outlet_type_encoded",
        "location_encoded"
    ]

    final_df = df[features + ["target_price"]]
    final_df.to_csv(FEATURE_OUTPUT, index=False)

    print(" Feature engineering complete")
    print(" Rows:", len(final_df))


if __name__ == "__main__":
    build_features()
