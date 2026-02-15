import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(exist_ok=True)


def load_bigmart():
    return pd.read_csv(DATA_DIR / "bigmart_dataset.csv")


def preprocess_bigmart(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Handle missing values
    df["Weight"] = df["Weight"].fillna(df["Weight"].median())
    df["OutletSize"] = df["OutletSize"].fillna(df["OutletSize"].mode()[0])

   
    # Clean FatContent inconsistencies
    df["FatContent"] = df["FatContent"].replace({
        "low fat": "Low Fat",
        "LF": "Low Fat",
        "reg": "Regular"
    })

    # Encode categorical variables
    categorical_cols = [
        "FatContent",
        "ProductType",
        "OutletSize",
        "LocationType",
        "OutletType"
    ]

    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    return df


def save_processed_data(df: pd.DataFrame):
    output_path = PROCESSED_DIR / "bigmart_processed.csv"
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")


if __name__ == "__main__":
    df = load_bigmart()
    processed_df = preprocess_bigmart(df)
    save_processed_data(processed_df)

    print("Final shape:", processed_df.shape)