from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.campaign.service import CampaignService

router = APIRouter(prefix="/campaigns", tags=["campaigns"])


@router.get("/")
async def active_campaigns(db: AsyncSession = Depends(get_db)):
    svc = CampaignService(db)
    return await svc.active_campaigns()


@router.post("/", status_code=201)
async def create_campaign(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can create campaigns")
    svc = CampaignService(db)
    result = await svc.create_campaign(data, current_user.id)
    await db.commit()
    return result


@router.put("/{campaign_id}")
async def update_campaign(
    campaign_id: int, data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can update campaigns")
    svc = CampaignService(db)
    result = await svc.update_campaign(campaign_id, data)
    if not result:
        raise HTTPException(404, "Campaign not found")
    await db.commit()
    return result


@router.get("/flash-sales")
async def flash_sales(db: AsyncSession = Depends(get_db)):
    svc = CampaignService(db)
    return await svc.list_flash_sales()


@router.post("/flash-sales", status_code=201)
async def create_flash_sale(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can create flash sales")
    svc = CampaignService(db)
    result = await svc.create_flash_sale(data)
    await db.commit()
    return result


@router.post("/{campaign_id}/apply")
async def apply_campaign(
    campaign_id: int, order_id: int, order_total: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CampaignService(db)
    result = await svc.apply_campaign(campaign_id, current_user.id, order_id, order_total)
    if not result:
        raise HTTPException(400, "Campaign cannot be applied")
    await db.commit()
    return result
