from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base

class PayoutSchedule(Base):
    __tablename__ = "payout_schedules"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    frequency = Column(String(20))
    day_of_week = Column(Integer)
    day_of_month = Column(Integer)
    min_amount = Column(Float, default=50)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MultiCurrencyBalance(Base):
    __tablename__ = "multi_currency_balances"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String(10), nullable=False)
    balance = Column(Float, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())
