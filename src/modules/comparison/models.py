from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, UniqueConstraint
from src.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), default="Karşılaştırma")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ComparisonItem(Base):
    __tablename__ = "comparison_items"
    id = Column(Integer, primary_key=True, index=True)
    comparison_id = Column(Integer, ForeignKey("comparisons.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    __table_args__ = (UniqueConstraint("comparison_id", "product_id"),)
