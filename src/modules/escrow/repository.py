from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.escrow.models import EscrowTransaction, Dispute
from src.models.order import Order


class EscrowRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_escrow(self, **kwargs) -> EscrowTransaction:
        e = EscrowTransaction(**kwargs)
        self.db.add(e)
        return e

    async def get_escrow(self, escrow_id: int):
        r = await self.db.execute(select(EscrowTransaction).where(EscrowTransaction.id == escrow_id))
        return r.scalar_one_or_none()

    async def get_by_order(self, order_id: int):
        r = await self.db.execute(select(EscrowTransaction).where(EscrowTransaction.order_id == order_id))
        return r.scalar_one_or_none()

    async def release_escrow(self, escrow_id: int, released_by: str = "system"):
        from datetime import datetime, timezone
        e = await self.get_escrow(escrow_id)
        if e:
            e.status = "released"
            e.released_at = datetime.now(timezone.utc)
            e.released_by = released_by

    async def refund_escrow(self, escrow_id: int):
        e = await self.get_escrow(escrow_id)
        if e:
            e.status = "refunded"

    async def list_seller_holds(self, seller_id: int):
        r = await self.db.execute(
            select(EscrowTransaction).where(EscrowTransaction.seller_id == seller_id, EscrowTransaction.status == "held")
        )
        return r.scalars().all()

    async def create_dispute(self, **kwargs) -> Dispute:
        d = Dispute(**kwargs)
        self.db.add(d)
        return d

    async def get_dispute(self, dispute_id: int):
        r = await self.db.execute(select(Dispute).where(Dispute.id == dispute_id))
        return r.scalar_one_or_none()

    async def list_order_disputes(self, order_id: int):
        r = await self.db.execute(select(Dispute).where(Dispute.order_id == order_id).order_by(Dispute.created_at.desc()))
        return r.scalars().all()

    async def resolve_dispute(self, dispute_id: int, resolution: str, resolved_by: int):
        from datetime import datetime, timezone
        d = await self.get_dispute(dispute_id)
        if d:
            d.status = "resolved"
            d.resolution = resolution
            d.resolved_by = resolved_by
            d.resolved_at = datetime.now(timezone.utc)

    async def get_order(self, order_id: int):
        r = await self.db.execute(select(Order).where(Order.id == order_id))
        return r.scalar_one_or_none()
