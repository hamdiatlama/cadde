from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class ListingScore(Base):
    __tablename__ = "listing_scores"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, unique=True)
    score = Column(Integer, default=0)
    title_score = Column(Integer, default=0)
    description_score = Column(Integer, default=0)
    image_score = Column(Integer, default=0)
    price_score = Column(Integer, default=0)
    category_score = Column(Integer, default=0)
    suggestions = Column(Text)
    calculated_at = Column(DateTime(timezone=True), server_default=func.now())

class SellerAcademyCourse(Base):
    __tablename__ = "seller_academy_courses"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    content_url = Column(String(500))
    category = Column(String(50))
    duration_minutes = Column(Integer)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SellerAcademyProgress(Base):
    __tablename__ = "seller_academy_progress"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("seller_academy_courses.id"), nullable=False)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
