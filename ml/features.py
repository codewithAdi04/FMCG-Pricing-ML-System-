import numpy as np
import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["visibility"] = np.log1p(df["visibility"].clip(0.0001))
    df["outlet_age"] = 2024 - df["establishment_year"]

    df["fat_content"] = df["fat_content"].str.lower().map({
        "low fat": 0,
        "regular": 1
    }).fillna(0)

    df["outlet_size"] = df["outlet_size"].str.lower().map({
        "small": 0,
        "medium": 1,
        "high": 2
    }).fillna(1)

    df["outlet_type"] = df["outlet_type"].str.lower().map({
        "grocery store": 0,
        "supermarket type1": 1,
        "supermarket type2": 2
    }).fillna(1)

    df["location_type"] = df["location_type"].str.lower().map({
        "tier 1": 1,
        "tier 2": 2,
        "tier 3": 3
    }).fillna(2)

    return df[
        [
            "weight",
            "visibility",
            "outlet_age",
            "fat_content",
            "outlet_size",
            "outlet_type",
            "location_type"
        ]
    ]