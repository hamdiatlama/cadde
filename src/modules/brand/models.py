from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from src.database import Base


class Brand(Base):
    __tablename__ = "brands"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trademark_no = Column(String(100))
    is_verified = Column(Boolean, default=False)
    logo_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
