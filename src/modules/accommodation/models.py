from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, JSON
from src.database import Base


class AccommodationSatisfactionSurvey(Base):
    __tablename__ = "accommodation_satisfaction_surveys"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    overall_score = Column(Integer)
    would_recommend = Column(Boolean)
    checkin_experience = Column(Integer)
    cleanliness_score = Column(Integer)
    service_score = Column(Integer)
    view_score = Column(Integer)
    food_score = Column(Integer)
    value_score = Column(Integer)
    noise_score = Column(Integer)
    bed_comfort = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AccommodationReviewPhoto(Base):
    __tablename__ = "accommodation_review_photos"
    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("hotel_reviews.id"), nullable=False)
    url = Column(String(500), nullable=False)
    caption = Column(String(200))
    sort_order = Column(Integer, default=0)


class GuestComplaint(Base):
    __tablename__ = "guest_complaints"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category = Column(String(50), nullable=False)
    priority = Column(String(20), default="normal")
    description = Column(Text, nullable=False)
    status = Column(String(20), default="open")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComplaintResolution(Base):
    __tablename__ = "complaint_resolutions"
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("guest_complaints.id"), nullable=False)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    resolution_notes = Column(Text)
    compensation = Column(String(500))
    resolved_at = Column(DateTime(timezone=True), server_default=func.now())


class GuestPreference(Base):
    __tablename__ = "guest_preferences"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    preferred_room_type = Column(String(100))
    dietary_restrictions = Column(Text)
    special_needs = Column(Text)
    preferred_floor = Column(String(20))
    smoking_preference = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HousekeepingLog(Base):
    __tablename__ = "housekeeping_logs"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=True)
    room_number = Column(String(20))
    cleaning_date = Column(DateTime, nullable=False)
    cleaner_name = Column(String(100))
    checklist_items = Column(JSON)
    status = Column(String(20), default="completed")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyFumigationLog(Base):
    __tablename__ = "property_fumigation_logs"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    scheduled_date = Column(DateTime)
    fumigation_date = Column(DateTime)
    next_fumigation_date = Column(DateTime)
    chemical_used = Column(String(200))
    company_name = Column(String(200))
    technician_name = Column(String(100))
    target_pests = Column(String(200))
    areas_treated = Column(Text)
    status = Column(String(20), default="scheduled")
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HotelKitchen(Base):
    __tablename__ = "hotel_kitchens"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    cuisine_type = Column(String(100))
    is_open = Column(Boolean, default=True)
    opening_time = Column(String(5), default="07:00")
    closing_time = Column(String(5), default="22:00")
    min_order_amount = Column(Float, default=0)
    preparation_time_min = Column(Integer, default=30)
    phone = Column(String(20))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HotelMenuItem(Base):
    __tablename__ = "hotel_menu_items"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    kitchen_id = Column(Integer, ForeignKey("hotel_kitchens.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    is_available = Column(Boolean, default=True)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    image_url = Column(String(500))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InRoomDiningOrder(Base):
    __tablename__ = "in_room_dining_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(20), unique=True, nullable=False)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    kitchen_id = Column(Integer, ForeignKey("hotel_kitchens.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    room_number = Column(String(20))
    items = Column(JSON, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default="ordered")
    special_instructions = Column(Text)
    ordered_at = Column(DateTime(timezone=True), server_default=func.now())
    prepared_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))


