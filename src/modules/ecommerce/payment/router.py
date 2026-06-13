from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.models.order import Order
from src.models.payment import Payment, PaymentMethod, PointsTransaction
from src.core.auth import get_current_user
from src.modules.ecommerce.payment.schemas import PaymentRequest, PaymentResponse, PointsResponse, InstallmentOption
from src.modules.ecommerce.common import auto_cancel_expired_approvals

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/pay", response_model=PaymentResponse)
async def process_payment(
    data: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await auto_cancel_expired_approvals(db)
    r = await db.execute(select(Order).where(Order.id == data.order_id, Order.user_id == current_user.id))
    order = r.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.payment_status == "paid":
        raise HTTPException(status_code=400, detail="Order already paid")
    if order.status != "approved":
        raise HTTPException(status_code=400, detail=f"Order must be approved by seller first. Current status: {order.status}")
    amount_due = order.total
    points_used = 0
    if data.method == "points" or (data.method == "mixed" and data.points_to_use > 0):
        pts = min(data.points_to_use, current_user.points, int(amount_due))
        if pts > 0:
            points_used = pts
            amount_due -= pts
            current_user.points -= pts
            db.add(PointsTransaction(user_id=current_user.id, amount=-pts, type="spend",
                description=f"Payment for order #{order.id}", order_id=order.id))
    if data.method == "cod":
        order.payment_method = "cod"
        order.payment_status = "pending"
    else:
        order.payment_method = data.method
        order.payment_status = "paid"
    pts_earned = int(order.total * 0.05)
    if pts_earned > 0:
        current_user.points += pts_earned
        db.add(PointsTransaction(user_id=current_user.id, amount=pts_earned, type="earn",
            description=f"Points earned from order #{order.id}", order_id=order.id))
    order.status = "preparing"
    payment = Payment(order_id=order.id, user_id=current_user.id, method=data.method,
        amount=order.total, points_used=points_used, points_earned=pts_earned,
        installment=data.installment, status="completed")
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return PaymentResponse.model_validate(payment)

@router.get("/installments/{amount}", response_model=list[InstallmentOption])
async def get_installment_options(amount: float):
    banks = {"Ziraat": [1, 2, 3, 4, 5, 6], "İş Bankası": [1, 2, 3],
             "Garanti": [1, 2, 3, 4, 5, 6, 9, 12], "Yapı Kredi": [1, 2, 3, 4, 5, 6], "Akbank": [1, 2, 3, 4]}
    options = []
    for bank, installments in banks.items():
        for count in installments:
            interest = 0.015 * (count - 1) if count > 1 else 0
            total = amount * (1 + interest)
            options.append(InstallmentOption(bank=bank, count=count,
                monthly=round(total / count, 2), total=round(total, 2)))
    return options

@router.get("/points", response_model=PointsResponse)
async def get_my_points(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(PointsTransaction).where(PointsTransaction.user_id == current_user.id)
        .order_by(PointsTransaction.created_at.desc()).limit(50)
    )
    txns = [{"id": t.id, "amount": t.amount, "type": t.type, "description": t.description,
             "created_at": t.created_at.isoformat() if t.created_at else None} for t in r.scalars().all()]
    return PointsResponse(balance=current_user.points, transactions=txns)

@router.post("/methods", response_model=dict)
async def add_payment_method(
    type: str, provider: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    m = PaymentMethod(user_id=current_user.id, type=type, provider=provider)
    db.add(m)
    await db.commit()
    return {"message": "Payment method added", "id": m.id}

@router.get("/methods", response_model=list[dict])
async def list_payment_methods(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(PaymentMethod).where(PaymentMethod.user_id == current_user.id, PaymentMethod.is_active == True)
    )
    return [{"id": m.id, "type": m.type, "provider": m.provider, "is_default": m.is_default} for m in r.scalars().all()]
