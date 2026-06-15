from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.live_shopping.models import LiveStream, LiveStreamProduct, LiveStreamOrder


class LiveShoppingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_stream(self, seller_id: int, title: str, stream_url: str = None, thumbnail_url: str = None, scheduled_at=None) -> LiveStream:
        s = LiveStream(seller_id=seller_id, title=title, stream_url=stream_url, thumbnail_url=thumbnail_url, scheduled_at=scheduled_at)
        self.db.add(s)
        return s

    async def list_active(self):
        r = await self.db.execute(
            select(LiveStream).where(LiveStream.status.in_(["live", "scheduled"])).order_by(LiveStream.scheduled_at.desc())
        )
        return r.scalars().all()

    async def get_stream(self, stream_id: int):
        r = await self.db.execute(select(LiveStream).where(LiveStream.id == stream_id))
        return r.scalar_one_or_none()

    async def add_product(self, stream_id: int, product_id: int, discount_rate: float = 0, sort_order: int = 0):
        existing = await self.db.execute(
            select(LiveStreamProduct).where(LiveStreamProduct.stream_id == stream_id, LiveStreamProduct.product_id == product_id)
        )
        if existing.scalar_one_or_none():
            return None
        lp = LiveStreamProduct(stream_id=stream_id, product_id=product_id, discount_rate=discount_rate, sort_order=sort_order)
        self.db.add(lp)
        return lp

    async def remove_product(self, stream_id: int, product_id: int):
        await self.db.execute(
            delete(LiveStreamProduct).where(LiveStreamProduct.stream_id == stream_id, LiveStreamProduct.product_id == product_id)
        )

    async def get_stream_orders(self, stream_id: int):
        r = await self.db.execute(
            select(LiveStreamOrder).where(LiveStreamOrder.stream_id == stream_id).order_by(LiveStreamOrder.created_at.desc())
        )
        return r.scalars().all()

    async def record_order(self, stream_id: int, order_id: int):
        lo = LiveStreamOrder(stream_id=stream_id, order_id=order_id)
        self.db.add(lo)
        return lo
