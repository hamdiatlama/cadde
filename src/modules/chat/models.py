from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, func, ForeignKey, Enum as SAEnum
from src.database import Base
import enum


class ChatStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(50), index=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(50), primary_key=True)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"))
    order_id = Column(Integer)
    status = Column(SAEnum(ChatStatus), default=ChatStatus.OPEN)
    last_message_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
