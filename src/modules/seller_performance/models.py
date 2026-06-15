from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class SellerRating(Base):
    __tablename__ = "seller_ratings"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    review = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SellerBadge(Base):
    __tablename__ = "seller_badges"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    badge_type = Column(String(50), nullable=False)
    awarded_at = Column(DateTime(timezone=True), server_default=func.now())


class SellerPerformanceMetric(Base):
    __tablename__ = "seller_performance_metrics"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    period = Column(String(10), nullable=False)
    total_orders = Column(Integer, default=0)
    completed_orders = Column(Integer, default=0)
    cancelled_orders = Column(Integer, default=0)
    late_shipments = Column(Integer, default=0)
    avg_rating = Column(Float, default=0)
    return_rate = Column(Float, default=0)
    on_time_rate = Column(Float, default=100)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())
