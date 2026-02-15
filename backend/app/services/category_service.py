class CategoryService:
    """
    Detects high-level product category
    """

    CATEGORY_KEYWORDS = {
        "food": [
            "milk", "biscuit", "chips", "oil", "snack",
            "bread", "chocolate", "rice", "atta"
        ],
        "electronics": [
            "mobile", "laptop", "tv", "earphone",
            "headphone", "charger"
        ],
        "clothing": [
            "tshirt", "shirt", "jeans", "kurti",
            "jacket", "sweater"
        ],
        "footwear": [
            "shoes", "slippers", "chapal", "sandals"
        ],
        "furniture": [
            "chair", "table", "sofa", "bed", "almirah"
        ]
    }

    @classmethod
    def detect(cls, product_name: str, product_type: str) -> str:
        text = f"{product_name} {product_type}".lower()

        for category, keywords in cls.CATEGORY_KEYWORDS.items():
            for word in keywords:
                if word in text:
                    return category

        return "food"  