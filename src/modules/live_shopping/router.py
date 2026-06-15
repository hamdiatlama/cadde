from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.live_shopping.repository import LiveShoppingRepository

router = APIRouter(prefix="/live-shopping", tags=["live_shopping"])


@router.post("/streams", status_code=201)
async def create_stream(
    title: str, stream_url: str = None, thumbnail_url: str = None, scheduled_at: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = LiveShoppingRepository(db)
    s = await repo.create_stream(current_user.id, title, stream_url, thumbnail_url, scheduled_at)
    await db.commit()
    return s


@router.get("/streams")
async def list_streams(db: AsyncSession = Depends(get_db)):
    repo = LiveShoppingRepository(db)
    return await repo.list_active()


@router.get("/streams/{id}")
async def get_stream(id: int, db: AsyncSession = Depends(get_db)):
    repo = LiveShoppingRepository(db)
    s = await repo.get_stream(id)
    if not s:
        raise HTTPException(404, "Stream not found")
    return s


@router.post("/streams/{id}/products", status_code=201)
async def add_product(
    id: int, product_id: int, discount_rate: float = 0, sort_order: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = LiveShoppingRepository(db)
    lp = await repo.add_product(id, product_id, discount_rate, sort_order)
    if not lp:
        raise HTTPException(400, "Product already added to stream")
    await db.commit()
    return lp


@router.delete("/streams/{id}/products/{product_id}")
async def remove_product(
    id: int, product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = LiveShoppingRepository(db)
    await repo.remove_product(id, product_id)
    await db.commit()
    return {"ok": True}


@router.get("/streams/{id}/orders")
async def get_orders(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = LiveShoppingRepository(db)
    return await repo.get_stream_orders(id)


@router.put("/streams/{id}/status")
async def update_status(
    id: int, status: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = LiveShoppingRepository(db)
    s = await repo.get_stream(id)
    if not s:
        raise HTTPException(404, "Stream not found")
    s.status = status
    await db.commit()
    return s
