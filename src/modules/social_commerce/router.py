from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.social_commerce.repository import (
    SocialChannelRepository, SocialProductSyncRepository,
    SocialOrderRepository, ShoppingFeedRepository, AffiliateNetworkRepository
)

router = APIRouter(prefix="/social-commerce", tags=["social_commerce"])


@router.post("/channels/connect", status_code=201)
async def connect_channel(platform: str, access_token: str, refresh_token: str = None, page_id: str = None,
                          current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SocialChannelRepository(db)
    ch = await repo.connect(current_user.id, platform, access_token, refresh_token, page_id)
    await db.commit()
    return {"id": ch.id, "platform": ch.platform}


@router.get("/channels")
async def list_channels(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SocialChannelRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.post("/channels/{channel_id}/sync-products")
async def sync_products(channel_id: int, product_id: int,
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SocialProductSyncRepository(db)
    sync = await repo.sync_product(channel_id, product_id)
    await db.commit()
    return {"id": sync.id, "status": sync.status}


@router.get("/products/sync-status")
async def get_sync_status(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = SocialProductSyncRepository(db)
    status = await repo.get_sync_status(product_id)
    if not status:
        raise HTTPException(404, "Sync status not found")
    return status


@router.post("/products/feed/generate")
async def generate_feed(feed_type: str = "google_shopping",
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ShoppingFeedRepository(db)
    feed = await repo.generate_feed(current_user.id, feed_type)
    await db.commit()
    return {"id": feed.id, "feed_url": feed.feed_url}


@router.get("/products/feed")
async def get_feed(feed_type: str = None,
                   current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = ShoppingFeedRepository(db)
    feed = await repo.get_feed(current_user.id, feed_type)
    if not feed:
        raise HTTPException(404, "Feed not found")
    return feed


@router.get("/orders")
async def list_social_orders(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SocialOrderRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.post("/networks", status_code=201)
async def create_network(name: str, api_key: str, api_url: str,
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = AffiliateNetworkRepository(db)
    net = await repo.create_network(name, api_key, api_url)
    await db.commit()
    return {"id": net.id, "name": net.name}


@router.get("/networks")
async def list_networks(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = AffiliateNetworkRepository(db)
    return await repo.list_networks()
