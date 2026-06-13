from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.subscription.service import SubscriptionService

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

@router.get("/plans", response_model=list[dict])
async def list_plans(db: AsyncSession = Depends(get_db)):
    svc = SubscriptionService(db)
    return await svc.list_plans()

@router.post("/plans", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_plan(
    name: str, interval_days: int, duration_months: int, price_per_delivery: float,
    description: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.create_plan(name, interval_days, duration_months,
                                         price_per_delivery, description, current_user.role)
    if err:
        raise HTTPException(status_code=403, detail=err)
    await db.commit()
    return result

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    plan_id: int, seller_id: int, product_id: int,
    start_date: str = None, recipient_name: str = None, recipient_phone: str = None,
    delivery_address: str = None, notes: str = None, card_message: str = None,
    is_gift: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.create_subscription(
        current_user.id, plan_id, seller_id, product_id, start_date,
        recipient_name, recipient_phone, delivery_address, notes, card_message, is_gift
    )
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return result

@router.get("/my", response_model=list[dict])
async def get_my_subscriptions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    return await svc.get_my_subscriptions(current_user.id)

@router.get("/{sub_id}", response_model=dict)
async def get_subscription(
    sub_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result = await svc.get_subscription(sub_id, current_user.id, current_user.role)
    if not result:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result

@router.put("/{sub_id}/pause", response_model=dict)
async def pause_subscription(
    sub_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.pause_subscription(sub_id, current_user.id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return result

@router.put("/{sub_id}/resume", response_model=dict)
async def resume_subscription(
    sub_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.resume_subscription(sub_id, current_user.id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return result

@router.delete("/{sub_id}/cancel", response_model=dict)
async def cancel_subscription(
    sub_id: int, reason: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.cancel_subscription(sub_id, current_user.id, reason)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return result

@router.get("/{sub_id}/deliveries", response_model=list[dict])
async def get_deliveries(
    sub_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result = await svc.get_deliveries(sub_id, current_user.id, current_user.role)
    if result is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return result

@router.put("/deliveries/{delivery_id}/skip", response_model=dict)
async def skip_delivery(
    delivery_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.skip_delivery(delivery_id, current_user.id)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return result

@router.put("/{sub_id}/change-product", response_model=dict)
async def change_subscription_product(
    sub_id: int, new_product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SubscriptionService(db)
    result, err = await svc.change_product(sub_id, current_user.id, new_product_id)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return result
