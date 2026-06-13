from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from src.database import Base


class DeliveryPhoto(Base):
    __tablename__ = "delivery_photos"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    courier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    photo_url = Column(String, nullable=False)
    photo_type = Column(String, default="delivery")
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
