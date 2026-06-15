from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class MultiVendorCart(Base):
    __tablename__ = "multi_vendor_carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_amount = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MultiVendorCartItem(Base):
    __tablename__ = "multi_vendor_cart_items"
    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("multi_vendor_carts.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SellerApplication(Base):
    __tablename__ = "seller_applications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    company_name = Column(String(200))
    tax_number = Column(String(50))
    phone = Column(String(20))
    business_type = Column(String(50))
    status = Column(String(20), default="pending")
    reviewed_by = Column(Integer, ForeignKey("users.id"))
    reviewed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PreOrder(Base):
    __tablename__ = "pre_orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    expected_stock_date = Column(DateTime(timezone=True))
    status = Column(String(20), default="pending")
    order_id = Column(Integer, ForeignKey("orders.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GuestCheckout(Base):
    __tablename__ = "guest_checkouts"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), nullable=False)
    session_id = Column(String(100))
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    converted_to_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
