from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float, ForeignKey, Numeric, func
from src.database import Base


class Venue(Base):
    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    district = Column(String(100))
    address = Column(Text)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    capacity = Column(Integer, default=0)
    phone = Column(String(20))
    venue_type = Column(String(20), default="kapali")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class VenueSection(Base):
    __tablename__ = "venue_sections"
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, default=0)
    price_multiplier = Column(Numeric(4, 2), default=1.00)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(300), nullable=False)
    category = Column(String(30), nullable=False)
    venue_id = Column(Integer, ForeignKey("venues.id"), nullable=False)
    description = Column(Text)
    poster_url = Column(Text)
    min_age = Column(Integer, default=0)
    organizer = Column(String(200))
    status = Column(String(20), default="published")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))


class EventSession(Base):
    __tablename__ = "event_sessions"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    women_only = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SessionPricing(Base):
    __tablename__ = "session_pricing"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("event_sessions.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("venue_sections.id"), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="TRY")


class Seat(Base):
    __tablename__ = "seats"
    id = Column(Integer, primary_key=True, index=True)
    section_id = Column(Integer, ForeignKey("venue_sections.id"), nullable=False)
    row_label = Column(String(10))
    seat_number = Column(Integer)
    is_active = Column(Boolean, default=True)


class TicketBooking(Base):
    __tablename__ = "ticket_bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("event_sessions.id"), nullable=False)
    status = Column(String(20), default="pending")
    total_amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="TRY")
    paid_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("ticket_bookings.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("event_sessions.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("venue_sections.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"))
    seat_label = Column(String(20))
    price = Column(Numeric(10, 2), nullable=False)
    barcode = Column(String(100), unique=True)
    status = Column(String(20), default="active")
    used_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
