from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class PricingRule(Base):
    __tablename__ = "pricing_rules"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    rule_type = Column(String(50))
    min_price = Column(Float)
    max_price = Column(Float)
    target_margin = Column(Float)
    adjustment_rate = Column(Float, default=5)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    old_price = Column(Float)
    new_price = Column(Float)
    reason = Column(String(100))
    changed_at = Column(DateTime(timezone=True), server_default=func.now())


class InventoryForecast(Base):
    __tablename__ = "inventory_forecasts"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    forecast_date = Column(DateTime(timezone=True))
    predicted_demand = Column(Integer, default=0)
    confidence = Column(Float, default=0.8)
    reorder_point = Column(Integer, default=0)
    suggested_order_qty = Column(Integer, default=0)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
