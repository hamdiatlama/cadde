from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, func, ForeignKey
from sqlalchemy.dialects.sqlite import JSON
from src.database import Base


class PaymentProvider(Base):
    __tablename__ = "payment_providers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    supported_currencies = Column(String(200), default="TRY,USD,EUR")
    fee_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MerchantAccount(Base):
    __tablename__ = "merchant_accounts"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    provider_id = Column(Integer, ForeignKey("payment_providers.id"), nullable=False)
    api_key = Column(Text)
    api_secret = Column(Text)
    merchant_id = Column(String(100))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id"), nullable=False)
    merchant_account_id = Column(Integer, ForeignKey("merchant_accounts.id"), nullable=False)
    transaction_id = Column(String(200))
    reference_no = Column(String(100), unique=True, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="TRY")
    fee = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    payment_method = Column(String(50))
    card_last_four = Column(String(4))
    installment = Column(Integer, default=1)
    paid_at = Column(DateTime(timezone=True))
    refunded_at = Column(DateTime(timezone=True))
    raw_response = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PayoutRequest(Base):
    __tablename__ = "payout_requests"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    status = Column(String(20), default="pending")
    account_holder = Column(String(200))
    iban = Column(String(50))
    bank_name = Column(String(100))
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PayoutHistory(Base):
    __tablename__ = "payout_histories"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    payout_request_id = Column(Integer, ForeignKey("payout_requests.id"), nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float, default=0.0)
    net_amount = Column(Float, nullable=False)
    status = Column(String(20))
    external_payout_id = Column(String(200))
    processed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
