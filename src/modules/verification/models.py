from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class ProductVerification(Base):
    __tablename__ = "product_verifications"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    verifier_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")
    verified_at = Column(DateTime(timezone=True))
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
