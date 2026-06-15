from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class PwaManifest(Base):
    __tablename__ = "pwa_manifests"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    name = Column(String(200))
    short_name = Column(String(50))
    icon_url = Column(String(500))
    theme_color = Column(String(7))
    background_color = Column(String(7))
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

class CookieConsent(Base):
    __tablename__ = "cookie_consents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    session_id = Column(String(100))
    consent_type = Column(String(50))
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class GdprDataRequest(Base):
    __tablename__ = "gdpr_data_requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_type = Column(String(20))
    status = Column(String(20), default="pending")
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
