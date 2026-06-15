from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Text
from src.database import Base


class TaxRateAddress(Base):
    __tablename__ = "tax_rate_addresses"
    id = Column(Integer, primary_key=True, index=True)
    country = Column(String(2), nullable=False)
    state = Column(String(100))
    city = Column(String(100))
    rate = Column(Float, nullable=False)
    tax_type = Column(String(20), default="vat")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class GibInvoice(Base):
    __tablename__ = "gib_invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    gib_id = Column(String(100))
    invoice_no = Column(String(50), unique=True)
    status = Column(String(20), default="draft")
    xml_content = Column(Text)
    qr_code = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InternationalDocument(Base):
    __tablename__ = "international_documents"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    doc_type = Column(String(50))
    doc_number = Column(String(100))
    file_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
