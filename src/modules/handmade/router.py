from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.handmade.repository import HandmadeRepository

router = APIRouter(prefix="/handmade", tags=["handmade"])


@router.post("/orders", status_code=201)
async def create_order(
    seller_id: int, description: str, requirements: str = None, product_id: int = None, estimated_days: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = HandmadeRepository(db)
    o = await repo.create_order(current_user.id, seller_id, description, requirements, product_id, estimated_days)
    await db.commit()
    return o


@router.get("/orders/{id}")
async def get_order(id: int, db: AsyncSession = Depends(get_db)):
    repo = HandmadeRepository(db)
    o = await repo.get_order(id)
    if not o:
        raise HTTPException(404, "Order not found")
    return o


@router.get("/orders/my/buyer")
async def my_buyer_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = HandmadeRepository(db)
    return await repo.list_by_buyer(current_user.id)


@router.get("/orders/my/seller")
async def my_seller_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = HandmadeRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.put("/orders/{id}/status")
async def update_order_status(
    id: int, status: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = HandmadeRepository(db)
    o = await repo.update_status(id, status)
    if not o:
        raise HTTPException(404, "Order not found")
    await db.commit()
    return o
