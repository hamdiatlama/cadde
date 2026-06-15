from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200))
    report_type = Column(String(50))
    date_from = Column(DateTime(timezone=True))
    date_to = Column(DateTime(timezone=True))
    config = Column(Text)
    last_generated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SavedDashboard(Base):
    __tablename__ = "saved_dashboards"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200))
    widgets = Column(Text)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RfmSegment(Base):
    __tablename__ = "rfm_segments"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100))
    r_score = Column(Integer)
    f_score = Column(Integer)
    m_score = Column(Integer)
    customer_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
