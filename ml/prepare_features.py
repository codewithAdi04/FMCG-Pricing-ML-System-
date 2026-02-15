import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path

CURRENT_YEAR = datetime.now().year

RAW_PATH = Path("data/raw/bigmart_dataset.csv")
OUT_PATH = Path("data/processed/bigmart_features.csv")
OUT_PATH.parent.mkdir(exist_ok=True)

# Encoding maps

fat_content_map = {"low fat": 1, "regular": 0}
outlet_size_map = {"small": 0, "medium": 1, "high": 2}
outlet_type_map = {
    "supermarket type1": 1,
    "supermarket type2": 2,
    "grocery store": 0
}
location_type_map = {"tier 1": 1, "tier 2": 2, "tier 3": 3}

def safe_str(x):
    return str(x).strip().lower()

def pack_bucket(w):
    if w <= 0.25:
        return 0
    elif w <= 0.75:
        return 1
    else:
        return 2

def main():
    df = pd.read_csv(RAW_PATH)


    # Core features

    df["Item_Weight"] = df["Weight"]

    df["Item_Visibility_Log"] = np.log1p(
        df["ProductVisibility"].clip(lower=1e-6)
    )

    df["Outlet_Age"] = CURRENT_YEAR - df["EstablishmentYear"]

    df["Fat_Content_Encoded"] = (
        df["FatContent"].apply(safe_str).map(fat_content_map).fillna(0)
    )

    df["Outlet_Size_Encoded"] = (
        df["OutletSize"].apply(safe_str).map(outlet_size_map).fillna(1)
    )

    df["Outlet_Type_Encoded"] = (
        df["OutletType"].apply(safe_str).map(outlet_type_map).fillna(0)
    )

    df["Location_Type_Encoded"] = (
        df["LocationType"].apply(safe_str).map(location_type_map).fillna(2)
    )

    # --------------------
    # ML RANGE SIGNALS
    # --------------------
    df["Pack_Size_Bucket"] = df["Item_Weight"].apply(pack_bucket)

    # Target = price density
    df["Price_per_kg"] = df["MRP"] / df["Item_Weight"]
    df["Log_Price_per_kg"] = np.log1p(df["Price_per_kg"])

    FINAL_COLS = [
        "Item_Weight",
        "Item_Visibility_Log",
        "Outlet_Age",
        "Fat_Content_Encoded",
        "Outlet_Size_Encoded",
        "Outlet_Type_Encoded",
        "Location_Type_Encoded",
        "Pack_Size_Bucket",
        "Log_Price_per_kg"
    ]

    final_df = df[FINAL_COLS]
    final_df.to_csv(OUT_PATH, index=False)

    print("Feature dataset created")
    print("Shape:", final_df.shape)

if __name__ == "__main__":
    main()