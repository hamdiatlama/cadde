from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class FulfillmentCenter(Base):
    __tablename__ = "fulfillment_centers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FulfillmentRequest(Base):
    __tablename__ = "fulfillment_requests"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    center_id = Column(Integer, ForeignKey("fulfillment_centers.id"))
    status = Column(String(20), default="pending")
    tracking_no = Column(String(100))
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
