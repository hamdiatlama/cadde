from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class PosTerminal(Base):
    __tablename__ = "pos_terminals"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100))
    serial_no = Column(String(100), unique=True)
    location = Column(String(200))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PosOrder(Base):
    __tablename__ = "pos_orders"
    id = Column(Integer, primary_key=True, index=True)
    terminal_id = Column(Integer, ForeignKey("pos_terminals.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("users.id"))
    order_id = Column(Integer, ForeignKey("orders.id"))
    total = Column(Float, nullable=False)
    payment_method = Column(String(50))
    status = Column(String(20), default="completed")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PosOrderItem(Base):
    __tablename__ = "pos_order_items"
    id = Column(Integer, primary_key=True, index=True)
    pos_order_id = Column(Integer, ForeignKey("pos_orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    barcode = Column(String(100))
    name = Column(String(200))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
