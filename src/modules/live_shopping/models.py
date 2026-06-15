from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class LiveStream(Base):
    __tablename__ = "live_streams"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    stream_url = Column(String(500))
    thumbnail_url = Column(String(500))
    status = Column(String(20), default="scheduled")
    viewer_count = Column(Integer, default=0)
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    ended_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LiveStreamProduct(Base):
    __tablename__ = "live_stream_products"
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("live_streams.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    discount_rate = Column(Float, default=0)
    sort_order = Column(Integer, default=0)


class LiveStreamOrder(Base):
    __tablename__ = "live_stream_orders"
    id = Column(Integer, primary_key=True, index=True)
    stream_id = Column(Integer, ForeignKey("live_streams.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
