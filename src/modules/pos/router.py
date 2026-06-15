from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.pos.repository import PosTerminalRepository, PosOrderRepository

router = APIRouter(prefix="/pos", tags=["pos"])


@router.post("/terminals", status_code=201)
async def register_terminal(
    name: str, serial_no: str, location: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PosTerminalRepository(db)
    t = await repo.register_terminal(current_user.id, name, serial_no, location)
    await db.commit()
    return t


@router.get("/terminals")
async def list_terminals(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PosTerminalRepository(db)
    return await repo.list_terminals(current_user.id)


@router.post("/orders", status_code=201)
async def create_pos_order(
    terminal_id: int, items: list[dict], payment_method: str,
    customer_id: int = None, order_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PosOrderRepository(db)
    order = await repo.create_order(terminal_id, current_user.id, items, payment_method, customer_id, order_id)
    await db.commit()
    return order


@router.get("/orders")
async def list_pos_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PosOrderRepository(db)
    return await repo.list_orders(current_user.id)


@router.get("/orders/{order_id}")
async def get_pos_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PosOrderRepository(db)
    order = await repo.get_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    return order
