from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class Carrier(Base):
    __tablename__ = "carriers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    api_url = Column(String(500))
    api_key = Column(String(500))
    services = Column(String(500))
    is_active = Column(Boolean, default=True)

class CarrierRate(Base):
    __tablename__ = "carrier_rates"
    id = Column(Integer, primary_key=True, index=True)
    carrier_id = Column(Integer, ForeignKey("carriers.id"), nullable=False)
    service_name = Column(String(100))
    weight_min = Column(Float, default=0)
    weight_max = Column(Float)
    price = Column(Float, nullable=False)
    estimated_days_min = Column(Integer)
    estimated_days_max = Column(Integer)

class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    carrier_id = Column(Integer, ForeignKey("carriers.id"))
    service_name = Column(String(100))
    tracking_no = Column(String(100))
    label_url = Column(String(500))
    cost = Column(Float)
    weight = Column(Float)
    status = Column(String(20), default="pending")
    shipped_at = Column(DateTime(timezone=True))
    estimated_delivery = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CarbonFootprint(Base):
    __tablename__ = "carbon_footprints"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    co2_grams = Column(Float)
    offset_cost = Column(Float)
    offset_paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GiftWrap(Base):
    __tablename__ = "gift_wraps"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100))
    price = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