class HotelKitchenReview(Base):
    __tablename__ = "hotel_kitchen_reviews"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    kitchen_id = Column(Integer, ForeignKey("hotel_kitchens.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("in_room_dining_orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_quality = Column(Integer)
    presentation = Column(Integer)
    delivery_speed = Column(Integer)
    temperature = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class NearbyPlace(Base):
    __tablename__ = "nearby_places"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    distance_km = Column(Float)
    lat = Column(Float)
    lng = Column(Float)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ═══════════════════════════════════════════════════════════════════
# Property Safety & Compliance (Güvenlik, Yangın, İnşaat, Denetim)
# ═══════════════════════════════════════════════════════════════════

class PropertyBuildingInfo(Base):
    __tablename__ = "property_building_info"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False, unique=True)
    year_built = Column(Integer)
    architect = Column(String(200))
    contractor = Column(String(200))
    construction_company = Column(String(200))
    building_type = Column(String(100))
    number_of_floors = Column(Integer)
    total_room_count = Column(Integer)
    has_elevator = Column(Boolean, default=False)
    has_generator = Column(Boolean, default=False)
    has_parking = Column(Boolean, default=False)
    has_shelter = Column(Boolean, default=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class FireSafetySystem(Base):
    __tablename__ = "fire_safety_systems"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    system_type = Column(String(100), nullable=False)
    has_sprinkler = Column(Boolean, default=False)
    has_fire_alarm = Column(Boolean, default=False)
    has_fire_extinguisher = Column(Boolean, default=False)
    has_fire_hose = Column(Boolean, default=False)
    has_emergency_exit = Column(Boolean, default=False)
    has_fire_escape = Column(Boolean, default=False)
    installation_company = Column(String(200))
    last_service_date = Column(DateTime)
    next_service_date = Column(DateTime)
    certificate_number = Column(String(100))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PropertySecuritySystem(Base):
    __tablename__ = "property_security_systems"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    has_cctv = Column(Boolean, default=False)
    has_alarm = Column(Boolean, default=False)
    has_security_personnel = Column(Boolean, default=False)
    has_room_safe = Column(Boolean, default=False)
    has_electronic_card = Column(Boolean, default=False)
    has_24h_front_desk = Column(Boolean, default=False)
    has_fire_door = Column(Boolean, default=False)
    has_emergency_lighting = Column(Boolean, default=False)
    has_smoke_detector = Column(Boolean, default=False)
    has_co_detector = Column(Boolean, default=False)
    installation_company = Column(String(200))
    verification_date = Column(DateTime)
    verification_company = Column(String(200))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PropertyInspection(Base):
    __tablename__ = "property_inspections"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    inspection_type = Column(String(50), nullable=False)
    inspector_name = Column(String(200))
    inspector_organization = Column(String(200))
    inspection_date = Column(DateTime, nullable=False)
    result = Column(String(20))
    certificate_number = Column(String(100))
    valid_until = Column(DateTime)
    findings = Column(Text)
    notes = Column(Text)
    document_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SafetyCertificate(Base):
    __tablename__ = "safety_certificates"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    certificate_type = Column(String(100), nullable=False)
    certificate_number = Column(String(200))
    issuing_authority = Column(String(200))
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    document_url = Column(String(500))
    is_valid = Column(Boolean, default=True)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TourismAssociation(Base):
    __tablename__ = "tourism_associations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    association_type = Column(String(50), nullable=False)
    city = Column(String(100))
    phone = Column(String(20))
    website = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyAssociationMember(Base):
    __tablename__ = "property_association_members"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    association_id = Column(Integer, ForeignKey("tourism_associations.id"), nullable=False)
    membership_number = Column(String(100))
    member_since = Column(DateTime)
    valid_until = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HotelSuspension(Base):
    __tablename__ = "hotel_suspensions"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    suspension_number = Column(Integer, default=1)
    reason = Column(Text, nullable=False)
    duration_days = Column(Integer, nullable=False)
    start_date = Column(DateTime(timezone=True), nullable=False)
    end_date = Column(DateTime(timezone=True), nullable=False)
    triggered_by_complaint_id = Column(Integer, ForeignKey("guest_complaints.id"))
    resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComplaintAction(Base):
    __tablename__ = "complaint_actions"
    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("guest_complaints.id"), nullable=False)
    action_type = Column(String(50), nullable=False)
    description = Column(Text)
    performed_by = Column(Integer, ForeignKey("users.id"))
    deadline = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class LocationRegistrationRequest(Base):
    __tablename__ = "location_registration_requests"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    existing_hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(Text)
    status = Column(String(20), default="pending")
    approved_by = Column(Integer, ForeignKey("users.id"))
    approved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GuestBan(Base):
    __tablename__ = "guest_bans"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason_category = Column(String(50), nullable=False)
    description = Column(Text)
    is_permanent = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    issued_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    revoked_at = Column(DateTime(timezone=True))
    revoked_by = Column(Integer, ForeignKey("users.id"))


class PropertyDocument(Base):
    __tablename__ = "property_documents"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    document_type = Column(String(100), nullable=False)
    document_name = Column(String(200))
    file_url = Column(String(500), nullable=False)
    reference_number = Column(String(100))
    issuing_authority = Column(String(200))
    issue_date = Column(DateTime)
    expiry_date = Column(DateTime)
    is_verified = Column(Boolean, default=False)
    verified_by = Column(Integer, ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
