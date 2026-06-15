from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class ProductVariantGroup(Base):
    __tablename__ = "product_variant_groups"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    name = Column(String(100), nullable=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductVariantOption(Base):
    __tablename__ = "product_variant_options"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("product_variant_groups.id"), nullable=False)
    value = Column(String(100), nullable=False)
    sort_order = Column(Integer, default=0)


class ProductVariantSku(Base):
    __tablename__ = "product_variant_skus"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    barcode = Column(String(100))
    price_override = Column(Float)
    compare_price_override = Column(Float)
    stock = Column(Integer, default=0)
    image_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ProductVariantMapping(Base):
    __tablename__ = "product_variant_mappings"
    id = Column(Integer, primary_key=True, index=True)
    sku_id = Column(Integer, ForeignKey("product_variant_skus.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("product_variant_options.id"), nullable=False)
