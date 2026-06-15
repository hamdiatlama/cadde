from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payout.models import Payout, PayoutBatch
from src.models.order import Order
from src.modules.escrow.models import EscrowTransaction


class PayoutRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_seller_earnings(self, seller_id: int, days: int = 30):
        since = datetime.now(timezone.utc) - timedelta(days=days)
        r = await self.db.execute(
            select(func.coalesce(func.sum(Order.total), 0))
            .where(Order.seller_id == seller_id, Order.status == "delivered", Order.created_at >= since)
        )
        total_sales = r.scalar()
        r = await self.db.execute(
            select(func.coalesce(func.sum(EscrowTransaction.seller_amount), 0))
            .where(EscrowTransaction.seller_id == seller_id, EscrowTransaction.status == "held")
        )
        pending = r.scalar()
        r = await self.db.execute(
            select(func.coalesce(func.sum(EscrowTransaction.seller_amount), 0))
            .where(EscrowTransaction.seller_id == seller_id, EscrowTransaction.status == "released",
                   EscrowTransaction.released_at >= since)
        )
        released = r.scalar()
        return {"total_sales_30d": round(float(total_sales), 2),
                "pending_escrow": round(float(pending), 2),
                "released_30d": round(float(released), 2)}

    async def create_batch(self, **kwargs) -> PayoutBatch:
        b = PayoutBatch(**kwargs)
        self.db.add(b)
        return b

    async def create_payout(self, **kwargs) -> Payout:
        p = Payout(**kwargs)
        self.db.add(p)
        return p

    async def list_payouts(self, seller_id: int):
        r = await self.db.execute(
            select(Payout).where(Payout.seller_id == seller_id).order_by(Payout.created_at.desc())
        )
        return r.scalars().all()

    async def get_batch(self, batch_id: int):
        r = await self.db.execute(select(PayoutBatch).where(PayoutBatch.id == batch_id))
        return r.scalar_one_or_none()

    async def mark_paid(self, payout_id: int, payment_ref: str = None):
        p = await self.db.execute(select(Payout).where(Payout.id == payout_id))
        p = p.scalar_one_or_none()
        if p:
            p.status = "paid"
            p.paid_at = datetime.now(timezone.utc)
            if payment_ref:
                p.payment_ref = payment_ref
