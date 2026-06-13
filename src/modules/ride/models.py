from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func
from src.database import Base


class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
    current_latitude = Column(Float)
    current_longitude = Column(Float)
    current_speed_kmh = Column(Float, default=0)
    current_heading = Column(Float, default=0)
    current_accuracy_m = Column(Float, default=0)
    last_location_update = Column(DateTime(timezone=True))
    total_rides = Column(Integer, default=0)
    cancelled_rides = Column(Integer, default=0)
    gps_spoofing_score = Column(Float, default=0)
    consecutive_anomalies = Column(Integer, default=0)
    last_anomaly_at = Column(DateTime(timezone=True))
    penalty_until = Column(DateTime(timezone=True))
    rating = Column(Float, default=0)
    total_ratings = Column(Integer, default=0)
    phone_verified = Column(Boolean, default=False)
    license_plate = Column(String)
    vehicle_model = Column(String)
    vehicle_color = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverLocationHistory(Base):
    __tablename__ = "driver_location_history"
    id = Column(Integer, primary_key=True, index=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    ride_id = Column(Integer, ForeignKey("rides.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed_kmh = Column(Float, default=0)
    heading = Column(Float, default=0)
    accuracy_m = Column(Float, default=0)
    source = Column(String, default="gps")
    was_anomaly = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Ride(Base):
    __tablename__ = "rides"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"))
    status = Column(String, default="waiting_for_driver")
    pickup_address = Column(Text, nullable=False)
    pickup_latitude = Column(Float, nullable=False)
    pickup_longitude = Column(Float, nullable=False)
    dropoff_address = Column(Text, nullable=False)
    dropoff_latitude = Column(Float, nullable=False)
    dropoff_longitude = Column(Float, nullable=False)
    estimated_fare = Column(Float, nullable=False)
    actual_fare = Column(Float)
    surge_multiplier = Column(Float, default=1.0)
    payment_method = Column(String, default="card")
    payment_status = Column(String, default="pending")
    optimal_distance_km = Column(Float)
    actual_distance_km = Column(Float)
    route_deviation_km = Column(Float)
    eta_at_booking = Column(Integer)
    actual_wait_seconds = Column(Integer)
    driver_distance_at_accept_km = Column(Float)
    notes = Column(Text)
    accepted_at = Column(DateTime(timezone=True))
    arrived_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    cancel_reason = Column(Text)
    cancelled_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RideSafety(Base):
    __tablename__ = "ride_safety"
    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    driver_plate_confirmed = Column(Boolean, default=False)
    driver_photo_confirmed = Column(Boolean, default=False)
    emergency_contact_notified = Column(Boolean, default=False)
    emergency_contact_phone = Column(String)
    share_link = Column(String)
    incident_reported = Column(Boolean, default=False)
    incident_type = Column(String)
    incident_description = Column(Text)
    reported_at = Column(DateTime(timezone=True))


class RideRating(Base):
    __tablename__ = "ride_ratings"
    id = Column(Integer, primary_key=True, index=True)
    ride_id = Column(Integer, ForeignKey("rides.id"), nullable=False)
    rated_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    categories = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
