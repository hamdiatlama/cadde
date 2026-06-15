from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class Campaign(Base):
    __tablename__ = "campaigns"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    type = Column(String(30), nullable=False)
    discount_type = Column(String(20))
    discount_value = Column(Float, default=0)
    min_order_amount = Column(Float, default=0)
    max_discount_amount = Column(Float)
    max_uses = Column(Integer)
    current_uses = Column(Integer, default=0)
    per_user_limit = Column(Integer, default=1)
    applicable_categories = Column(String)
    applicable_products = Column(String)
    applicable_sellers = Column(String)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    banner_url = Column(String(500))
    sort_order = Column(Integer, default=0)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CampaignUsage(Base):
    __tablename__ = "campaign_usage"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    discount_amount = Column(Float, default=0)
    used_at = Column(DateTime(timezone=True), server_default=func.now())


class FlashSale(Base):
    __tablename__ = "flash_sales"
    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sale_price = Column(Float, nullable=False)
    quantity_limit = Column(Integer, default=0)
    sold_count = Column(Integer, default=0)
    max_per_user = Column(Integer, default=1)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
