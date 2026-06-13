from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class Courier(Base):
    __tablename__ = "couriers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="offline")
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    current_speed_kmh = Column(Float, default=0)
    current_heading = Column(Float, default=0)
    current_accuracy_m = Column(Float, default=0)
    last_location_update = Column(DateTime(timezone=True))
    gps_spoofing_score = Column(Float, default=0)
    consecutive_anomalies = Column(Integer, default=0)
    last_anomaly_at = Column(DateTime(timezone=True))
    total_deliveries = Column(Integer, default=0)
    total_distance_km = Column(Float, default=0)
    rating = Column(Float, default=0)
    total_ratings = Column(Integer, default=0)
    vehicle_type = Column(String, default="motorcycle")
    vehicle_plate = Column(String)
    max_load_kg = Column(Float, default=50)
    service_zone = Column(String)
    max_delivery_radius_km = Column(Float, default=10)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class CourierEarning(Base):
    __tablename__ = "courier_earnings"
    id = Column(Integer, primary_key=True, index=True)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    delivery_fee_earned = Column(Float, default=0)
    tip_amount = Column(Float, default=0)
    bonus_amount = Column(Float, default=0)
    platform_commission = Column(Float, default=0)
    net_amount = Column(Float, default=0)
    status = Column(String, default="pending")
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourierShift(Base):
    __tablename__ = "courier_shifts"
    id = Column(Integer, primary_key=True, index=True)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    status = Column(String, default="active")
    orders_completed = Column(Integer, default=0)
    total_earned = Column(Float, default=0)
    total_distance_km = Column(Float, default=0)
    started_latitude = Column(Float)
    started_longitude = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CourierLocationHistory(Base):
    __tablename__ = "courier_location_history"
    id = Column(Integer, primary_key=True, index=True)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed_kmh = Column(Float, default=0)
    heading = Column(Float, default=0)
    accuracy_m = Column(Float, default=0)
    source = Column(String, default="gps")
    was_anomaly = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
