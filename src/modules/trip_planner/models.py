from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, Enum as SAEnum, Date, Time, JSON
from src.database import Base
import enum


class TripStatus(str, enum.Enum):
    DRAFT = "draft"
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TransportMode(str, enum.Enum):
    WALKING = "walking"
    TAXI = "taxi"
    BUS = "bus"
    DOLMUS = "dolmus"
    MINIBUS = "minibus"
    TRAIN = "train"
    HIGH_SPEED_TRAIN = "high_speed_train"
    AIRPLANE = "airplane"
    FERRY = "ferry"
    SHUTTLE = "shuttle"
    RENTAL_CAR = "rental_car"
    PRIVATE_TRANSFER = "private_transfer"


class SegmentType(str, enum.Enum):
    TRANSPORT = "transport"
    STAY = "stay"
    ACTIVITY = "activity"
    FOOD = "food"
    RENTAL = "rental"
    DELIVERY = "delivery"
    MEETING = "meeting"


# ─── Ana Plan ────────────────────────────────────────────────
class TripPlan(Base):
    __tablename__ = "trip_plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(300), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    origin_city = Column(String(100))
    origin_address = Column(String(500))
    status = Column(SAEnum(TripStatus), default=TripStatus.DRAFT)
    total_budget = Column(Float, default=0)
    currency = Column(String(3), default="TRY")
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ─── Rota Segmenti (her bir bacak / hareket) ────────────────
class TripSegment(Base):
    __tablename__ = "trip_segments"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    segment_type = Column(SAEnum(SegmentType), default=SegmentType.TRANSPORT)

    # Origin
    origin_name = Column(String(300))
    origin_type = Column(String(50))
    origin_id = Column(Integer)
    origin_lat = Column(Float)
    origin_lng = Column(Float)
    origin_address = Column(String(500))

    # Destination
    destination_name = Column(String(300))
    destination_type = Column(String(50))
    destination_id = Column(Integer)
    destination_lat = Column(Float)
    destination_lng = Column(Float)
    destination_address = Column(String(500))

    # Transport specific
    transport_mode = Column(SAEnum(TransportMode))
    transport_schedule_id = Column(Integer)
    transport_ticket_id = Column(Integer)
    estimated_duration_minutes = Column(Integer)
    estimated_distance_km = Column(Float)
    cost = Column(Float, default=0)
    currency = Column(String(3), default="TRY")

    # Timing
    planned_departure = Column(DateTime(timezone=True))
    planned_arrival = Column(DateTime(timezone=True))
    actual_departure = Column(DateTime(timezone=True))
    actual_arrival = Column(DateTime(timezone=True))

    # Status
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Konaklama ───────────────────────────────────────────────
class TripStay(Base):
    __tablename__ = "trip_stays"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    segment_id = Column(Integer, ForeignKey("trip_segments.id"))
    sequence = Column(Integer, nullable=False)

    accommodation_type = Column(String(50))
    accommodation_id = Column(Integer)
    accommodation_name = Column(String(300))
    accommodation_booking_id = Column(Integer)
    check_in = Column(DateTime(timezone=True), nullable=False)
    check_out = Column(DateTime(timezone=True), nullable=False)
    address = Column(String(500))
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String(20))
    confirmation_code = Column(String(100))
    cost = Column(Float, default=0)
    currency = Column(String(3), default="TRY")
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Aktiviteler (etkinlik, gezi, toplantı, restoran) ───────
class TripActivity(Base):
    __tablename__ = "trip_activities"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    segment_id = Column(Integer, ForeignKey("trip_segments.id"))
    stay_id = Column(Integer, ForeignKey("trip_stays.id"))
    sequence = Column(Integer, nullable=False)

    activity_type = Column(String(50))
    activity_id = Column(Integer)
    activity_name = Column(String(300))
    category = Column(String(50))
    booking_id = Column(Integer)
    booking_no = Column(String(50))
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True))
    location_name = Column(String(300))
    location_address = Column(String(500))
    lat = Column(Float)
    lng = Column(Float)
    cost = Column(Float, default=0)
    currency = Column(String(3), default="TRY")
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Yemek (restoran rezervasyonu / sipariş) ─────────────────
class TripFood(Base):
    __tablename__ = "trip_foods"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    stay_id = Column(Integer, ForeignKey("trip_stays.id"))
    sequence = Column(Integer, nullable=False)

    food_type = Column(String(20))
    restaurant_id = Column(Integer)
    restaurant_name = Column(String(300))
    restaurant_address = Column(String(500))
    lat = Column(Float)
    lng = Column(Float)
    meal_time = Column(DateTime(timezone=True), nullable=False)
    participant_count = Column(Integer, default=1)
    cost = Column(Float, default=0)
    currency = Column(String(3), default="TRY")
    order_id = Column(Integer)
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Araç Kiralama ───────────────────────────────────────────
class TripRental(Base):
    __tablename__ = "trip_rentals"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    sequence = Column(Integer, nullable=False)

    vehicle_type = Column(String(50))
    rental_booking_id = Column(Integer, ForeignKey("rental_bookings.id"))
    rental_company = Column(String(200))
    pickup_location = Column(String(300))
    pickup_address = Column(String(500))
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    pickup_time = Column(DateTime(timezone=True), nullable=False)
    dropoff_location = Column(String(300))
    dropoff_address = Column(String(500))
    dropoff_lat = Column(Float)
    dropoff_lng = Column(Float)
    dropoff_time = Column(DateTime(timezone=True))
    total_cost = Column(Float, default=0)
    currency = Column(String(3), default="TRY")
    booking_reference = Column(String(100))
    is_confirmed = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Teslimat (e-ticaret kargosu) ────────────────────────────
class TripDelivery(Base):
    __tablename__ = "trip_deliveries"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trip_plans.id"), nullable=False)
    stay_id = Column(Integer, ForeignKey("trip_stays.id"), nullable=False)
    sequence = Column(Integer, nullable=False)

    order_id = Column(Integer, nullable=False)
    order_no = Column(String(50))
    cargo_company = Column(String(100))
    tracking_no = Column(String(100))
    estimated_delivery = Column(Date)
    delivery_address = Column(String(500))
    delivery_lat = Column(Float)
    delivery_lng = Column(Float)
    is_delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
