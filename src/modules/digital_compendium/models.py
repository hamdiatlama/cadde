from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, JSON, func
from src.database import Base
from datetime import datetime, timezone


class DigitalCompendium(Base):
    __tablename__ = "digital_compendiums"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), unique=True, nullable=False)
    welcome_message = Column(Text)
    wifi_ssid = Column(String(100))
    wifi_password = Column(String(100))
    breakfast_info = Column(Text, comment="saat, yer, menü")
    restaurant_info = Column(Text)
    room_service_info = Column(Text)
    spa_info = Column(Text)
    gym_info = Column(Text)
    parking_info = Column(Text)
    house_rules = Column(Text)
    emergency_info = Column(Text, comment="acil numaralar")
    checkout_info = Column(Text)
    local_attractions = Column(JSON, comment="yakın yerler")
    hotel_services = Column(JSON, comment="tüm hizmetler")
    contact_info = Column(Text, comment="resepsiyon numarası")
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class CompendiumPage(Base):
    __tablename__ = "compendium_pages"

    id = Column(Integer, primary_key=True, index=True)
    compendium_id = Column(Integer, ForeignKey("digital_compendiums.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GuestNotification(Base):
    __tablename__ = "guest_notifications"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_number = Column(String(20))
    notification_type = Column(String(50), comment="welcome, housekeeping, maintenance, event, promo, checkout_reminder")
    title = Column(String(200), nullable=False)
    message = Column(Text)
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RoomServiceRequest(Base):
    __tablename__ = "room_service_requests"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_number = Column(String(20))
    category = Column(String(50), comment="food, cleaning, maintenance, amenities, other")
    item_name = Column(String(200), nullable=False)
    quantity = Column(Integer, default=1)
    notes = Column(Text)
    status = Column(String(20), default="pending", comment="pending, in_progress, completed, cancelled")
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
