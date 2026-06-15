from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.payout_extended.repository import PayoutScheduleRepository
from src.modules.payout.models import Payout, PayoutBatch

router = APIRouter(prefix="/payout-extended", tags=["payout_extended"])

@router.post("/schedule", status_code=201)
async def set_schedule(
    seller_id: int, frequency: str, day: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PayoutScheduleRepository(db)
    sched = await repo.set_schedule(seller_id, frequency, day)
    await db.commit()
    return sched

@router.get("/schedule")
async def get_schedule(
    seller_id: int,
    db: AsyncSession = Depends(get_db),
):
    repo = PayoutScheduleRepository(db)
    sched = await repo.get_schedule(seller_id)
    if not sched:
        raise HTTPException(404, "Schedule not found")
    return sched

@router.get("/balances")
async def list_balances(
    seller_id: int,
    db: AsyncSession = Depends(get_db),
):
    from sqlalchemy import select
    from src.modules.payout_extended.models import MultiCurrencyBalance
    r = await db.execute(
        select(MultiCurrencyBalance).where(MultiCurrencyBalance.seller_id == seller_id)
    )
    return r.scalars().all()

@router.get("/balances/{currency}")
async def get_balance(
    seller_id: int, currency: str,
    db: AsyncSession = Depends(get_db),
):
    repo = PayoutScheduleRepository(db)
    bal = await repo.get_currency_balance(seller_id, currency.upper())
    if not bal:
        raise HTTPException(404, "Balance not found")
    return bal

@router.post("/convert")
async def convert_currency(
    from_currency: str, to_currency: str, amount: float,
    db: AsyncSession = Depends(get_db),
):
    repo = PayoutScheduleRepository(db)
    try:
        return await repo.convert_currency(from_currency.upper(), to_currency.upper(), amount)
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.post("/process-scheduled")
async def process_scheduled(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from datetime import datetime, timezone, timedelta
    from sqlalchemy import select, update
    from src.modules.payout_extended.models import PayoutSchedule
    r = await db.execute(
        select(PayoutSchedule).where(PayoutSchedule.is_active == True)
    )
    schedules = r.scalars().all()
    now = datetime.now(timezone.utc)
    processed = []
    for s in schedules:
        oweek = now.isoweekday() % 7
        if s.frequency == "weekly" and s.day_of_week != oweek:
            continue
        if s.frequency == "biweekly" and (s.day_of_month != now.day or now.day > 28):
            continue
        if s.frequency == "monthly" and s.day_of_month != now.day:
            continue
        bal_r = await db.execute(
            select(MultiCurrencyBalance).where(
                MultiCurrencyBalance.seller_id == s.seller_id,
                MultiCurrencyBalance.currency == "USD",
            )
        )
        bal = bal_r.scalar_one_or_none()
        if not bal or bal.balance < s.min_amount:
            continue
        payout = Payout(
            seller_id=s.seller_id, amount=bal.balance,
            net_amount=bal.balance, status="processing", period_start=now - timedelta(days=30), period_end=now,
        )
        db.add(payout)
        bal.balance = 0
        processed.append({"seller_id": s.seller_id, "amount": bal.balance})
    await db.commit()
    return {"processed": len(processed), "payouts": processed}
