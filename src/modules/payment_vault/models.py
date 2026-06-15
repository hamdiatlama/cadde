from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class SavedPaymentMethod(Base):
    __tablename__ = "saved_payment_methods"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), nullable=False)
    last_four = Column(String(4))
    card_holder = Column(String(100))
    card_brand = Column(String(50))
    expiry_month = Column(Integer)
    expiry_year = Column(Integer)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
