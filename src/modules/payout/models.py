from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class PayoutBatch(Base):
    __tablename__ = "payout_batches"
    id = Column(Integer, primary_key=True, index=True)
    batch_no = Column(String(50), unique=True, nullable=False)
    total_amount = Column(Float, default=0)
    total_sellers = Column(Integer, default=0)
    status = Column(String(30), default="pending")
    notes = Column(Text)
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Payout(Base):
    __tablename__ = "payouts"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    batch_id = Column(Integer, ForeignKey("payout_batches.id"))
    amount = Column(Float, nullable=False)
    platform_fee = Column(Float, default=0)
    net_amount = Column(Float, nullable=False)
    status = Column(String(30), default="pending")
    payment_method = Column(String(50))
    payment_ref = Column(String(255))
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    paid_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
