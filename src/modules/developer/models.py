from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class ApiKey(Base):
    __tablename__ = "api_keys"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_hash = Column(String(200), unique=True, nullable=False)
    key_prefix = Column(String(10))
    name = Column(String(100))
    permissions = Column(String(500))
    rate_limit = Column(Integer, default=100)
    is_active = Column(Boolean, default=True)
    last_used_at = Column(DateTime(timezone=True))
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Webhook(Base):
    __tablename__ = "webhooks"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url = Column(String(500), nullable=False)
    secret = Column(String(200))
    events = Column(String(1000))
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WebhookEvent(Base):
    __tablename__ = "webhook_events"
    id = Column(Integer, primary_key=True, index=True)
    webhook_id = Column(Integer, ForeignKey("webhooks.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    payload = Column(Text)
    status = Column(String(20), default="pending")
    response_code = Column(Integer)
    response_body = Column(Text)
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
