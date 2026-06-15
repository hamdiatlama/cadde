from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, func
from src.database import Base


class FoodSupplier(Base):
    __tablename__ = "food_suppliers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    company_name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    logo_url = Column(String(500))
    cover_url = Column(String(500))
    supplier_type = Column(String(20), nullable=False, default="producer")
    city = Column(String(100))
    district = Column(String(100))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    contact_phone = Column(String(50))
    contact_email = Column(String(255))
    website_url = Column(String(500))
    is_organic_certified = Column(Boolean, default=False)
    is_halal_certified = Column(Boolean, default=False)
    certifications = Column(Text)
    product_categories = Column(String)
    kitchen_photos = Column(String)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    verification_status = Column(String(20), default="pending")
    is_active = Column(Boolean, default=True)
    created_at = Column(Text, server_default=func.datetime("now"))
    updated_at = Column(Text, server_default=func.datetime("now"))


class FoodSupplierProduct(Base):
    __tablename__ = "food_supplier_products"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("food_suppliers.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100), nullable=False, index=True)
    subcategory = Column(String(100))
    unit = Column(String(50), nullable=False, default="kg")
    price_per_unit = Column(Float)
    is_organic = Column(Boolean, default=False)
    is_local = Column(Boolean, default=False)
    season_start_month = Column(Integer)
    season_end_month = Column(Integer)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(Text, server_default=func.datetime("now"))


class FoodRestaurantSupplier(Base):
    __tablename__ = "food_restaurant_suppliers"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), nullable=False)
    supplier_id = Column(Integer, ForeignKey("food_suppliers.id"), nullable=False)
    is_preferred = Column(Boolean, default=False)
    contract_start = Column(String)
    contract_end = Column(String)
    notes = Column(Text)
    created_at = Column(Text, server_default=func.datetime("now"))


class FoodMenuItemIngredient(Base):
    __tablename__ = "food_menu_item_ingredients"
    id = Column(Integer, primary_key=True, index=True)
    menu_item_id = Column(Integer, ForeignKey("food_menu_items.id"), nullable=False)
    supplier_product_id = Column(Integer, ForeignKey("food_supplier_products.id"), nullable=False)
    quantity = Column(Float)
    unit = Column(String(50))
    notes = Column(Text)
    is_visible_to_customer = Column(Boolean, default=True)
    created_at = Column(Text, server_default=func.datetime("now"))


class FoodTransparencyScore(Base):
    __tablename__ = "food_transparency_scores"
    id = Column(Integer, primary_key=True, index=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"), unique=True, nullable=False)
    total_menu_items = Column(Integer, default=0)
    items_with_ingredients = Column(Integer, default=0)
    total_suppliers_linked = Column(Integer, default=0)
    transparency_percentage = Column(Float, default=0)
    total_points = Column(Integer, default=0)
    last_calculated_at = Column(Text, server_default=func.datetime("now"))
    created_at = Column(Text, server_default=func.datetime("now"))
