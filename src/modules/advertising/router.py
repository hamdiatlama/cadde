from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.models.seller import Seller
from src.core.auth import get_current_user
from src.modules.advertising.service import AdService

router = APIRouter(prefix="/ads", tags=["advertising"])


@router.get("/sponsored")
async def sponsored_products(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = AdService(db)
    return await svc.get_sponsored(limit)


@router.post("/campaigns", status_code=201)
async def create_campaign(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = AdService(db)
    result = await svc.create_campaign(seller.id, data)
    await db.commit()
    return result


@router.put("/campaigns/{campaign_id}")
async def update_campaign(
    campaign_id: int, data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = AdService(db)
    result = await svc.update_campaign(campaign_id, seller.id, data)
    if not result:
        raise HTTPException(404, "Campaign not found")
    await db.commit()
    return result


@router.get("/campaigns")
async def list_campaigns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return []
    svc = AdService(db)
    return await svc.list_my_campaigns(seller.id)


@router.get("/campaigns/{campaign_id}")
async def campaign_analytics(
    campaign_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = AdService(db)
    result = await svc.get_campaign_analytics(campaign_id, seller.id)
    if not result:
        raise HTTPException(404, "Campaign not found")
    return result


@router.post("/campaigns/{campaign_id}/products", status_code=201)
async def add_product(
    campaign_id: int, product_id: int, bid_amount: float = 0.50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = AdService(db)
    result, err = await svc.add_product(campaign_id, seller.id, product_id, bid_amount)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.post("/click/{ad_product_id}")
async def record_click(
    ad_product_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = AdService(db)
    await svc.record_click(ad_product_id)
    await db.commit()
    return {"ok": True}
