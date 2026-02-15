class CostPricingService:
    """
    INDUSTRIAL PRICE ENGINE (FINAL FIXED)
    """

    CATEGORY_RULES = {
        "snack": (5, 40),
        "dairy": (40, 70),
        "oil": (90, 300),
        "bakery": (20, 120),
        "electronics": (500, 50000),
        "clothing": (299, 6000),
        "footwear": (399, 8000),
        "furniture": (800, 80000),
        "generic": (10, 10000),
    }

    BRAND_MULTIPLIER = {
        "generic": 1.0,
        "mid": 1.05,
        "premium": 1.25,
    }

    def adjust(
        self,
        ml_price: float,
        market_price: float | None,
        cost_price: float | None,
        category: str,
        brand: str,
        weight: float,
    ) -> float:

        category = category.lower()
        brand = brand.lower()

      
        if market_price:
            price = 0.55 * market_price + 0.45 * ml_price
        else:
            price = ml_price


        if category == "electronics" and market_price:
            price = market_price

      
        low, high = self.CATEGORY_RULES.get(
            category, self.CATEGORY_RULES["generic"]
        )
        price = max(low, min(price, high))

        if category == "snack" and weight < 0.2:
            price = min(price, 30)

     
        multiplier = self.BRAND_MULTIPLIER.get(brand, 1.0)
        price = price * multiplier

        if cost_price:
            price = max(price, cost_price * 1.15)

        return round(price, 2)