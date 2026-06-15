from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class TradeInRequest(Base):
    __tablename__ = "trade_in_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_to_trade = Column(String(200))
    estimated_value = Column(Float)
    condition = Column(String(50))
    target_product_id = Column(Integer, ForeignKey("products.id"))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RefurbishedProduct(Base):
    __tablename__ = "refurbished_products"
    id = Column(Integer, primary_key=True, index=True)
    original_product_id = Column(Integer, ForeignKey("products.id"))
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    condition_grade = Column(String(20))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
