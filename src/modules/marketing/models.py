from sqlalchemy import Column, Integer, String, Float, Text, Boolean, DateTime, func, ForeignKey
from src.database import Base


class EmailCampaign(Base):
    __tablename__ = "email_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(200))
    subject = Column(String(200))
    body = Column(Text)
    audience_segment = Column(String(100))
    sent_count = Column(Integer, default=0)
    open_count = Column(Integer, default=0)
    click_count = Column(Integer, default=0)
    status = Column(String(20), default="draft")
    scheduled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SmsCampaign(Base):
    __tablename__ = "sms_campaigns"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    audience_count = Column(Integer, default=0)
    status = Column(String(20), default="draft")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Affiliate(Base):
    __tablename__ = "affiliates"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    referral_code = Column(String(50), unique=True, nullable=False)
    commission_rate = Column(Float, default=5.0)
    total_earnings = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AffiliateClick(Base):
    __tablename__ = "affiliate_clicks"
    id = Column(Integer, primary_key=True, index=True)
    affiliate_id = Column(Integer, ForeignKey("affiliates.id"), nullable=False)
    clicked_by = Column(Integer, ForeignKey("users.id"))
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AffiliateSale(Base):
    __tablename__ = "affiliate_sales"
    id = Column(Integer, primary_key=True, index=True)
    affiliate_id = Column(Integer, ForeignKey("affiliates.id"), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    commission = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    content = Column(Text)
    excerpt = Column(String(500))
    image_url = Column(String(500))
    tags = Column(String(500))
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    published_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CustomerSegment(Base):
    __tablename__ = "customer_segments"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(100), nullable=False)
    criteria = Column(Text)
    member_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
