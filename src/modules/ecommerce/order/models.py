from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="pending_approval")
    subtotal = Column(Float, nullable=False)
    delivery_fee = Column(Float, default=0)
    total = Column(Float, nullable=False)
    payment_method = Column(String, default="card")
    payment_status = Column(String, default="pending")
    notes = Column(Text)
    recipient_name = Column(String)
    recipient_phone = Column(String)
    delivery_address = Column(Text)
    delivery_latitude = Column(Float)
    delivery_longitude = Column(Float)
    scheduled_date = Column(DateTime(timezone=True))
    delivery_time_slot = Column(String)
    is_express = Column(Boolean, default=False)
    express_fee = Column(Float, default=0)
    is_gift = Column(Boolean, default=False)
    gift_card_message = Column(Text)
    gift_card_sender = Column(String)
    coupon_code = Column(String)
    discount_amount = Column(Float, default=0)
    tip_amount = Column(Float, default=0)
    contactless_delivery = Column(Boolean, default=False)
    branch_id = Column(Integer, ForeignKey("restaurant_branches.id"))
    approved_at = Column(DateTime(timezone=True))
    rejected_at = Column(DateTime(timezone=True))
    reject_reason = Column(Text)
    approval_deadline = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))
    cancel_reason = Column(Text)
    tracking_no = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("food_menu_items.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    modifiers = Column(Text)


class Substitution(Base):
    __tablename__ = "substitutions"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    order_item_id = Column(Integer, ForeignKey("order_items.id"), nullable=False)
    original_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    suggested_product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    suggested_product_name = Column(String, nullable=False)
    suggested_product_price = Column(Float, nullable=False)
    status = Column(String, default="pending")
    responded_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
