from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, Enum as SAEnum, Date, JSON
from src.database import Base
import enum


class RentalCategory(str, enum.Enum):
    CAR = "car"
    MOTORCYCLE = "motorcycle"
    SCOOTER = "scooter"
    BOAT = "boat"
    CARAVAN = "caravan"
    PLANE = "plane"


class RentalStatus(str, enum.Enum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"


class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    ACTIVE = "active"
    RETURNED = "returned"
    CANCELLED = "cancelled"


class FuelType(str, enum.Enum):
    GASOLINE = "gasoline"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    HYBRID = "hybrid"
    LPG = "lpg"


# ─── Kiralama Firması ────────────────────────────────────────
class RentalCompany(Base):
    __tablename__ = "rental_companies"
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
    categories = Column(JSON)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Şube / Ofis ────────────────────────────────────────────
class RentalBranch(Base):
    __tablename__ = "rental_branches"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("rental_companies.id"), nullable=False)
    name = Column(String(200))
    city = Column(String(100), nullable=False)
    district = Column(String(100))
    address = Column(String(500))
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Araç / Taşıt ────────────────────────────────────────────
class RentalVehicle(Base):
    __tablename__ = "rental_vehicles"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("rental_companies.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("rental_branches.id"))
    category = Column(SAEnum(RentalCategory), nullable=False)
    brand = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    year = Column(Integer)
    color = Column(String(50))
    plate_number = Column(String(20), unique=True)
    fuel_type = Column(SAEnum(FuelType))
    seat_count = Column(Integer)
    luggage_capacity = Column(String(50))
    engine_power = Column(String(50))
    has_ac = Column(Boolean, default=True)
    has_gps = Column(Boolean, default=False)
    has_bluetooth = Column(Boolean, default=False)
    mileage_limit_km = Column(Integer)
    daily_price = Column(Float, nullable=False)
    weekly_price = Column(Float)
    monthly_price = Column(Float)
    currency = Column(String(3), default="TRY")
    deposit_amount = Column(Float, default=0)
    photos = Column(JSON)
    features = Column(JSON)
    min_driver_age = Column(Integer, default=21)
    license_required_years = Column(Integer, default=1)
    status = Column(SAEnum(RentalStatus), default=RentalStatus.AVAILABLE)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RentalBooking(Base):
    __tablename__ = "rental_bookings"
    id = Column(Integer, primary_key=True, index=True)
    booking_no = Column(String(20), unique=True, nullable=False)
    vehicle_id = Column(Integer, ForeignKey("rental_vehicles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    pickup_branch_id = Column(Integer, ForeignKey("rental_branches.id"))
    dropoff_branch_id = Column(Integer, ForeignKey("rental_branches.id"))
    pickup_date = Column(DateTime(timezone=True), nullable=False)
    dropoff_date = Column(DateTime(timezone=True), nullable=False)
    pickup_location = Column(String(500))
    dropoff_location = Column(String(500))
    total_days = Column(Integer)
    daily_price = Column(Float)
    total_price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    deposit_paid = Column(Float, default=0)
    insurance_type = Column(String(50))
    insurance_cost = Column(Float, default=0)
    additional_driver = Column(Boolean, default=False)
    additional_driver_name = Column(String(200))
    driver_name = Column(String(200), nullable=False)
    driver_phone = Column(String(20))
    driver_email = Column(String(200))
    driver_license_no = Column(String(50))
    status = Column(SAEnum(BookingStatus), default=BookingStatus.PENDING)
    reseller_fee = Column(Float, default=0)
    commission_rate = Column(Float, default=0)
    notes = Column(Text)
    cancellation_reason = Column(Text)
    booked_at = Column(DateTime(timezone=True), server_default=func.now())
    returned_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RentalInsurance(Base):
    __tablename__ = "rental_insurances"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("rental_companies.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    coverage = Column(Text)
    daily_cost = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RentalReview(Base):
    __tablename__ = "rental_reviews"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("rental_bookings.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("rental_vehicles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_rating = Column(Integer)
    company_rating = Column(Integer)
    cleanliness_rating = Column(Integer)
    overall_rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
