from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.handmade.models import CustomOrder


class HandmadeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, buyer_id: int, seller_id: int, description: str, requirements: str = None, product_id: int = None, estimated_days: int = None) -> CustomOrder:
        o = CustomOrder(buyer_id=buyer_id, seller_id=seller_id, description=description, requirements=requirements, product_id=product_id, estimated_days=estimated_days)
        self.db.add(o)
        return o

    async def get_order(self, order_id: int):
        r = await self.db.execute(select(CustomOrder).where(CustomOrder.id == order_id))
        return r.scalar_one_or_none()

    async def list_by_buyer(self, buyer_id: int):
        r = await self.db.execute(
            select(CustomOrder).where(CustomOrder.buyer_id == buyer_id).order_by(CustomOrder.created_at.desc())
        )
        return r.scalars().all()

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(CustomOrder).where(CustomOrder.seller_id == seller_id).order_by(CustomOrder.created_at.desc())
        )
        return r.scalars().all()

    async def update_status(self, order_id: int, status: str):
        o = await self.get_order(order_id)
        if not o:
            return None
        o.status = status
        return o
