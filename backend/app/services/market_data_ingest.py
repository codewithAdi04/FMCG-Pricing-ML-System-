import pandas as pd
from backend.app.db.database import SessionLocal
from backend.app.db.models import MarketPrice


def ingest_flipkart_data(csv_path: str):
    """
    Ingest real Flipkart pricing data into market_prices table
    """
    df = pd.read_csv(csv_path)

    # Basic cleaning
    df = df.dropna(subset=["title", "actprice1", "maincateg"])

    db = SessionLocal()
    inserted = 0

    for _, row in df.iterrows():
        try:
            price = float(row["actprice1"])
        except:
            continue

        market_price = MarketPrice(
            product_name=row["title"][:100],
            category=row["maincateg"],
            weight_grams=0,          
            platform="Flipkart",
            city="India",            
            price=price
        )

        db.add(market_price)
        inserted += 1

    db.commit()
    db.close()

    print(f"Inserted {inserted} Flipkart market prices")


if __name__ == "__main__":
    ingest_flipkart_data("data/raw/flipkart_dataset.csv")