from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey, Text
from src.database import Base


class ProductView(Base):
    __tablename__ = "product_views"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    session_id = Column(String(100))
    viewed_at = Column(DateTime(timezone=True), server_default=func.now())


class SearchHistory(Base):
    __tablename__ = "search_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    query = Column(String(200), nullable=False)
    session_id = Column(String(100))
    searched_at = Column(DateTime(timezone=True), server_default=func.now())
