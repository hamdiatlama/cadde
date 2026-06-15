from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey, JSON
from src.database import Base


class ReputationProfile(Base):
    __tablename__ = "reputation_profiles"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), unique=True, nullable=False)
    overall_score = Column(Float, default=0)
    review_count = Column(Integer, default=0)
    response_rate = Column(Float, default=0)
    avg_response_time_hours = Column(Float)
    platform_scores = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ExternalReview(Base):
    __tablename__ = "external_reviews"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    platform = Column(String(50))
    external_review_id = Column(String(200))
    reviewer_name = Column(String(200))
    rating = Column(Float)
    title = Column(String(200))
    comment = Column(Text)
    language = Column(String(10))
    reviewed_at = Column(DateTime(timezone=True))
    imported_at = Column(DateTime(timezone=True))
    is_responded = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReviewResponse(Base):
    __tablename__ = "review_responses"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("external_reviews.id"), nullable=False)
    response_text = Column(Text)
    responded_by = Column(Integer, ForeignKey("users.id"))
    is_auto_generated = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SentimentAnalysis(Base):
    __tablename__ = "sentiment_analysis"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("external_reviews.id"), nullable=False)
    sentiment = Column(String(20))
    score = Column(Float)
    keywords = Column(JSON)
    category = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ReputationAlert(Base):
    __tablename__ = "reputation_alerts"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    alert_type = Column(String(50))
    severity = Column(String(20))
    message = Column(Text)
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
