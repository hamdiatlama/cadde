from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func
from src.database import Base


class Restaurant(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    cuisine_type = Column(String, index=True)
    cuisine_subtypes = Column(String)
    phone = Column(String)
    description = Column(Text)
    logo_url = Column(String)
    cover_image_url = Column(String)
    is_active = Column(Boolean, default=True)
    is_open = Column(Boolean, default=True)
    accepts_orders = Column(Boolean, default=True)
    opening_time = Column(String, default="09:00")
    closing_time = Column(String, default="22:00")
    closed_days = Column(String)
    min_order_amount = Column(Float, default=0)
    delivery_fee = Column(Float, default=19.90)
    free_delivery_min_amount = Column(Float, default=100)
    max_delivery_radius_km = Column(Float, default=5.0)
    preparation_time_min = Column(Integer, default=20)
    has_thermal_bags = Column(Boolean, default=False)
    hygiene_rating = Column(String, default="pending")
    verification_status = Column(String, default="pending")
    verification_docs = Column(Text)
    commission_rate = Column(Float, default=0.15)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RestaurantBranch(Base):
    __tablename__ = "restaurant_branches"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String)
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    phone = Column(String)
    opening_time = Column(String)
    closing_time = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class FoodMenuItem(Base):
    __tablename__ = "food_menu_items"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    branch_id = Column(Integer, ForeignKey("restaurant_branches.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String, index=True)
    subcategory = Column(String)
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    calories_kcal = Column(Integer)
    protein_g = Column(Float)
    carbs_g = Column(Float)
    fat_g = Column(Float)
    fiber_g = Column(Float)
    serving_size = Column(String)
    is_vegetarian = Column(Boolean, default=False)
    is_vegan = Column(Boolean, default=False)
    is_gluten_free = Column(Boolean, default=False)
    is_halal = Column(Boolean, default=False)
    is_spicy = Column(Boolean, default=False)
    dietary_tags = Column(String)
    allergens = Column(String)
    image_url = Column(String)
    image_urls = Column(String)
    is_available = Column(Boolean, default=True)
    preparation_time_min = Column(Integer, default=10)
    sort_order = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MenuItemModifier(Base):
    __tablename__ = "menu_item_modifiers"
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("food_menu_items.id"), nullable=False)
    group_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    price_modifier = Column(Float, default=0)
    max_select = Column(Integer, default=1)
    sort_order = Column(Integer, default=0)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)


class DeliveryZone(Base):
    __tablename__ = "delivery_zones"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    name = Column(String, nullable=False)
    min_latitude = Column(Float, nullable=False)
    max_latitude = Column(Float, nullable=False)
    min_longitude = Column(Float, nullable=False)
    max_longitude = Column(Float, nullable=False)
    delivery_fee = Column(Float, default=0)
    min_order = Column(Float, default=0)
    estimated_delivery_min = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_role = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TemperatureCheck(Base):
    __tablename__ = "temperature_checks"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    check_type = Column(String, default="pickup")
    photo_url = Column(String)
    notes = Column(Text)
    is_acceptable = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class HygieneReport(Base):
    __tablename__ = "hygiene_reports"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    report_type = Column(String, default="customer")
    issue_type = Column(String, nullable=False)
    description = Column(Text)
    photo_urls = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DriverReport(Base):
    __tablename__ = "driver_reports"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    reporter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("couriers.id"), nullable=False)
    rating = Column(Integer, default=5)
    issue_type = Column(String)
    description = Column(Text)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BatchDeliveryPrevention(Base):
    __tablename__ = "batch_delivery_prevention"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, unique=True)
    max_batch_size = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
