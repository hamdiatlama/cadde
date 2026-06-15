from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text, Date
from sqlalchemy.dialects.postgresql import JSON
from src.database import Base


class PropertyGroup(Base):
    __tablename__ = "property_groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    logo_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PropertyGroupMember(Base):
    __tablename__ = "property_group_members"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("property_groups.id"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    role = Column(String(50), nullable=False)
    is_primary = Column(Boolean, default=False)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyGroupInvite(Base):
    __tablename__ = "property_group_invites"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("property_groups.id"), nullable=False)
    email = Column(String(200), nullable=False)
    role = Column(String(50), nullable=False)
    token = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default="pending")
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)


class GroupConsolidatedReport(Base):
    __tablename__ = "group_consolidated_reports"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("property_groups.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    total_revenue = Column(Float, default=0)
    total_bookings = Column(Integer, default=0)
    avg_occupancy = Column(Float, default=0)
    avg_revpar = Column(Float, default=0)
    total_hotels = Column(Integer, default=0)
    report_data = Column(JSON)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
