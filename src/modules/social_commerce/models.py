from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class SocialChannel(Base):
    __tablename__ = "social_channels"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(50), nullable=False)
    access_token = Column(Text)
    refresh_token = Column(Text)
    token_expires_at = Column(DateTime(timezone=True))
    page_id = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SocialProductSync(Base):
    __tablename__ = "social_product_syncs"
    id = Column(Integer, primary_key=True, index=True)
    channel_id = Column(Integer, ForeignKey("social_channels.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    platform_product_id = Column(String(200))
    status = Column(String(20), default="pending")
    last_synced_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SocialOrder(Base):
    __tablename__ = "social_orders"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False)
    platform_order_id = Column(String(200))
    order_id = Column(Integer, ForeignKey("orders.id"))
    buyer_name = Column(String(200))
    buyer_platform_id = Column(String(200))
    total = Column(Float)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ShoppingFeed(Base):
    __tablename__ = "shopping_feeds"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    feed_type = Column(String(50))
    feed_url = Column(String(500))
    product_count = Column(Integer, default=0)
    last_generated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AffiliateNetwork(Base):
    __tablename__ = "affiliate_networks"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    api_key = Column(String(500))
    api_url = Column(String(500))
    is_active = Column(Boolean, default=True)
