from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.abandoned_cart.repository import AbandonedCartRepository

router = APIRouter(prefix="/abandoned-cart", tags=["abandoned_cart"])


@router.post("/mark", status_code=201)
async def mark_cart_abandoned(cart_data: str, total: int, current_user: User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    repo = AbandonedCartRepository(db)
    ac = await repo.mark_abandoned(current_user.id, cart_data, total)
    await db.commit()
    return {"id": ac.id, "status": "tracked"}


@router.post("/reminder-templates", status_code=201)
async def create_reminder_template(name: str, subject: str, body: str, delay_hours: int = 24,
                                    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = AbandonedCartRepository(db)
    t = await repo.create_reminder_template(name, subject, body, delay_hours)
    await db.commit()
    return {"id": t.id, "name": t.name}


@router.get("/pending")
async def get_pending_abandoned(hours: int = 24, db: AsyncSession = Depends(get_db)):
    repo = AbandonedCartRepository(db)
    return await repo.get_abandoned_carts(hours)
