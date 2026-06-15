from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payment_gateway.models import (
    PaymentProvider, MerchantAccount, PaymentTransaction,
    PayoutRequest, PayoutHistory,
)


class PaymentProviderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> PaymentProvider:
        obj = PaymentProvider(**kwargs)
        self.db.add(obj)
        return obj

    async def get(self, provider_id: int) -> PaymentProvider | None:
        r = await self.db.execute(select(PaymentProvider).where(PaymentProvider.id == provider_id))
        return r.scalar_one_or_none()

    async def get_by_code(self, code: str) -> PaymentProvider | None:
        r = await self.db.execute(select(PaymentProvider).where(PaymentProvider.code == code))
        return r.scalar_one_or_none()

    async def list_active(self):
        r = await self.db.execute(
            select(PaymentProvider).where(PaymentProvider.is_active == True)
            .order_by(PaymentProvider.id)
        )
        return list(r.scalars().all())

    async def list_all(self):
        r = await self.db.execute(select(PaymentProvider).order_by(PaymentProvider.id))
        return list(r.scalars().all())


class MerchantAccountRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> MerchantAccount:
        obj = MerchantAccount(**kwargs)
        self.db.add(obj)
        return obj

    async def get(self, account_id: int) -> MerchantAccount | None:
        r = await self.db.execute(select(MerchantAccount).where(MerchantAccount.id == account_id))
        return r.scalar_one_or_none()

    async def get_by_hotel(self, hotel_id: int):
        r = await self.db.execute(
            select(MerchantAccount).where(MerchantAccount.hotel_id == hotel_id)
            .order_by(MerchantAccount.created_at.desc())
        )
        return list(r.scalars().all())

    async def get_active_by_hotel(self, hotel_id: int):
        r = await self.db.execute(
            select(MerchantAccount).where(
                MerchantAccount.hotel_id == hotel_id,
                MerchantAccount.is_active == True,
                MerchantAccount.is_verified == True,
            )
        )
        return r.scalar_one_or_none()

    async def update(self, account_id: int, **kwargs) -> MerchantAccount | None:
        obj = await self.get(account_id)
        if not obj:
            return None
        for field, val in kwargs.items():
            setattr(obj, field, val)
        obj.updated_at = datetime.now(timezone.utc)
        self.db.add(obj)
        return obj


class PaymentTransactionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> PaymentTransaction:
        obj = PaymentTransaction(**kwargs)
        self.db.add(obj)
        return obj

    async def get(self, txn_id: int) -> PaymentTransaction | None:
        r = await self.db.execute(select(PaymentTransaction).where(PaymentTransaction.id == txn_id))
        return r.scalar_one_or_none()

    async def get_by_reference(self, ref_no: str) -> PaymentTransaction | None:
        r = await self.db.execute(select(PaymentTransaction).where(PaymentTransaction.reference_no == ref_no))
        return r.scalar_one_or_none()

    async def list(self, booking_id: int = None, hotel_id: int = None, status: str = None):
        query = select(PaymentTransaction)
        if booking_id is not None:
            query = query.where(PaymentTransaction.booking_id == booking_id)
        if status is not None:
            query = query.where(PaymentTransaction.status == status)
        query = query.order_by(PaymentTransaction.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def update_status(self, txn_id: int, status: str, **extra) -> PaymentTransaction | None:
        obj = await self.get(txn_id)
        if not obj:
            return None
        obj.status = status
        for field, val in extra.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def get_hotel_transactions(self, hotel_id: int, status: str = None):
        from src.modules.hotel.models import Booking
        query = select(PaymentTransaction).join(Booking, PaymentTransaction.booking_id == Booking.id)
        if status is not None:
            query = query.where(PaymentTransaction.status == status)
        query = query.where(Booking.hotel_id == hotel_id)
        query = query.order_by(PaymentTransaction.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def get_hotel_aggregates(self, hotel_id: int):
        from src.modules.hotel.models import Booking
        total_q = select(func.coalesce(func.sum(PaymentTransaction.amount), 0)).join(
            Booking, PaymentTransaction.booking_id == Booking.id
        ).where(Booking.hotel_id == hotel_id, PaymentTransaction.status == "success")
        total = (await self.db.execute(total_q)).scalar()

        pending_q = select(func.coalesce(func.sum(PaymentTransaction.amount), 0)).join(
            Booking, PaymentTransaction.booking_id == Booking.id
        ).where(Booking.hotel_id == hotel_id, PaymentTransaction.status == "pending")
        pending = (await self.db.execute(pending_q)).scalar()

        fee_q = select(func.coalesce(func.sum(PaymentTransaction.fee), 0)).join(
            Booking, PaymentTransaction.booking_id == Booking.id
        ).where(Booking.hotel_id == hotel_id, PaymentTransaction.status == "success")
        fees = (await self.db.execute(fee_q)).scalar()

        paid_q = select(func.coalesce(func.sum(PayoutRequest.amount), 0)).where(
            PayoutRequest.hotel_id == hotel_id,
            PayoutRequest.status.in_(["processing", "completed"]),
        )
        paid = (await self.db.execute(paid_q)).scalar()

        return {
            "total_earned": round(float(total), 2),
            "pending": round(float(pending), 2),
            "total_fees": round(float(fees), 2),
            "paid_out": round(float(paid), 2),
            "net_balance": round(float(total) - float(pending) - float(paid), 2),
        }

    async def get_report(self, hotel_id: int, date_from, date_to):
        from src.modules.hotel.models import Booking
        query = select(
            func.date(PaymentTransaction.created_at),
            func.count(PaymentTransaction.id),
            func.coalesce(func.sum(PaymentTransaction.amount), 0),
            func.coalesce(func.sum(PaymentTransaction.fee), 0),
            func.coalesce(func.sum(PaymentTransaction.net_amount), 0),
        ).join(Booking, PaymentTransaction.booking_id == Booking.id).where(
            Booking.hotel_id == hotel_id,
            PaymentTransaction.status == "success",
            PaymentTransaction.created_at >= date_from,
            PaymentTransaction.created_at <= date_to,
        ).group_by(func.date(PaymentTransaction.created_at)).order_by(func.date(PaymentTransaction.created_at))
        r = await self.db.execute(query)
        rows = r.all()
        return [
            {
                "date": str(row[0]),
                "transaction_count": row[1],
                "amount": round(float(row[2]), 2),
                "fee": round(float(row[3]), 2),
                "net": round(float(row[4]), 2),
            }
            for row in rows
        ]


class PayoutRequestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> PayoutRequest:
        obj = PayoutRequest(**kwargs)
        self.db.add(obj)
        return obj

    async def get(self, payout_id: int) -> PayoutRequest | None:
        r = await self.db.execute(select(PayoutRequest).where(PayoutRequest.id == payout_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int):
        r = await self.db.execute(
            select(PayoutRequest).where(PayoutRequest.hotel_id == hotel_id)
            .order_by(PayoutRequest.created_at.desc())
        )
        return list(r.scalars().all())

    async def update_status(self, payout_id: int, status: str, **extra) -> PayoutRequest | None:
        obj = await self.get(payout_id)
        if not obj:
            return None
        obj.status = status
        for field, val in extra.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj


class PayoutHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, **kwargs) -> PayoutHistory:
        obj = PayoutHistory(**kwargs)
        self.db.add(obj)
        return obj

    async def list_by_hotel(self, hotel_id: int):
        r = await self.db.execute(
            select(PayoutHistory).where(PayoutHistory.hotel_id == hotel_id)
            .order_by(PayoutHistory.created_at.desc())
        )
        return list(r.scalars().all())
