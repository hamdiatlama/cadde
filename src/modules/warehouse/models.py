from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float
from src.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    country = Column(String(100), default="Türkiye")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WarehouseStock(Base):
    __tablename__ = "warehouse_stock"
    id = Column(Integer, primary_key=True, index=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    sku_id = Column(Integer, ForeignKey("product_variant_skus.id"), nullable=True)
    quantity = Column(Integer, default=0)
    min_threshold = Column(Integer, default=5)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WarehouseTransfer(Base):
    __tablename__ = "warehouse_transfers"
    id = Column(Integer, primary_key=True, index=True)
    from_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    to_warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
