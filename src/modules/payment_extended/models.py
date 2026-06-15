from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, func, ForeignKey, Enum as SAEnum
from src.database import Base
import enum

class PaymentMethodType(str, enum.Enum):
    CARD = "card"
    COD = "cod"
    BNPL = "bnpl"
    CRYPTO = "crypto"
    INSTALLMENT = "installment"
    WALLET = "wallet"

class CodOrder(Base):
    __tablename__ = "cod_orders"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    status = Column(String(20), default="pending")
    collected_amount = Column(Float)
    collected_at = Column(DateTime(timezone=True))

class BnplInstallment(Base):
    __tablename__ = "bnpl_installments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    installment_count = Column(Integer, nullable=False)
    installment_amount = Column(Float, nullable=False)
    status = Column(String(20), default="active")
    next_payment_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CryptoPayment(Base):
    __tablename__ = "crypto_payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    currency = Column(String(10), nullable=False)
    wallet_address = Column(String(200))
    amount = Column(Float, nullable=False)
    tx_hash = Column(String(200))
    status = Column(String(20), default="pending")
    confirmations = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Wallet(Base):
    __tablename__ = "wallets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    balance = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    id = Column(Integer, primary_key=True, index=True)
    wallet_id = Column(Integer, ForeignKey("wallets.id"), nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String(20), nullable=False)
    reference_id = Column(Integer)
    reference_type = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
