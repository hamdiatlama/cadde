from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class AbandonedCart(Base):
    __tablename__ = "abandoned_carts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cart_data = Column(Text)
    total = Column(Integer, default=0)
    reminder_sent = Column(Boolean, default=False)
    reminder_count = Column(Integer, default=0)
    recovered = Column(Boolean, default=False)
    recovered_order_id = Column(Integer, ForeignKey("orders.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_reminder_at = Column(DateTime(timezone=True))


class CartReminderTemplate(Base):
    __tablename__ = "cart_reminder_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    subject = Column(String(200))
    body = Column(Text)
    delay_hours = Column(Integer, default=24)
    is_active = Column(Boolean, default=True)
