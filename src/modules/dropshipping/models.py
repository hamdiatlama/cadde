from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class DropshippingSupplier(Base):
    __tablename__ = "dropshipping_suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200))
    api_url = Column(String(500))
    api_key = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class DropshippingProduct(Base):
    __tablename__ = "dropshipping_products"
    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("dropshipping_suppliers.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    supplier_sku = Column(String(100))
    cost_price = Column(Float)
    is_active = Column(Boolean, default=True)
