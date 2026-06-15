from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text, JSON, Date
from src.database import Base


class UpsellOffer(Base):
    __tablename__ = "upsell_offers"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    is_active = Column(Boolean, default=True)
    is_auto_offer = Column(Boolean, default=False)
    trigger_event = Column(String(50), nullable=True)
    display_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UpsellBookingItem(Base):
    __tablename__ = "upsell_booking_items"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    offer_id = Column(Integer, ForeignKey("upsell_offers.id"), nullable=False)
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    confirmed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class UpsellCampaign(Base):
    __tablename__ = "upsell_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    rules = Column(JSON)
    discount_percentage = Column(Float)
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AncillaryRevenueReport(Base):
    __tablename__ = "ancillary_revenue_reports"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    total_upsell_revenue = Column(Float, default=0)
    total_orders = Column(Integer, default=0)
    breakdown = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
