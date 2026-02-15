import pandas as pd

def load_and_merge():
    dfs = []

    bigmart = pd.read_csv("data/processed/bigmart_features.csv")

    if "Item_Type" in bigmart.columns:
        bigmart["category"] = bigmart["Item_Type"].str.lower()
    elif "product_type" in bigmart.columns:
        bigmart["category"] = bigmart["product_type"].str.lower()
    else:
        bigmart["category"] = "generic"

    if "Item_MRP" in bigmart.columns:
        bigmart["price"] = bigmart["Item_MRP"]
    elif "MRP" in bigmart.columns:
        bigmart["price"] = bigmart["MRP"]

    if "Item_Weight" in bigmart.columns:
        bigmart["weight"] = bigmart["Item_Weight"]
    else:
        bigmart["weight"] = 1.0

    dfs.append(bigmart)

    ecommerce = pd.read_csv("data/raw/ecommerce_dataset.csv")

    ecommerce = ecommerce.rename(columns={
        "selling_price": "price",
        "product_category": "category",
        "weight_kg": "weight"
    })

    dfs.append(ecommerce)

    grocery = pd.read_csv("data/raw/grocery_chain_data.csv")

    grocery = grocery.rename(columns={
        "mrp": "price",
        "category": "category",
        "weight": "weight"
    })

    dfs.append(grocery)

    df = pd.concat(dfs, ignore_index=True)

    df = df.dropna(subset=["price", "weight", "category"])
    df = df[df["price"] > 1]
    df = df[df["weight"] > 0]

    return df