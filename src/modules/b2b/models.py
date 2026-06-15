from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey
from src.database import Base


class B2bPriceTier(Base):
    __tablename__ = "b2b_price_tiers"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    min_qty = Column(Integer, nullable=False)
    max_qty = Column(Integer)
    unit_price = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class B2bCustomer(Base):
    __tablename__ = "b2b_customers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(200))
    tax_office = Column(String(100))
    tax_number = Column(String(50))
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class B2bQuote(Base):
    __tablename__ = "b2b_quotes"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("b2b_customers.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String(20), default="pending")
    total_amount = Column(Float)
    notes = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))


class B2bQuoteItem(Base):
    __tablename__ = "b2b_quote_items"
    id = Column(Integer, primary_key=True, index=True)
    quote_id = Column(Integer, ForeignKey("b2b_quotes.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
