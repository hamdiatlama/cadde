from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class SubscriptionPlan(Base):
    __tablename__ = "subscription_plans"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    interval_days = Column(Integer, nullable=False)
    duration_months = Column(Integer, default=1)
    price_per_delivery = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    status = Column(String, default="active")
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    next_delivery_date = Column(DateTime(timezone=True))
    recipient_name = Column(String)
    recipient_phone = Column(String)
    delivery_address = Column(Text)
    delivery_latitude = Column(Float)
    delivery_longitude = Column(Float)
    notes = Column(Text)
    card_message = Column(Text)
    is_gift = Column(Boolean, default=False)
    paused_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    cancel_reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SubscriptionDelivery(Base):
    __tablename__ = "subscription_deliveries"
    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    delivery_number = Column(Integer, nullable=False)
    scheduled_date = Column(DateTime(timezone=True))
    status = Column(String, default="pending")
    is_gift = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
