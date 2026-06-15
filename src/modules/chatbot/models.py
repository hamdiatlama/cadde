from sqlalchemy import Column, Integer, String, DateTime, func, Text
from src.database import Base


class ChatbotIntent(Base):
    __tablename__ = "chatbot_intents"
    id = Column(Integer, primary_key=True, index=True)
    intent = Column(String(100), nullable=False)
    keywords = Column(Text)
    response = Column(Text, nullable=False)


class ChatbotConversation(Base):
    __tablename__ = "chatbot_conversations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
