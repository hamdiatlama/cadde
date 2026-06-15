from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.trade_in.repository import TradeInRepository

router = APIRouter(prefix="/trade-in", tags=["trade_in"])


@router.post("/requests", status_code=201)
async def create_request(
    product_to_trade: str, condition: str, estimated_value: float = None, target_product_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = TradeInRepository(db)
    r = await repo.create_trade_in_request(current_user.id, product_to_trade, condition, estimated_value, target_product_id)
    await db.commit()
    return r


@router.get("/requests/my")
async def my_requests(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = TradeInRepository(db)
    return await repo.list_requests(current_user.id)


@router.post("/refurbished", status_code=201)
async def create_refurbished(
    original_product_id: int, condition_grade: str, price: float, stock: int = 1,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = TradeInRepository(db)
    rp = await repo.create_refurbished_product(current_user.id, original_product_id, condition_grade, price, stock)
    await db.commit()
    return rp


@router.get("/refurbished")
async def list_refurbished(db: AsyncSession = Depends(get_db)):
    repo = TradeInRepository(db)
    return await repo.list_refurbished()
