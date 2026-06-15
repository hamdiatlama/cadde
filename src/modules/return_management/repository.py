from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.return_management.models import ReturnRequest
from src.models.order import Order


class ReturnManagementRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_request(self, user_id: int, order_id: int, reason: str) -> ReturnRequest:
        r = ReturnRequest(user_id=user_id, order_id=order_id, reason=reason)
        self.db.add(r)
        return r

    async def list_by_user(self, user_id: int):
        r = await self.db.execute(
            select(ReturnRequest).where(ReturnRequest.user_id == user_id).order_by(ReturnRequest.created_at.desc())
        )
        return r.scalars().all()

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(ReturnRequest).join(Order, ReturnRequest.order_id == Order.id)
            .where(Order.seller_id == seller_id).order_by(ReturnRequest.created_at.desc())
        )
        return r.scalars().all()

    async def approve_request(self, id: int, refund_amount: float):
        r = await self.get_request(id)
        if not r:
            return None
        r.status = "approved"
        r.refund_amount = refund_amount
        r.resolved_at = datetime.now(timezone.utc)
        return r

    async def reject_request(self, id: int, reason: str):
        r = await self.get_request(id)
        if not r:
            return None
        r.status = "rejected"
        r.notes = reason
        r.resolved_at = datetime.now(timezone.utc)
        return r

    async def get_request(self, id: int):
        r = await self.db.execute(select(ReturnRequest).where(ReturnRequest.id == id))
        return r.scalar_one_or_none()
