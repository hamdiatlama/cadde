from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class FraudRule(Base):
    __tablename__ = "fraud_rules"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    rule_type = Column(String(50))
    threshold_value = Column(Float)
    score = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FraudCheck(Base):
    __tablename__ = "fraud_checks"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    total_score = Column(Integer, default=0)
    risk_level = Column(String(20))
    flags = Column(Text)
    is_blocked = Column(Boolean, default=False)
    checked_at = Column(DateTime(timezone=True), server_default=func.now())


class FraudTransactionHistory(Base):
    __tablename__ = "fraud_transaction_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ip_address = Column(String(50))
    device_fingerprint = Column(String(200))
    amount = Column(Float)
    success = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
