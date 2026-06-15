from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class GiftCard(Base):
    __tablename__ = "gift_cards"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    balance = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipient_email = Column(String)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GiftCardTransaction(Base):
    __tablename__ = "gift_card_transactions"
    id = Column(Integer, primary_key=True, index=True)
    gift_card_id = Column(Integer, ForeignKey("gift_cards.id"), nullable=False)
    amount = Column(Float, nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
