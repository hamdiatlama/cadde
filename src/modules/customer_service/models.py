from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base

class HelpArticle(Base):
    __tablename__ = "help_articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text)
    category = Column(String(50))
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ForumTopic(Base):
    __tablename__ = "forum_topics"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    view_count = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ForumPost(Base):
    __tablename__ = "forum_posts"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("forum_topics.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class KycDocument(Base):
    __tablename__ = "kyc_documents"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doc_type = Column(String(50))
    doc_number = Column(String(100))
    file_url = Column(String(500))
    status = Column(String(20), default="pending")
    verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CoBrowsingSession(Base):
    __tablename__ = "co_browsing_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"))
    session_token = Column(String(200))
    status = Column(String(20), default="active")
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
