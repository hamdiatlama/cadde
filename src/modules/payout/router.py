from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.models.seller import Seller
from src.core.auth import get_current_user
from src.modules.payout.service import PayoutService

router = APIRouter(prefix="/payouts", tags=["payouts"])


@router.get("/earnings")
async def earnings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = PayoutService(db)
    return await svc.seller_earnings(seller.id)


@router.post("/request")
async def request_payout(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = PayoutService(db)
    result, err = await svc.process_payout(seller.id, current_user.id)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.get("/history")
async def payout_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return []
    svc = PayoutService(db)
    return await svc.my_payouts(seller.id)


@router.put("/{payout_id}/mark-paid")
async def mark_paid(
    payout_id: int, payment_ref: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can mark payouts as paid")
    svc = PayoutService(db)
    result = await svc.mark_paid(payout_id, payment_ref)
    await db.commit()
    return result
