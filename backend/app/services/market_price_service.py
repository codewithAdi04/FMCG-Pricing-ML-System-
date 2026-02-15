from sqlalchemy.orm import Session
from backend.app.db.models import MarketPrice

class MarketPriceService:
    def __init__(self, db: Session):
        self.db = db

    def get_market_price(self, category: str) -> float | None:
        category = category.lower()

        rows = (
            self.db.query(MarketPrice)
            .filter(MarketPrice.category == category)
            .all()
        )

        if not rows:
            return None

        prices = [r.price for r in rows if r.price > 0]
        if not prices:
            return None

        prices.sort()
        mid = len(prices) // 2
        return round(prices[mid], 2)