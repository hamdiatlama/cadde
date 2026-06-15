from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Enum as SAEnum
from src.database import Base
import enum


class TaxType(str, enum.Enum):
    KDV = "kdv"
    STOPAJ = "stopaj"
    GELIR_VERGISI = "gelir_vergisi"


class TaxRate(Base):
    __tablename__ = "tax_rates"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=True)
    tax_type = Column(SAEnum(TaxType), default=TaxType.KDV)
    rate = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    invoice_no = Column(String(50), unique=True, nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subtotal = Column(Float, nullable=False)
    tax_total = Column(Float, nullable=False)
    grand_total = Column(Float, nullable=False)
    status = Column(String(20), default="draft")
    pdf_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
