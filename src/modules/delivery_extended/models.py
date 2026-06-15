from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class DeliverySlot(Base):
    __tablename__ = "delivery_slots"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(String(10), nullable=False)
    start_time = Column(String(5), nullable=False)
    end_time = Column(String(5), nullable=False)
    max_orders = Column(Integer, default=10)
    current_orders = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class ExpressDelivery(Base):
    __tablename__ = "express_deliveries"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"))
    estimated_minutes = Column(Integer)
    fee = Column(Float)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PickupPoint(Base):
    __tablename__ = "pickup_points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    address = Column(String(500))
    city = Column(String(100))
    lat = Column(Float)
    lng = Column(Float)
    is_active = Column(Boolean, default=True)


class InternationalShipment(Base):
    __tablename__ = "international_shipments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    origin_country = Column(String(2), nullable=False)
    destination_country = Column(String(2), nullable=False)
    customs_value = Column(Float)
    customs_tax = Column(Float)
    shipping_cost = Column(Float)
    tracking_no = Column(String(100))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
