from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, Enum as SAEnum, Time, Date, JSON
from src.database import Base
import enum


class VehicleType(str, enum.Enum):
    BUS = "bus"
    MINIBUS = "minibus"
    DOLMUS = "dolmus"
    TRAIN = "train"
    HIGH_SPEED_TRAIN = "high_speed_train"
    AIRPLANE = "airplane"
    FERRY = "ferry"


class SeatClass(str, enum.Enum):
    ECONOMY = "economy"
    BUSINESS = "business"
    FIRST = "first"
    PREMIUM = "premium"


class TicketStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    USED = "used"
    REFUNDED = "refunded"


# ─── Firma / Şirket ─────────────────────────────────────────
class TransportCompany(Base):
    __tablename__ = "transport_companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    vehicle_type = Column(SAEnum(VehicleType), nullable=False)
    code = Column(String(20), unique=True)
    logo_url = Column(String(500))
    phone = Column(String(20))
    email = Column(String(200))
    website = Column(String(200))
    description = Column(Text)
    is_operator = Column(Boolean, default=True)
    commission_percent = Column(Float, default=2.0)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    tax_id = Column(String(50))
    company_address = Column(Text)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Durak / İstasyon ───────────────────────────────────────
class TransportStation(Base):
    __tablename__ = "transport_stations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    district = Column(String(100))
    address = Column(String(500))
    lat = Column(Float)
    lng = Column(Float)
    code = Column(String(20))
    type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Rota ────────────────────────────────────────────────────
class TransportRoute(Base):
    __tablename__ = "transport_routes"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("transport_companies.id"), nullable=False)
    origin_station_id = Column(Integer, ForeignKey("transport_stations.id"), nullable=False)
    destination_station_id = Column(Integer, ForeignKey("transport_stations.id"), nullable=False)
    name = Column(String(200))
    duration_minutes = Column(Integer)
    distance_km = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Rota Üzerindeki Duraklar / Yolcu Alma Noktaları ────────
class TransportRouteStop(Base):
    __tablename__ = "transport_route_stops"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("transport_routes.id"), nullable=False)
    station_id = Column(Integer, ForeignKey("transport_stations.id"), nullable=True)
    name = Column(String(200), nullable=False)
    lat = Column(Float)
    lng = Column(Float)
    km_from_start = Column(Float, default=0)
    minutes_from_departure = Column(Integer, default=0)
    can_pickup = Column(Boolean, default=True)
    can_dropoff = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Araç / Filon ────────────────────────────────────────────
class TransportVehicle(Base):
    __tablename__ = "transport_vehicles"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("transport_companies.id"), nullable=False)
    plate_number = Column(String(20), nullable=False, unique=True)
    brand = Column(String(100))
    model = Column(String(100))
    year = Column(Integer)
    color = Column(String(50))
    seat_count = Column(Integer, nullable=False)
    features = Column(JSON)
    has_wifi = Column(Boolean, default=False)
    has_ac = Column(Boolean, default=True)
    has_toilet = Column(Boolean, default=False)
    has_usb = Column(Boolean, default=False)
    has_tv = Column(Boolean, default=False)
    photo_url = Column(String(500))
    last_maintenance_date = Column(Date)
    next_maintenance_date = Column(Date)
    inspection_date = Column(Date)
    insurance_date = Column(Date)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Şoför ───────────────────────────────────────────────────
