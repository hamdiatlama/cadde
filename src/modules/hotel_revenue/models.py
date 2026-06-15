from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, JSON, Date
from src.database import Base


class HotelRevenueRule(Base):
    __tablename__ = "hotel_revenue_rules"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    rule_type = Column(String(50))
    name = Column(String(200), nullable=False)
    is_active = Column(Boolean, default=True)
    priority = Column(Integer, default=0)
    conditions = Column(JSON)
    adjustment_type = Column(String(20))
    adjustment_value = Column(Float)
    min_stay = Column(Integer)
    max_stay = Column(Integer)
    advance_days_min = Column(Integer)
    advance_days_max = Column(Integer)
    occupancy_threshold = Column(Float)
    day_of_week = Column(String(50))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HotelDailyRate(Base):
    __tablename__ = "hotel_daily_rates"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=False)
    date = Column(Date, nullable=False)
    base_price = Column(Float)
    dynamic_price = Column(Float)
    final_price = Column(Float)
    occupancy_rate = Column(Float, default=0)
    is_boosted = Column(Boolean, default=False)
    is_sale = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class HotelRevenueReport(Base):
    __tablename__ = "hotel_revenue_reports"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    report_date = Column(Date)
    revpar = Column(Float)
    adr = Column(Float)
    occupancy_rate = Column(Float)
    total_revenue = Column(Float)
    room_revenue = Column(Float)
    ancillary_revenue = Column(Float)
    booked_rooms = Column(Integer)
    available_rooms = Column(Integer)
    cancellation_rate = Column(Float)
    avg_length_of_stay = Column(Float)
    report_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
