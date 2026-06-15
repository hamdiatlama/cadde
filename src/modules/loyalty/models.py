from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base

class LoyaltyTier(Base):
    __tablename__ = "loyalty_tiers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    min_spend = Column(Float, default=0)
    discount_rate = Column(Float, default=0)
    free_shipping = Column(Boolean, default=False)
    badge_color = Column(String(20))

class UserLoyalty(Base):
    __tablename__ = "user_loyalty"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    points = Column(Integer, default=0)
    total_spend = Column(Float, default=0)
    tier_id = Column(Integer, ForeignKey("loyalty_tiers.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LoyaltyPointTransaction(Base):
    __tablename__ = "loyalty_point_transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    reference_type = Column(String(50))
    reference_id = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
