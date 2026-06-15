from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.fulfillment.models import FulfillmentCenter, FulfillmentRequest


class FulfillmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_center(self, name: str, address: str = None, city: str = None) -> FulfillmentCenter:
        c = FulfillmentCenter(name=name, address=address, city=city)
        self.db.add(c); return c

    async def list_centers(self):
        r = await self.db.execute(select(FulfillmentCenter).where(FulfillmentCenter.is_active == True))
        return r.scalars().all()

    async def create_request(self, seller_id: int, order_id: int) -> FulfillmentRequest:
        fr = FulfillmentRequest(seller_id=seller_id, order_id=order_id)
        self.db.add(fr); return fr

    async def assign_center(self, request_id: int, center_id: int) -> FulfillmentRequest:
        r = await self.db.execute(select(FulfillmentRequest).where(FulfillmentRequest.id == request_id))
        fr = r.scalar_one_or_none()
        if fr:
            fr.center_id = center_id
        return fr

    async def update_status(self, request_id: int, status: str) -> FulfillmentRequest:
        r = await self.db.execute(select(FulfillmentRequest).where(FulfillmentRequest.id == request_id))
        fr = r.scalar_one_or_none()
        if fr:
            fr.status = status
        return fr

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(FulfillmentRequest).where(FulfillmentRequest.seller_id == seller_id)
            .order_by(FulfillmentRequest.created_at.desc())
        )
        return r.scalars().all()

    async def list_by_center(self, center_id: int):
        r = await self.db.execute(
            select(FulfillmentRequest).where(FulfillmentRequest.center_id == center_id)
            .order_by(FulfillmentRequest.created_at.desc())
        )
        return r.scalars().all()
