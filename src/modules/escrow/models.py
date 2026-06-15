from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class EscrowTransaction(Base):
    __tablename__ = "escrow_transactions"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    platform_fee = Column(Float, default=0)
    seller_amount = Column(Float, default=0)
    status = Column(String(30), default="held")
    release_trigger = Column(String(50))
    release_at = Column(DateTime(timezone=True))
    released_at = Column(DateTime(timezone=True))
    released_by = Column(String(50))
    dispute_id = Column(Integer, ForeignKey("disputes.id"))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Dispute(Base):
    __tablename__ = "disputes"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    raised_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    raised_against = Column(String(20))
    reason = Column(String(255), nullable=False)
    description = Column(Text)
    evidence = Column(String)
    status = Column(String(30), default="open")
    resolution = Column(String(255))
    resolved_by = Column(Integer, ForeignKey("users.id"))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
