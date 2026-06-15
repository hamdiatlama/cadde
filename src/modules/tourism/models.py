from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, Enum as SAEnum, Date, Time, JSON
from src.database import Base
import enum


class ExperienceCategory(str, enum.Enum):
    BALLOON = "balloon"
    SAFARI = "safari"
    DIVING = "diving"
    MUSEUM = "museum"
    ZOO = "zoo"
    THEME_PARK = "theme_park"
    AQUARIUM = "aquarium"
    CITY_TOUR = "city_tour"
    BOAT_TOUR = "boat_tour"
    NATIONAL_PARK = "national_park"
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    HIKING = "hiking"
    HORSE_RIDING = "horse_riding"
    FISHING = "fishing"
    CAMPING = "camping"
    WORKSHOP = "workshop"
    SPA = "spa"
    COOKING = "cooking"
    WINE_TASTING = "wine_tasting"
    OTHER = "other"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    REFUNDED = "refunded"


class TourismProvider(Base):
    __tablename__ = "tourism_providers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(200), nullable=False)
    tax_id = Column(String(50))
    phone = Column(String(20))
    email = Column(String(200))
    website = Column(String(200))
    address = Column(Text)
    description = Column(Text)
    logo_url = Column(String(500))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TourismExperience(Base):
    __tablename__ = "tourism_experiences"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(Integer, ForeignKey("tourism_providers.id"), nullable=False)
    category = Column(SAEnum(ExperienceCategory), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    short_description = Column(String(500))
    location = Column(String(300))
    city = Column(String(100))
    district = Column(String(100))
    lat = Column(Float)
    lng = Column(Float)
    duration_minutes = Column(Integer)
    min_participants = Column(Integer, default=1)
    max_participants = Column(Integer)
    includes = Column(Text)
    excludes = Column(Text)
    what_to_bring = Column(Text)
    highlights = Column(JSON)
    photos = Column(JSON)
    cover_photo_url = Column(String(500))
    base_price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    cancellation_policy = Column(Text)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TourismSchedule(Base):
    __tablename__ = "tourism_schedules"
    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("tourism_experiences.id"), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    capacity = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False)
    price = Column(Float)
    currency = Column(String(3), default="TRY")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TourismBooking(Base):
    __tablename__ = "tourism_bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_no = Column(String(20), unique=True, nullable=False)
    schedule_id = Column(Integer, ForeignKey("tourism_schedules.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    participant_count = Column(Integer, default=1)
    participant_names = Column(JSON)
    total_price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    status = Column(SAEnum(BookingStatus), default=BookingStatus.PENDING)
    reseller_fee = Column(Float, default=0)
    commission_rate = Column(Float, default=0)
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(20))
    customer_email = Column(String(200))
    notes = Column(Text)
    qr_code = Column(String(500))
    cancellation_reason = Column(Text)
    booked_at = Column(DateTime(timezone=True), server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TourismReview(Base):
    __tablename__ = "tourism_reviews"
    id = Column(Integer, primary_key=True, index=True)
    experience_id = Column(Integer, ForeignKey("tourism_experiences.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("tourism_bookings.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    photos = Column(JSON)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
