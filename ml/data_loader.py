import pandas as pd
from pathlib import Path

RAW_DIR = Path("ml/data/raw")
OUTPUT_FILE = Path("ml/data/master_pricing_dataset.csv")


def safe_lower(x):
    if pd.isna(x):
        return "unknown"
    return str(x).strip().lower()


def safe_float(x, default=0.0):
    try:
        return float(x)
    except:
        return default


def load_bigmart():
    df = pd.read_csv(RAW_DIR / "bigmart_dataset.csv")

    return pd.DataFrame({
        "product_name": df["Item_Identifier"],
        "category": df["Item_Type"].apply(safe_lower),
        "brand": "generic",
        "weight": df["Item_Weight"].apply(safe_float),
        "price": df["Item_MRP"].apply(safe_float),
        "outlet_type": df["Outlet_Type"].apply(safe_lower),
        "outlet_size": df["Outlet_Size"].apply(safe_lower),
        "location_type": df["Outlet_Location_Type"].apply(safe_lower),
        "visibility": df["Item_Visibility"].apply(safe_float),
        "establishment_year": df["Outlet_Establishment_Year"],
        "source": "bigmart"
    })


def load_flipkart():
    df = pd.read_csv(RAW_DIR / "flipkart_dataset.csv")

    return pd.DataFrame({
        "product_name": df["product_name"],
        "category": df["category"].apply(safe_lower),
        "brand": df["brand"].apply(safe_lower),
        "weight": df.get("weight", 0.5),
        "price": df["selling_price"].apply(safe_float),
        "outlet_type": "online",
        "outlet_size": "na",
        "location_type": "tier 1",
        "visibility": 0.1,
        "establishment_year": 2020,
        "source": "flipkart"
    })

def load_ecommerce():
    df = pd.read_csv(RAW_DIR / "ecommerce_dataset.csv")

    return pd.DataFrame({
        "product_name": df["Product Name"],
        "category": df["Category"].apply(safe_lower),
        "brand": df["Brand"].apply(safe_lower),
        "weight": df.get("Weight", 0.5),
        "price": df["Price"].apply(safe_float),
        "outlet_type": "online",
        "outlet_size": "na",
        "location_type": "tier 1",
        "visibility": 0.12,
        "establishment_year": 2019,
        "source": "ecommerce"
    })

def load_grocery_chain():
    df = pd.read_csv(RAW_DIR / "grocery_chain_data.csv")

    return pd.DataFrame({
        "product_name": df["product"],
        "category": df["category"].apply(safe_lower),
        "brand": df.get("brand", "generic").apply(safe_lower),
        "weight": df["weight"].apply(safe_float),
        "price": df["mrp"].apply(safe_float),
        "outlet_type": "grocery store",
        "outlet_size": "small",
        "location_type": df.get("location", "tier 2"),
        "visibility": 0.08,
        "establishment_year": 2015,
        "source": "grocery_chain"
    })

def load_online_retail():
    df = pd.read_csv(RAW_DIR / "Online_Retail.csv")

    df["price"] = df["UnitPrice"] * df["Quantity"]

    return pd.DataFrame({
        "product_name": df["Description"],
        "category": "retail",
        "brand": "generic",
        "weight": 0.5,
        "price": df["price"].apply(safe_float),
        "outlet_type": "online",
        "outlet_size": "na",
        "location_type": "tier 1",
        "visibility": 0.15,
        "establishment_year": 2018,
        "source": "online_retail"
    })

def main():
    print("🚀 Loading datasets...")

    frames = [
        load_bigmart(),
        load_flipkart(),
        load_ecommerce(),
        load_grocery_chain(),
        load_online_retail()
    ]

    df = pd.concat(frames, ignore_index=True)

    df = df[df["price"] > 0]

    
    df["category"] = df["category"].replace({
        "snacks": "snack",
        "biscuits": "snack",
        "chips": "snack",
        "milk": "dairy",
        "oil & fats": "oil",
        "electronics accessories": "electronics"
    })

    df.to_csv(OUTPUT_FILE, index=False)
    print(f" Master dataset created: {OUTPUT_FILE}")
    print(f" Total rows: {len(df)}")


if __name__ == "__main__":
    main()