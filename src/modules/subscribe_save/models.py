from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_save_plans"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    interval_days = Column(Integer, nullable=False)
    discount_rate = Column(Float, default=5)
    max_orders = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SubscriptionSaveOrder(Base):
    __tablename__ = "subscription_save_orders"
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("subscription_save_plans.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    next_order_date = Column(DateTime(timezone=True))
    total_orders = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
