from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.models.seller import Seller
from src.core.auth import get_current_user
from src.modules.dashboard.service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/seller")
async def seller_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        raise HTTPException(404, "Seller not found")
    svc = DashboardService(db)
    return await svc.seller_dashboard(seller.id)


@router.get("/admin")
async def admin_dashboard(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    svc = DashboardService(db)
    return await svc.admin_dashboard()
