from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.store.coupon_service import CouponService

router = APIRouter(prefix="/coupons", tags=["coupons"])


@router.post("/validate")
async def validate_coupon(
    code: str, order_total: float,
    db: AsyncSession = Depends(get_db),
):
    svc = CouponService(db)
    result = await svc.validate(code, order_total)
    if not result:
        raise HTTPException(404, "Invalid or expired coupon")
    return result


@router.post("/apply")
async def apply_coupon(
    code: str, order_total: float,
    db: AsyncSession = Depends(get_db),
):
    svc = CouponService(db)
    result = await svc.apply(code, order_total)
    if not result:
        raise HTTPException(404, "Invalid or expired coupon")
    await db.commit()
    return result


@router.post("/", status_code=201)
async def create_coupon(
    data: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can create coupons")
    svc = CouponService(db)
    result = await svc.create(data, current_user.id)
    await db.commit()
    return result


@router.get("/")
async def list_coupons(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    svc = CouponService(db)
    return await svc.list_all()
