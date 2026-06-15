from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Date, ForeignKey, func
from src.database import Base


class FloristProfile(Base):
    __tablename__ = "florist_profiles"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    shop_name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    cover_url = Column(String(500))
    phone = Column(String(20))
    city = Column(String(100))
    district = Column(String(100))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    is_active = Column(Boolean, default=True)
    is_open = Column(Boolean, default=True)
    preparation_time_min = Column(Integer, default=30)
    delivery_radius_km = Column(Float, default=5.0)
    min_order_amount = Column(Float, default=0)
    delivery_fee = Column(Float, default=0)
    free_delivery_min_amount = Column(Float)
    working_hours_json = Column(Text)
    holiday_dates = Column(Text)
    verification_status = Column(String(20), default="pending")
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    total_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class FlowerProducerProfile(Base):
    __tablename__ = "flower_producer_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String(255))
    production_type = Column(String(50))
    capacity_per_month = Column(Integer)
    area_size = Column(Float)
    area_unit = Column(String(10), default="donum")
    city = Column(String(100))
    district = Column(String(100))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    organic_certificate = Column(Boolean, default=False)
    global_gap = Column(Boolean, default=False)
    good_agriculture = Column(Boolean, default=False)
    harvest_calendar_json = Column(Text)
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FlowerWholesalerProfile(Base):
    __tablename__ = "flower_wholesaler_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String(255), nullable=False)
    tax_id = Column(String(50))
    warehouse_address = Column(Text)
    city = Column(String(100))
    district = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)
    has_cold_storage = Column(Boolean, default=False)
    min_order_amount = Column(Float, default=0)
    shipping_type = Column(String(50))
    working_region = Column(String(255))
    is_verified = Column(Boolean, default=False)
    rating = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MaterialSupplierProfile(Base):
    __tablename__ = "material_supplier_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    company_name = Column(String(255), nullable=False)
    supplier_type = Column(String(50))
    product_list_json = Column(Text)
    min_order_amount = Column(Float, default=0)
    shipping_conditions = Column(Text)
    city = Column(String(100))
    district = Column(String(100))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FlowerProduct(Base):
    __tablename__ = "flower_products"

    id = Column(Integer, primary_key=True, index=True)
    seller_type = Column(String(20), nullable=False)
    seller_id = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    slug = Column(String(255))
    description = Column(Text)
    category = Column(String(50))
    subcategory = Column(String(50))
    occasion = Column(String(50))
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    stock = Column(Integer, default=0)
    unit = Column(String(20), default="adet")
    size = Column(String(50))
    weight_kg = Column(Float)
    color = Column(String(50))
    colors_json = Column(Text)
    flowers_json = Column(Text)
    meaning = Column(Text)
    season = Column(String(50))
    lifespan_days = Column(Integer)
    care_level = Column(String(20))
    has_vase = Column(Boolean, default=False)
    vase_type = Column(String(50))
    is_express_eligible = Column(Boolean, default=False)
    is_customizable = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    images_json = Column(Text)
    origin = Column(String(100))
    fragrance = Column(String(50))
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class CustomOrderDesign(Base):
    __tablename__ = "custom_order_designs"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    florist_id = Column(Integer, ForeignKey("florist_profiles.id"))
    theme = Column(String(50))
    size = Column(String(20))
    flowers_json = Column(Text)
    extras_json = Column(Text)
    vase_type = Column(String(50))
    card_message = Column(Text, nullable=False)
    card_design = Column(String(50))
    card_type = Column(String(20), default="dijital")
    total_price = Column(Float)
    status = Column(String(20), default="tasarim")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SpecialDayReminder(Base):
    __tablename__ = "special_day_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(255), nullable=False)
    reminder_date = Column(Date, nullable=False)
    occasion_type = Column(String(50))
    is_yearly = Column(Boolean, default=True)
    previous_order_id = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FloristImage(Base):
    __tablename__ = "florist_images"

    id = Column(Integer, primary_key=True, index=True)
    florist_id = Column(Integer, ForeignKey("florist_profiles.id"))
    category = Column(String(30), nullable=False)
    file_path = Column(String(500), nullable=False)
    resolution = Column(String(20))
    taken_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    score_contribution = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FloristCamera(Base):
    __tablename__ = "florist_cameras"

    id = Column(Integer, primary_key=True, index=True)
    florist_id = Column(Integer, ForeignKey("florist_profiles.id"))
    camera_name = Column(String(255))
    resolution = Column(String(20))
    stream_url = Column(String(500))
    is_active = Column(Boolean, default=False)
    last_interruption_at = Column(DateTime(timezone=True))
    working_hours_compliant = Column(Boolean, default=True)
    score_contribution = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FreshnessChain(Base):
    __tablename__ = "freshness_chain"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    stage = Column(String(30), nullable=False)
    happened_at = Column(DateTime(timezone=True), server_default=func.now())
    latitude = Column(Float)
    longitude = Column(Float)
    photo_url = Column(String(500))
    is_confirmed = Column(Boolean, default=False)


class FloristDocumentScore(Base):
    __tablename__ = "florist_document_scores"

    id = Column(Integer, primary_key=True, index=True)
    florist_id = Column(Integer, ForeignKey("florist_profiles.id"))
    document_type = Column(String(50), nullable=False)
    score = Column(Integer, default=0)
    file_path = Column(String(500))
    valid_until = Column(Date)
    is_confirmed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FlowerRating(Base):
    __tablename__ = "flower_ratings"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, index=True)
    rater_id = Column(Integer, ForeignKey("users.id"))
    rater_type = Column(String(20), nullable=False)
    rated_id = Column(Integer, nullable=False)
    rated_type = Column(String(20), nullable=False)
    score = Column(Float, nullable=False, default=5.0)
    criteria_json = Column(Text)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DeliveryTimeLog(Base):
    __tablename__ = "delivery_time_logs"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer)
    estimated_minutes = Column(Integer)
    actual_minutes = Column(Integer)
    weather_condition = Column(String(50))
    traffic_condition = Column(String(50))
    deviation_percent = Column(Float)
    improvement_suggestion = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
