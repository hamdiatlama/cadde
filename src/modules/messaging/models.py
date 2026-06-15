from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class EmailTemplate(Base):
    __tablename__ = "email_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    subject = Column(String(200))
    body_html = Column(Text)
    event_type = Column(String(50))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EmailLog(Base):
    __tablename__ = "email_logs"
    id = Column(Integer, primary_key=True, index=True)
    to_email = Column(String(200), nullable=False)
    subject = Column(String(200))
    template = Column(String(100))
    reference_type = Column(String(50))
    reference_id = Column(Integer)
    status = Column(String(20), default="sent")
    error = Column(Text)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class SmsTemplate(Base):
    __tablename__ = "sms_templates"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    body = Column(Text)
    event_type = Column(String(50))
    is_active = Column(Boolean, default=True)

class SmsLog(Base):
    __tablename__ = "sms_logs"
    id = Column(Integer, primary_key=True, index=True)
    to_phone = Column(String(20), nullable=False)
    body = Column(Text)
    reference_type = Column(String(50))
    reference_id = Column(Integer)
    status = Column(String(20), default="sent")
    error = Column(Text)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class PushSubscription(Base):
    __tablename__ = "push_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform = Column(String(20))
    token = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PushNotification(Base):
    __tablename__ = "push_notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200))
    body = Column(Text)
    data = Column(Text)
    is_read = Column(Boolean, default=False)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())
