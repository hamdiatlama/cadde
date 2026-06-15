from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base

class CommissionRule(Base):
    __tablename__ = "commission_rules"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    rate = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CommissionTransaction(Base):
    __tablename__ = "commission_transactions"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
