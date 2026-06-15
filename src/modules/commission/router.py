from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.commission.repository import CommissionRepository

router = APIRouter(prefix="/commission", tags=["commission"])


@router.post("/rules")
async def create_commission_rule(
    rate: float = Query(..., ge=0, le=100),
    category_id: int = Query(None),
    seller_id: int = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only admins can set commission rules")
    repo = CommissionRepository(db)
    rule = await repo.set_commission_rule(rate, category_id, seller_id)
    await db.commit()
    return {"id": rule.id, "rate": rule.rate, "category_id": rule.category_id, "seller_id": rule.seller_id, "is_active": rule.is_active}


@router.post("/calculate/{order_id}/{amount}")
async def calculate_commission(
    order_id: int,
    amount: float,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.models.seller import Seller
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    seller_id = seller.id if seller else 1
    repo = CommissionRepository(db)
    txn = await repo.calculate_commission(order_id, amount, seller_id)
    await db.commit()
    return {"id": txn.id, "order_id": txn.order_id, "seller_id": txn.seller_id, "amount": txn.amount, "rate": txn.rate}


@router.get("/transactions")
async def list_commissions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.models.seller import Seller
    r = await db.execute(select(Seller).where(Seller.user_id == current_user.id))
    seller = r.scalar_one_or_none()
    if not seller:
        return []
    repo = CommissionRepository(db)
    txns = await repo.list_commission_transactions(seller.id)
    return [
        {"id": t.id, "order_id": t.order_id, "amount": t.amount, "rate": t.rate, "created_at": t.created_at}
        for t in txns
    ]


@router.get("/rules")
async def list_rules(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    repo = CommissionRepository(db)
    rules = await repo.list_active_rules()
    return [
        {"id": r.id, "category_id": r.category_id, "seller_id": r.seller_id, "rate": r.rate, "created_at": r.created_at}
        for r in rules
    ]
