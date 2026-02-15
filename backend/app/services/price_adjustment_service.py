class PriceAdjustmentService:
    """
    INDUSTRIAL PRICE ADJUSTMENT ENGINE
    ML + Market + Cost + FMCG rules
    """

    CATEGORY_RULES = {
        "snack": {"min": 10, "max": 50},
        "dairy": {"min": 40, "max": 80},
        "oil": {"min": 100, "max": 300},
        "bakery": {"min": 20, "max": 150},
        "beverage": {"min": 20, "max": 200},
        "generic": {"min": 10, "max": 5000}
    }

    BRAND_MULTIPLIER = {
        "generic": 1.0,
        "mid": 1.08,
        "premium": 1.25
    }

    def adjust(
        self,
        ml_price: float,
        category: str,
        brand: str,
        weight: float,
        market_price: float | None = None,
        cost_price: float | None = None
    ) -> float:

        category = (category or "generic").lower()
        brand = (brand or "generic").lower()

        rules = self.CATEGORY_RULES.get(category, self.CATEGORY_RULES["generic"])

 
        price = ml_price
        if market_price:
            price = 0.65 * ml_price + 0.35 * market_price

        if category == "snack" and weight <= 0.1:
            price *= 0.75

  
        price *= self.BRAND_MULTIPLIER.get(brand, 1.0)

        if cost_price:
            price = max(price, cost_price * 1.10)

  
        if price < rules["min"]:
            price = rules["min"]
        elif price > rules["max"]:
            price = rules["max"] * 0.98

        return round(price, 2)