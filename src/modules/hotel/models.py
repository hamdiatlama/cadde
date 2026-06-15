from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text, Enum as SAEnum
from src.database import Base
import enum


class PropertyType(str, enum.Enum):
    HOTEL = "hotel"
    PANSİYON = "pansiyon"
    TATIL_KÖYÜ = "tatil_köyü"
    VILLA = "villa"
    YAZLIK = "yazlik"
    BUNGALOV = "bungalov"
    TINY_HOUSE = "tiny_house"
    DAG_EVI = "dag_evi"
    APART_OTEL = "apart_otel"
    ODA_KIRALAMA = "oda_kiralama"
    KÖY_EVI = "köy_evi"


class ListingType(str, enum.Enum):
    ENTIRE_PLACE = "entire_place"
    PRIVATE_ROOM = "private_room"
    SHARED_ROOM = "shared_room"
    HOTEL_ROOM = "hotel_room"


class PhotoCategory(str, enum.Enum):
    EXTERIOR = "exterior"
    INTERIOR = "interior"
    RECEPTION = "reception"
    LOBBY = "lobby"
    ROOM = "room"
    BATHROOM = "bathroom"
    POOL = "pool"
    GARDEN = "garden"
    RESTAURANT = "restaurant"
    KITCHEN = "kitchen"
    SPA = "spa"
    GYM = "gym"
    PARKING = "parking"
    VIEW = "view"
    OTHER = "other"


class HotelStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CHECKED_IN = "checked_in"
    CHECKED_OUT = "checked_out"
    CANCELLED = "cancelled"


class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    property_type = Column(SAEnum(PropertyType), default=PropertyType.HOTEL)
    listing_type = Column(SAEnum(ListingType), default=ListingType.ENTIRE_PLACE)
    star_rating = Column(Integer, default=3)
    address = Column(String(500))
    city = Column(String(100), nullable=False)
    country = Column(String(100), default="Türkiye")
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String(20))
    email = Column(String(200))
    website = Column(String(200))
    tax_id = Column(String(50))
    company_name = Column(String(200))
    company_description = Column(Text)
    check_in_time = Column(String(5), default="14:00")
    check_out_time = Column(String(5), default="12:00")
    house_rules = Column(Text)
    cancellation_policy = Column(String(500))
    status = Column(SAEnum(HotelStatus), default=HotelStatus.ACTIVE)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    suspended_until = Column(DateTime(timezone=True))
    suspension_reason = Column(Text)
    original_location_id = Column(Integer, ForeignKey("hotels.id"))
    requires_location_approval = Column(Boolean, default=False)
    location_approved_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ServiceCategory(Base):
    __tablename__ = "service_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(50))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)


class PropertyService(Base):
    __tablename__ = "property_services"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("service_categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    icon = Column(String(50))
    description = Column(String(200))
    is_free = Column(Boolean, default=True)
    price = Column(Float)
    is_active = Column(Boolean, default=True)


class HotelAmenity(Base):
    __tablename__ = "hotel_amenities"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(100), nullable=False)
    icon = Column(String(50))


class HotelPhoto(Base):
    __tablename__ = "hotel_photos"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    url = Column(String(500), nullable=False)
    caption = Column(String(200))
    category = Column(SAEnum(PhotoCategory), default=PhotoCategory.EXTERIOR)
    is_main = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)


class RoomType(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    max_guests = Column(Integer, default=2)
    bed_type = Column(String(100))
    size_sqm = Column(Float)
    quantity = Column(Integer, default=1)
    base_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)


class RoomAmenity(Base):
    __tablename__ = "room_amenities"
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    name = Column(String(100), nullable=False)


class RoomPhoto(Base):
    __tablename__ = "room_photos"
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    url = Column(String(500), nullable=False)
    caption = Column(String(200))
    category = Column(String(50), default="interior")
    is_main = Column(Boolean, default=False)


class SeasonalPrice(Base):
    __tablename__ = "seasonal_prices"
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    name = Column(String(100))
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)


class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_no = Column(String(20), unique=True, nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    guest_name = Column(String(200))
    guest_email = Column(String(200))
    guest_phone = Column(String(20))
    check_in = Column(DateTime, nullable=False)
    check_out = Column(DateTime, nullable=False)
    nights = Column(Integer, nullable=False)
    adults = Column(Integer, default=1)
    children = Column(Integer, default=0)
    room_count = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(SAEnum(BookingStatus), default=BookingStatus.PENDING)
    special_requests = Column(Text)
    payment_status = Column(String(20), default="pending")
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RoomAvailability(Base):
    __tablename__ = "room_availability"
    id = Column(Integer, primary_key=True, index=True)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    available_count = Column(Integer, default=0)
    is_blocked = Column(Boolean, default=False)
    price_override = Column(Float)


class HotelReview(Base):
    __tablename__ = "hotel_reviews"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    cleanliness = Column(Integer)
    comfort = Column(Integer)
    location_score = Column(Integer)
    staff_score = Column(Integer)
    value_score = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
