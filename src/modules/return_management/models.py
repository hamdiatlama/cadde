from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class ReturnRequest(Base):
    __tablename__ = "return_requests"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reason = Column(String(500))
    status = Column(String(20), default="pending")
    refund_amount = Column(Float)
    refund_method = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))
