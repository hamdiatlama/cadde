from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.subscribe_save.repository import SubscribeSaveRepository

router = APIRouter(prefix="/subscribe-save", tags=["subscribe_save"])


@router.post("/plans", status_code=201)
async def create_plan(product_id: int, interval_days: int, discount_rate: float = 5, max_orders: int = None,
                      current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    p = await repo.create_plan(product_id, current_user.id, interval_days, discount_rate, max_orders)
    await db.commit()
    return {"id": p.id, "product_id": p.product_id, "interval_days": p.interval_days}


@router.get("/plans/{product_id}")
async def list_plans(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    return await repo.list_plans(product_id)


@router.post("/{plan_id}/subscribe", status_code=201)
async def subscribe(plan_id: int, current_user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    sub = await repo.subscribe(plan_id, current_user.id)
    if not sub:
        raise HTTPException(404, "Plan not found")
    await db.commit()
    return {"id": sub.id, "plan_id": sub.plan_id, "next_order_date": sub.next_order_date.isoformat() if sub.next_order_date else None}


@router.post("/{sub_id}/cancel")
async def cancel_subscription(sub_id: int, current_user: User = Depends(get_current_user),
                              db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    sub = await repo.cancel_subscription(sub_id)
    if not sub:
        raise HTTPException(404, "Subscription not found")
    await db.commit()
    return {"id": sub.id, "is_active": sub.is_active}


@router.get("/my")
async def get_my_subscriptions(current_user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    return await repo.get_user_subscriptions(current_user.id)


@router.post("/generate-orders")
async def generate_orders(current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    repo = SubscribeSaveRepository(db)
    generated = await repo.generate_orders()
    await db.commit()
    return {"generated": len(generated), "orders": [{"id": s.id, "next_order_date": s.next_order_date.isoformat() if s.next_order_date else None} for s in generated]}
