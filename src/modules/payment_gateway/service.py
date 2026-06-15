import uuid
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payment_gateway.repository import (
    PaymentProviderRepository, MerchantAccountRepository,
    PaymentTransactionRepository, PayoutRequestRepository, PayoutHistoryRepository,
)


class PaymentGatewayService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.providers = PaymentProviderRepository(db)
        self.merchants = MerchantAccountRepository(db)
        self.transactions = PaymentTransactionRepository(db)
        self.payouts = PayoutRequestRepository(db)
        self.payout_history = PayoutHistoryRepository(db)

    async def list_providers(self):
        providers = await self.providers.list_all()
        return [
            {
                "id": p.id, "name": p.name, "code": p.code,
                "is_active": p.is_active,
                "supported_currencies": p.supported_currencies,
                "fee_percentage": p.fee_percentage,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in providers
        ]

    async def create_merchant_account(self, hotel_id: int, provider_id: int, **kwargs):
        existing = await self.merchants.get_active_by_hotel(hotel_id)
        if existing and existing.provider_id == provider_id:
            return None, "Merchant account already exists for this provider"
        merchant = await self.merchants.create(
            hotel_id=hotel_id, provider_id=provider_id, **kwargs
        )
        await self.db.flush()
        return {
            "id": merchant.id, "hotel_id": merchant.hotel_id,
            "provider_id": merchant.provider_id,
            "merchant_id": merchant.merchant_id,
            "is_verified": merchant.is_verified,
            "is_active": merchant.is_active,
            "created_at": merchant.created_at.isoformat() if merchant.created_at else None,
        }, None

    async def get_merchant_accounts(self, hotel_id: int):
        accounts = await self.merchants.get_by_hotel(hotel_id)
        return [
            {
                "id": a.id, "hotel_id": a.hotel_id,
                "provider_id": a.provider_id,
                "merchant_id": a.merchant_id,
                "is_verified": a.is_verified,
                "is_active": a.is_active,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in accounts
        ]

    async def process_payment(self, booking_id: int, amount: float, currency: str,
                              payment_method: str, card_info: dict = None,
                              merchant_account_id: int = None):
        ref_no = f"PAY-{uuid.uuid4().hex[:12].upper()}"
        fee = round(amount * 0.036, 2)
        net_amount = round(amount - fee, 2)
        card_last_four = None
        installment = 1
        if card_info:
            card_last_four = card_info.get("card_number", "")[-4:] if card_info.get("card_number") else None
            installment = card_info.get("installment", 1)
        txn = await self.transactions.create(
            booking_id=booking_id,
            merchant_account_id=merchant_account_id,
            transaction_id=f"TXN-{uuid.uuid4().hex[:16].upper()}",
            reference_no=ref_no,
            amount=amount,
            currency=currency,
            fee=fee,
            net_amount=net_amount,
            status="pending",
            payment_method=payment_method,
            card_last_four=card_last_four,
            installment=installment,
        )
        await self.db.flush()
        return {
            "id": txn.id, "reference_no": txn.reference_no,
            "transaction_id": txn.transaction_id,
            "amount": txn.amount, "currency": txn.currency,
            "fee": txn.fee, "net_amount": txn.net_amount,
            "status": txn.status, "payment_method": txn.payment_method,
        }

    async def complete_payment(self, reference_no: str):
        txn = await self.transactions.get_by_reference(reference_no)
        if not txn:
            return None, "Transaction not found"
        if txn.status != "pending":
            return None, f"Transaction already {txn.status}"
        txn.status = "success"
        txn.paid_at = datetime.now(timezone.utc)
        self.db.add(txn)
        return {"id": txn.id, "reference_no": txn.reference_no, "status": txn.status}, None

    async def process_refund(self, transaction_id: int):
        txn = await self.transactions.get(transaction_id)
        if not txn:
            return None, "Transaction not found"
        if txn.status != "success":
            return None, f"Cannot refund transaction with status '{txn.status}'"
        txn.status = "refunded"
        txn.refunded_at = datetime.now(timezone.utc)
        self.db.add(txn)
        return {
            "id": txn.id, "reference_no": txn.reference_no,
            "amount": txn.amount, "status": txn.status,
            "refunded_at": txn.refunded_at.isoformat() if txn.refunded_at else None,
        }, None

    async def list_transactions(self, booking_id: int = None, hotel_id: int = None, status: str = None):
        if hotel_id:
            txns = await self.transactions.get_hotel_transactions(hotel_id, status)
        else:
            txns = await self.transactions.list(booking_id=booking_id, status=status)
        return [
            {
                "id": t.id, "booking_id": t.booking_id,
                "transaction_id": t.transaction_id,
                "reference_no": t.reference_no,
                "amount": t.amount, "currency": t.currency,
                "fee": t.fee, "net_amount": t.net_amount,
                "status": t.status, "payment_method": t.payment_method,
                "card_last_four": t.card_last_four,
                "installment": t.installment,
                "paid_at": t.paid_at.isoformat() if t.paid_at else None,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in txns
        ]

    async def request_payout(self, hotel_id: int, amount: float, iban: str,
                             account_holder: str = None, bank_name: str = None):
        balance = await self.get_hotel_balance(hotel_id)
        if amount > balance["net_balance"]:
            return None, f"Insufficient balance. Available: {balance['net_balance']}"
        fee = round(amount * 0.02, 2)
        net_amount = round(amount - fee, 2)
        payout = await self.payouts.create(
            hotel_id=hotel_id, amount=amount, fee=fee,
            net_amount=net_amount, status="pending",
            account_holder=account_holder, iban=iban, bank_name=bank_name,
            requested_at=datetime.now(timezone.utc),
        )
        await self.db.flush()
        return {
            "id": payout.id, "hotel_id": payout.hotel_id,
            "amount": payout.amount, "fee": payout.fee,
            "net_amount": payout.net_amount, "status": payout.status,
            "iban": payout.iban, "bank_name": payout.bank_name,
            "requested_at": payout.requested_at.isoformat() if payout.requested_at else None,
        }, None

    async def list_payouts(self, hotel_id: int):
        payouts = await self.payouts.list_by_hotel(hotel_id)
        return [
            {
                "id": p.id, "hotel_id": p.hotel_id,
                "amount": p.amount, "fee": p.fee,
                "net_amount": p.net_amount, "status": p.status,
                "account_holder": p.account_holder,
                "iban": p.iban, "bank_name": p.bank_name,
                "notes": p.notes,
                "requested_at": p.requested_at.isoformat() if p.requested_at else None,
                "completed_at": p.completed_at.isoformat() if p.completed_at else None,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in payouts
        ]

    async def get_hotel_balance(self, hotel_id: int):
        return await self.transactions.get_hotel_aggregates(hotel_id)

    async def get_transaction_report(self, hotel_id: int, date_from, date_to):
        return await self.transactions.get_report(hotel_id, date_from, date_to)