class TransportDriver(Base):
    __tablename__ = "transport_drivers"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("transport_companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(200))
    license_number = Column(String(50))
    license_class = Column(String(20))
    license_expiry = Column(Date)
    tc_kimlik = Column(String(20))
    address = Column(Text)
    photo_url = Column(String(500))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Sefer (Her sefer = bir rota + bir gün + bir araç + bir şoför) ──
class TransportSchedule(Base):
    __tablename__ = "transport_schedules"
    id = Column(Integer, primary_key=True, index=True)
    route_id = Column(Integer, ForeignKey("transport_routes.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("transport_vehicles.id"))
    driver_id = Column(Integer, ForeignKey("transport_drivers.id"))
    departure_date = Column(Date, nullable=False)
    departure_time = Column(Time, nullable=False)
    arrival_time = Column(Time)
    base_price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    total_seats = Column(Integer, nullable=False)
    available_seats = Column(Integer, nullable=False)
    vehicle_number = Column(String(50))
    status = Column(String(20), default="active")
    is_pickup_route = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Seferin her duraktaki tahmini zamanı ────────────────────
class ScheduleStopTime(Base):
    __tablename__ = "schedule_stop_times"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("transport_schedules.id"), nullable=False)
    route_stop_id = Column(Integer, ForeignKey("transport_route_stops.id"), nullable=False)
    estimated_time = Column(Time, nullable=False)
    estimated_minutes = Column(Integer)
    is_active = Column(Boolean, default=True)


# ─── Koltuk ──────────────────────────────────────────────────
class TransportSeat(Base):
    __tablename__ = "transport_seats"
    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("transport_schedules.id"), nullable=False)
    seat_number = Column(String(10), nullable=False)
    seat_class = Column(SAEnum(SeatClass), default=SeatClass.ECONOMY)
    price = Column(Float)
    is_window = Column(Boolean, default=False)
    is_aisle = Column(Boolean, default=False)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Bilet ───────────────────────────────────────────────────
class TransportTicket(Base):
    __tablename__ = "transport_tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_no = Column(String(20), unique=True, nullable=False)
    schedule_id = Column(Integer, ForeignKey("transport_schedules.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("transport_seats.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agency_id = Column(Integer, ForeignKey("agencies.id"))
    pickup_stop_id = Column(Integer, ForeignKey("transport_route_stops.id"))
    dropoff_stop_id = Column(Integer, ForeignKey("transport_route_stops.id"))
    passenger_name = Column(String(200), nullable=False)
    passenger_surname = Column(String(200))
    passenger_id_no = Column(String(20))
    passenger_phone = Column(String(20))
    passenger_email = Column(String(200))
    pickup_lat = Column(Float)
    pickup_lng = Column(Float)
    pickup_address = Column(String(500))
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    provider_ticket_no = Column(String(100))
    reseller_fee = Column(Float, default=0)
    commission_rate = Column(Float, default=0)
    status = Column(SAEnum(TicketStatus), default=TicketStatus.PENDING)
    booking_reference = Column(String(50))
    qr_code = Column(String(500))
    checked_in = Column(Boolean, default=False)
    notified_pickup_15min = Column(Boolean, default=False)
    notified_driver = Column(Boolean, default=False)
    cancellation_reason = Column(Text)
    bought_at = Column(DateTime(timezone=True), server_default=func.now())
    cancelled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Rota Üzerinden Yolcu Alma (Pickup Booking) ─────────────
class TransportPickupBooking(Base):
    __tablename__ = "transport_pickup_bookings"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("transport_tickets.id"), nullable=False)
    schedule_id = Column(Integer, ForeignKey("transport_schedules.id"), nullable=False)
    pickup_stop_id = Column(Integer, ForeignKey("transport_route_stops.id"), nullable=False)
    pickup_time = Column(Time)
    passenger_phone = Column(String(20))
    status = Column(String(20), default="pending")
    driver_notified = Column(Boolean, default=False)
    passenger_notified = Column(Boolean, default=False)
    picked_up = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Değerlendirme ───────────────────────────────────────────
class TransportRating(Base):
    __tablename__ = "transport_ratings"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("transport_tickets.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("transport_companies.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("transport_drivers.id"))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_rating = Column(Integer)
    driver_rating = Column(Integer)
    cleanliness_rating = Column(Integer)
    comfort_rating = Column(Integer)
    punctuality_rating = Column(Integer)
    overall_rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ─── Belge Yönetimi ─────────────────────────────────────────
class TransportDocument(Base):
    __tablename__ = "transport_documents"
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("transport_companies.id"))
    vehicle_id = Column(Integer, ForeignKey("transport_vehicles.id"))
    driver_id = Column(Integer, ForeignKey("transport_drivers.id"))
    doc_type = Column(String(50), nullable=False)
    doc_name = Column(String(200))
    doc_number = Column(String(100))
    file_url = Column(String(500))
    issue_date = Column(Date)
    expiry_date = Column(Date)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
