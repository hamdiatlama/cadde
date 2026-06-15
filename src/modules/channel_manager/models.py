from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class OtaChannel(Base):
    __tablename__ = "ota_channels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    connection_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OtaConnection(Base):
    __tablename__ = "ota_connections"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    ota_channel_id = Column(Integer, ForeignKey("ota_channels.id"), nullable=False)
    status = Column(String(20), default="disconnected")
    api_key = Column(String(500))
    api_secret = Column(String(500))
    webhook_url = Column(String(500))
    connected_at = Column(DateTime(timezone=True))
    last_sync_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)


class OtaListing(Base):
    __tablename__ = "ota_listings"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    ota_connection_id = Column(Integer, ForeignKey("ota_connections.id"), nullable=False)
    external_listing_id = Column(String(200))
    external_url = Column(String(500))
    listing_title = Column(String(200))
    status = Column(String(20), default="active")
    last_synced_at = Column(DateTime(timezone=True))
    sync_errors = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class OtaRatePlan(Base):
    __tablename__ = "ota_rate_plans"
    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("ota_listings.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    external_rate_plan_id = Column(String(200))
    name = Column(String(200))
    base_price = Column(Float)
    currency = Column(String(3), default="TRY")
    is_active = Column(Boolean, default=True)


class OtaBooking(Base):
    __tablename__ = "ota_bookings"
    id = Column(Integer, primary_key=True, index=True)
    ota_listing_id = Column(Integer, ForeignKey("ota_listings.id"), nullable=False)
    external_booking_id = Column(String(200), unique=True, nullable=False)
    guest_name = Column(String(200))
    guest_email = Column(String(200))
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    total_price = Column(Float)
    currency = Column(String(3))
    status = Column(String(20))
    booking_data = Column(Text)
    synced_to_pms = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class OtaSyncLog(Base):
    __tablename__ = "ota_sync_logs"
    id = Column(Integer, primary_key=True, index=True)
    connection_id = Column(Integer, ForeignKey("ota_connections.id"), nullable=False)
    sync_type = Column(String(50))
    status = Column(String(20))
    message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    errors_count = Column(Integer, default=0)
