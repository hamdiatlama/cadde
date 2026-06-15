from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Time, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from src.database import Base


class DigitalKey(Base):
    __tablename__ = "digital_keys"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    room_number = Column(String(20), nullable=True)
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_code = Column(String(100), unique=True, nullable=False)
    qr_code = Column(String(500), nullable=True)
    status = Column(String(20), default="active")
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    issued_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    used_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    booking = relationship("Booking", backref="digital_keys")
    hotel = relationship("Hotel", backref="digital_keys")
    room_type = relationship("RoomType", backref="digital_keys")
    guest = relationship("User", backref="digital_keys")


class MobileCheckin(Base):
    __tablename__ = "mobile_checkins"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), unique=True, nullable=False)
    guest_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    checkin_data = Column(JSON, nullable=True)
    id_verified = Column(Boolean, default=False)
    status = Column(String(20), default="pending")
    verified_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    checked_in_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    booking = relationship("Booking", backref="mobile_checkins")
    guest = relationship("User", foreign_keys=[guest_id], backref="checkins")
    hotel = relationship("Hotel", backref="mobile_checkins")
    verified_by_user = relationship("User", foreign_keys=[verified_by], backref="verified_checkins")


class EarlyCheckinRequest(Base):
    __tablename__ = "early_checkin_requests"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    requested_time = Column(Time, nullable=False)
    is_approved = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    booking = relationship("Booking", backref="early_checkin_requests")
    approved_by_user = relationship("User", foreign_keys=[approved_by], backref="approved_early_checkins")


class LateCheckoutRequest(Base):
    __tablename__ = "late_checkout_requests"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    requested_time = Column(Time, nullable=False)
    is_approved = Column(Boolean, default=False)
    additional_fee = Column(Float, default=0.0)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    booking = relationship("Booking", backref="late_checkout_requests")
    approved_by_user = relationship("User", foreign_keys=[approved_by], backref="approved_late_checkouts")
