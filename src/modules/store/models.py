from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    name = Column(String, nullable=False)
    slug = Column(String, index=True)
    description = Column(Text)
    category = Column(String, index=True)
    subcategory = Column(String, index=True)
    price = Column(Float, nullable=False)
    compare_price = Column(Float)
    original_price = Column(Float)
    discount_start_at = Column(DateTime(timezone=True))
    image_url = Column(String)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    is_discounted = Column(Boolean, default=False)
    original_product_id = Column(Integer, ForeignKey("products.id"))
    tags = Column(String)
    color = Column(String)
    occasion = Column(String, index=True)
    care_instructions = Column(Text)
    season_start_month = Column(Integer)
    season_end_month = Column(Integer)
    is_express_eligible = Column(Boolean, default=False)
    rating = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductExtra(Base):
    __tablename__ = "product_extras"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    price = Column(Float, default=0)
    is_active = Column(Boolean, default=True)


class Bouquet(Base):
    __tablename__ = "bouquets"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    image_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True, nullable=False)
    discount_type = Column(String, default="percentage")
    discount_value = Column(Float, nullable=False)
    min_order_amount = Column(Float, default=0)
    max_uses = Column(Integer)
    current_uses = Column(Integer, default=0)
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
