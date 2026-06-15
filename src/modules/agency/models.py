from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from src.database import Base


class Agency(Base):
    __tablename__ = "agencies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(200), nullable=False)
    trade_name = Column(String(200))
    tax_id = Column(String(50))
    tax_office = Column(String(100))
    phone = Column(String(20))
    email = Column(String(200))
    website = Column(String(200))
    address = Column(Text)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AgencyAuthorization(Base):
    __tablename__ = "agency_authorizations"
    id = Column(Integer, primary_key=True, index=True)
    agency_id = Column(Integer, ForeignKey("agencies.id"), nullable=False)
    domain = Column(String(50), nullable=False)
    provider_id = Column(Integer, nullable=False)
    provider_name = Column(String(200))
    commission_split = Column(Float, default=0)
    status = Column(String(20), default="pending")
    authorized_by = Column(Integer, ForeignKey("users.id"))
    authorized_at = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    notes = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
