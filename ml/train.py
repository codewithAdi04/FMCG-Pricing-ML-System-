# ml/train.py
import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

MODEL_PATH = "models/pricing_model.pkl"

def main():
    print("🔹 Loading dataset...")
    df = pd.read_csv("data/raw/bigmart.csv")

 
    df = df.dropna(subset=["Item_MRP"])
    df["Item_Weight"] = df["Item_Weight"].fillna(df["Item_Weight"].median())
    df["Item_Visibility"] = df["Item_Visibility"].replace(0, df["Item_Visibility"].median())


    df["product_type"] = df["Item_Type"].str.lower()

    df["is_fmcg"] = df["product_type"].isin(
        ["snack foods", "dairy", "breads", "breakfast", "soft drinks", "frozen foods"]
    ).astype(int)

  
    df["visibility_log"] = np.log1p(df["Item_Visibility"])
    df["outlet_age"] = 2024 - df["Outlet_Establishment_Year"]

    FEATURES = [
        "Item_Weight",
        "visibility_log",
        "outlet_age",
        "is_fmcg"
    ]

    X = df[FEATURES]

    y = np.log1p(df["Item_MRP"] / (df["is_fmcg"] * 0.7 + 1))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=400,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42
    )

    print("🔹 Training model...")
    model.fit(X_train, y_train)

    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model saved at {MODEL_PATH}")

if __name__ == "__main__":
    main()