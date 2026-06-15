from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class HotelWebsite(Base):
    __tablename__ = "hotel_websites"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), unique=True, nullable=False)
    domain = Column(String(200), unique=True, nullable=True)
    subdomain = Column(String(200), unique=True, nullable=False)
    template_id = Column(String(50), default="default")
    primary_color = Column(String(7), default="#4A7FD4")
    secondary_color = Column(String(7), default="#EEF4FF")
    font_family = Column(String(100), default="Space Grotesk")
    logo_url = Column(String(500))
    hero_image_url = Column(String(500))
    about_text = Column(Text)
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WebsitePage(Base):
    __tablename__ = "website_pages"
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("hotel_websites.id"), nullable=False)
    slug = Column(String(200), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class WebsiteSEO(Base):
    __tablename__ = "website_seo"
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("hotel_websites.id"), nullable=False)
    page_id = Column(Integer, ForeignKey("website_pages.id"), nullable=True)
    meta_title = Column(String(200))
    meta_description = Column(String(500))
    meta_keywords = Column(String(500))
    og_image_url = Column(String(500))
    canonical_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class WebsiteBookingWidget(Base):
    __tablename__ = "website_booking_widgets"
    id = Column(Integer, primary_key=True, index=True)
    website_id = Column(Integer, ForeignKey("hotel_websites.id"), nullable=False)
    widget_type = Column(String(50), nullable=False)
    is_enabled = Column(Boolean, default=True)
    embed_code = Column(Text)
    custom_css = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
