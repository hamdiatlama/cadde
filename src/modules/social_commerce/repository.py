from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.social_commerce.models import SocialChannel, SocialProductSync, SocialOrder, ShoppingFeed, AffiliateNetwork


class SocialChannelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def connect(self, seller_id: int, platform: str, access_token: str, refresh_token: str = None, page_id: str = None) -> SocialChannel:
        ch = SocialChannel(seller_id=seller_id, platform=platform, access_token=access_token, refresh_token=refresh_token, page_id=page_id)
        self.db.add(ch)
        return ch

    async def disconnect(self, channel_id: int) -> SocialChannel:
        r = await self.db.execute(select(SocialChannel).where(SocialChannel.id == channel_id))
        ch = r.scalar_one_or_none()
        if ch:
            ch.is_active = False
        return ch

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(select(SocialChannel).where(SocialChannel.seller_id == seller_id))
        return r.scalars().all()

    async def get_token(self, channel_id: int) -> str:
        r = await self.db.execute(select(SocialChannel).where(SocialChannel.id == channel_id))
        ch = r.scalar_one_or_none()
        return ch.access_token if ch else None


class SocialProductSyncRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def sync_product(self, channel_id: int, product_id: int, platform_product_id: str = None) -> SocialProductSync:
        sync = SocialProductSync(channel_id=channel_id, product_id=product_id, platform_product_id=platform_product_id, status="synced", last_synced_at=datetime.now(timezone.utc))
        self.db.add(sync)
        return sync

    async def get_sync_status(self, product_id: int):
        r = await self.db.execute(select(SocialProductSync).where(SocialProductSync.product_id == product_id).order_by(SocialProductSync.created_at.desc()).limit(1))
        return r.scalar_one_or_none()

    async def list_by_channel(self, channel_id: int):
        r = await self.db.execute(select(SocialProductSync).where(SocialProductSync.channel_id == channel_id))
        return r.scalars().all()


class SocialOrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def import_order(self, platform: str, platform_order_id: str, buyer_name: str, buyer_platform_id: str, total: float) -> SocialOrder:
        o = SocialOrder(platform=platform, platform_order_id=platform_order_id, buyer_name=buyer_name, buyer_platform_id=buyer_platform_id, total=total, status="imported")
        self.db.add(o)
        return o

    async def list_by_seller(self, seller_id: int):
        from src.modules.store.models import Order
        r = await self.db.execute(
            select(SocialOrder).join(Order, SocialOrder.order_id == Order.id).where(Order.seller_id == seller_id)
        )
        return r.scalars().all()


class ShoppingFeedRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_feed(self, seller_id: int, feed_type: str) -> ShoppingFeed:
        feed_url = f"/feeds/{seller_id}/{feed_type}.xml"
        feed = ShoppingFeed(seller_id=seller_id, feed_type=feed_type, feed_url=feed_url, product_count=0, last_generated_at=datetime.now(timezone.utc))
        self.db.add(feed)
        return feed

    async def get_feed(self, seller_id: int, feed_type: str = None):
        q = select(ShoppingFeed).where(ShoppingFeed.seller_id == seller_id)
        if feed_type:
            q = q.where(ShoppingFeed.feed_type == feed_type)
        r = await self.db.execute(q.order_by(ShoppingFeed.created_at.desc()).limit(1))
        return r.scalar_one_or_none()


class AffiliateNetworkRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_network(self, name: str, api_key: str, api_url: str) -> AffiliateNetwork:
        net = AffiliateNetwork(name=name, api_key=api_key, api_url=api_url)
        self.db.add(net)
        return net

    async def list_networks(self):
        r = await self.db.execute(select(AffiliateNetwork).where(AffiliateNetwork.is_active == True))
        return r.scalars().all()
