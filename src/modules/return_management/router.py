from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.return_management.repository import ReturnManagementRepository

router = APIRouter(prefix="/returns", tags=["return_management"])


@router.post("/", status_code=201)
async def create_return(
    order_id: int, reason: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ReturnManagementRepository(db)
    r = await repo.create_request(current_user.id, order_id, reason)
    await db.commit()
    return r


@router.get("/my")
async def my_returns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ReturnManagementRepository(db)
    return await repo.list_by_user(current_user.id)


@router.get("/seller")
async def seller_returns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ReturnManagementRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.put("/{id}/approve")
async def approve_return(
    id: int, refund_amount: float,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ReturnManagementRepository(db)
    r = await repo.approve_request(id, refund_amount)
    if not r:
        raise HTTPException(404, "Return request not found")
    await db.commit()
    return r


@router.put("/{id}/reject")
async def reject_return(
    id: int, reason: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ReturnManagementRepository(db)
    r = await repo.reject_request(id, reason)
    if not r:
        raise HTTPException(404, "Return request not found")
    await db.commit()
    return r
