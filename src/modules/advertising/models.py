from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class AdCampaign(Base):
    __tablename__ = "ad_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(30))
    daily_budget = Column(Float, default=0)
    total_budget = Column(Float, default=0)
    spent = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AdProduct(Base):
    __tablename__ = "ad_products"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    bid_amount = Column(Float, default=0)
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
