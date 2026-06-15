from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.models.seller import Seller
from src.core.auth import get_current_user
from sqlalchemy import select
from src.modules.escrow.service import EscrowService

router = APIRouter(prefix="/escrow", tags=["escrow"])


@router.post("/hold")
async def hold_payment(
    order_id: int, amount: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EscrowService(db)
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    seller_id = seller.id if seller else 1
    result, err = await svc.hold_payment(order_id, current_user.id, seller_id, amount)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.post("/release/{escrow_id}")
async def release_escrow(
    escrow_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can release escrow")
    svc = EscrowService(db)
    result = await svc.release_payment(escrow_id, "admin")
    if not result:
        raise HTTPException(404, "Escrow not found or already released")
    await db.commit()
    return result


@router.get("/order/{order_id}")
async def escrow_status(
    order_id: int, db: AsyncSession = Depends(get_db),
):
    svc = EscrowService(db)
    result = await svc.get_escrow_status(order_id)
    if not result:
        raise HTTPException(404, "No escrow for this order")
    return result


@router.get("/seller/balance")
async def seller_balance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = EscrowService(db)
    return await svc.seller_balance(seller.id)


@router.post("/disputes")
async def raise_dispute(
    order_id: int, reason: str, description: str = None, evidence: str = None,
    raised_against: str = "seller",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EscrowService(db)
    result = await svc.raise_dispute(order_id, current_user.id, reason, description, evidence, raised_against)
    await db.commit()
    return result


@router.put("/disputes/{dispute_id}/resolve")
async def resolve_dispute(
    dispute_id: int, resolution: str, refund_buyer: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can resolve disputes")
    svc = EscrowService(db)
    result = await svc.resolve_dispute(dispute_id, resolution, current_user.id, refund_buyer)
    if not result:
        raise HTTPException(404, "Dispute not found")
    await db.commit()
    return result


@router.get("/disputes/{order_id}")
async def order_disputes(
    order_id: int, db: AsyncSession = Depends(get_db),
):
    svc = EscrowService(db)
    return await svc.get_disputes(order_id)
