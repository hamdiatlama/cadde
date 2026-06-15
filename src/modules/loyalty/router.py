from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.loyalty.repository import LoyaltyRepository

router = APIRouter(prefix="/loyalty", tags=["loyalty"])


@router.get("/tiers")
async def list_tiers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = LoyaltyRepository(db)
    tiers = await repo.list_tiers()
    return [
        {"id": t.id, "name": t.name, "min_spend": t.min_spend, "discount_rate": t.discount_rate,
         "free_shipping": t.free_shipping, "badge_color": t.badge_color}
        for t in tiers
    ]


@router.post("/tiers")
async def create_tier(
    name: str = Query(...),
    min_spend: float = Query(0),
    discount_rate: float = Query(0),
    free_shipping: bool = Query(False),
    badge_color: str = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can create loyalty tiers")
    repo = LoyaltyRepository(db)
    tier = await repo.create_tier(name, min_spend, discount_rate, free_shipping, badge_color)
    await db.commit()
    return {"id": tier.id, "name": tier.name, "min_spend": tier.min_spend, "discount_rate": tier.discount_rate}


@router.get("/my")
async def my_loyalty(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = LoyaltyRepository(db)
    ul = await repo.get_or_create_user_loyalty(current_user.id)
    tier = await repo.get_user_tier(current_user.id)
    return {
        "user_id": ul.user_id, "points": ul.points, "total_spend": ul.total_spend,
        "tier": {"id": tier.id, "name": tier.name, "discount_rate": tier.discount_rate,
                 "free_shipping": tier.free_shipping, "badge_color": tier.badge_color} if tier else None,
    }


@router.post("/my/add-points")
async def add_loyalty_points(
    points: int = Query(..., gt=0),
    type: str = Query("earn"),
    reference_type: str = Query(None),
    reference_id: int = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can add points")
    repo = LoyaltyRepository(db)
    ul = await repo.add_points(current_user.id, points, type, reference_type, reference_id)
    await db.commit()
    return {"user_id": ul.user_id, "points": ul.points, "message": f"{points} points added"}


@router.get("/my/history")
async def loyalty_history(
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = LoyaltyRepository(db)
    txns = await repo.get_history(current_user.id, limit)
    return [
        {"id": t.id, "points": t.points, "type": t.type, "reference_type": t.reference_type,
         "reference_id": t.reference_id, "created_at": t.created_at}
        for t in txns
    ]


@router.get("/my/tier")
async def my_tier(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = LoyaltyRepository(db)
    tier = await repo.get_user_tier(current_user.id)
    if not tier:
        raise HTTPException(404, "No tier assigned")
    return {"id": tier.id, "name": tier.name, "discount_rate": tier.discount_rate,
            "free_shipping": tier.free_shipping, "badge_color": tier.badge_color}
