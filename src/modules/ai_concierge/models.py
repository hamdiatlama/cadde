from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, Text, ForeignKey, JSON
from src.database import Base


class ConciergeConfig(Base):
    __tablename__ = "concierge_configs"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), unique=True, nullable=False)
    is_active = Column(Boolean, default=False)
    language = Column(String(10), default="tr")
    greeting_message = Column(Text)
    operating_hours_start = Column(String(5), default="00:00")
    operating_hours_end = Column(String(5), default="23:59")
    auto_respond = Column(Boolean, default=True)
    escalation_threshold = Column(Integer, default=3)
    whatsapp_enabled = Column(Boolean, default=False)
    whatsapp_number = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class ConciergeIntent(Base):
    __tablename__ = "concierge_intents"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    intent_key = Column(String(100), nullable=False)
    trigger_phrases = Column(JSON)
    response_template = Column(Text)
    requires_human = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConciergeConversation(Base):
    __tablename__ = "concierge_conversations"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"))
    guest_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    channel = Column(String(20), default="in_app")
    status = Column(String(20), default="active")
    started_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConciergeMessage(Base):
    __tablename__ = "concierge_messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("concierge_conversations.id"), nullable=False)
    sender_type = Column(String(20), default="guest")
    message = Column(Text, nullable=False)
    intent_matched = Column(String(100))
    is_auto_response = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ConciergeKnowledgeBase(Base):
    __tablename__ = "concierge_knowledge_base"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    category = Column(String(50))
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AutomatedMessageSequence(Base):
    __tablename__ = "automated_message_sequences"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    trigger_event = Column(String(50), nullable=False)
    delay_hours = Column(Integer)
    message_template = Column(Text, nullable=False)
    channel = Column(String(20), default="in_app")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
