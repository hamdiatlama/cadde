from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class CustomOrder(Base):
    __tablename__ = "custom_orders"
    id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    description = Column(String(1000))
    requirements = Column(String(2000))
    status = Column(String(20), default="pending")
    price = Column(Float)
    estimated_days = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
