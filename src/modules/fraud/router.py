from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.fraud.repository import FraudRepository

router = APIRouter(prefix="/fraud", tags=["fraud"])


@router.post("/rules", status_code=201)
async def create_rule(
    name: str, rule_type: str, threshold_value: float, score: int = 10,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = FraudRepository(db)
    r = await repo.create_rule(name, rule_type, threshold_value, score)
    await db.commit()
    return r


@router.get("/rules")
async def list_rules(db: AsyncSession = Depends(get_db)):
    repo = FraudRepository(db)
    return await repo.list_rules()


@router.put("/rules/{id}/toggle")
async def toggle_rule(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = FraudRepository(db)
    r = await repo.toggle_rule(id)
    if not r:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return r


@router.post("/check/{order_id}")
async def check_order(
    order_id: int, user_id: int, ip_address: str = None, amount: float = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = FraudRepository(db)
    c = await repo.check_order(order_id, user_id, ip_address, amount)
    await db.commit()
    return c


@router.get("/order/{order_id}")
async def get_order_risk(order_id: int, db: AsyncSession = Depends(get_db)):
    repo = FraudRepository(db)
    r = await repo.get_order_risk(order_id)
    if not r:
        raise HTTPException(404, "No fraud check found for this order")
    return r


@router.get("/history")
async def list_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = FraudRepository(db)
    from sqlalchemy import select
    from src.modules.fraud.models import FraudTransactionHistory
    r = await db.execute(
        select(FraudTransactionHistory).order_by(FraudTransactionHistory.created_at.desc()).limit(50)
    )
    return r.scalars().all()
