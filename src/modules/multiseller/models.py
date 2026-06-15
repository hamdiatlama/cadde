from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class SellerOffer(Base):
    __tablename__ = "seller_offers"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_winning = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
