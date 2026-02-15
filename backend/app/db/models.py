from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from backend.app.db.database import Base


class PredictionLog(Base):
    __tablename__ = "prediction_logs"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    predicted_price = Column(Float, nullable=False)
    confidence = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False)

    weight_grams = Column(Integer, nullable=False)
    platform = Column(String, nullable=False)
    city = Column(String, nullable=False)

    price = Column(Float, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)