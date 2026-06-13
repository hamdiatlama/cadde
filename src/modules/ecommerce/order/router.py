from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.ecommerce.order.schemas import OrderCreate, OrderResponse, OrderCancelRequest, OrderModifyRequest
from src.modules.ecommerce.order.service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order, err = await svc.create_order(current_user.id, data)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    await db.refresh(order)
    return OrderResponse.model_validate(order)

@router.get("/", response_model=list[OrderResponse])
async def list_orders(
    status_filter: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    return await svc.list_orders(current_user.id, status_filter)

@router.get("/seller", response_model=list[OrderResponse])
async def seller_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can view seller orders")
    svc = OrderService(db)
    return await svc.seller_orders(current_user.id)

@router.get("/pending-approval", response_model=list[OrderResponse])
async def pending_approval_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can view pending approvals")
    svc = OrderService(db)
    return await svc.pending_approval_orders(current_user.id)

@router.post("/{order_id}/approve", response_model=OrderResponse)
async def approve_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order, err = await svc.approve_order(order_id, current_user.id, current_user.role)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    await db.refresh(order)
    return order

@router.post("/{order_id}/reject", response_model=OrderResponse)
async def reject_order(
    order_id: int, reason: str = "Stokta urun bulunamadi",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order, err = await svc.reject_order(order_id, current_user.id, current_user.role, reason)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    await db.refresh(order)
    return order

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order = await svc.get_order(order_id, current_user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/{order_id}/cancel", response_model=OrderResponse)
async def cancel_order(
    order_id: int, data: OrderCancelRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order, err = await svc.cancel_order(order_id, current_user.id, data.reason)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    await db.refresh(order)
    return order

@router.put("/{order_id}/modify", response_model=OrderResponse)
async def modify_order(
    order_id: int, data: OrderModifyRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    order, err = await svc.modify_order(order_id, current_user.id, data)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    await db.refresh(order)
    return order

@router.post("/{order_id}/substitutions", response_model=dict)
async def propose_substitution(
    order_id: int, order_item_id: int, suggested_product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    result, err = await svc.propose_substitution(
        order_id, order_item_id, suggested_product_id, current_user.id, current_user.role
    )
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return result

@router.get("/{order_id}/substitutions", response_model=list[dict])
async def get_substitutions(order_id: int, db: AsyncSession = Depends(get_db)):
    svc = OrderService(db)
    return await svc.get_substitutions(order_id)

@router.put("/substitutions/{sub_id}/respond", response_model=dict)
async def respond_substitution(
    sub_id: int, approve: bool,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    result, err = await svc.respond_substitution(sub_id, approve, current_user.id)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return result

@router.post("/{order_id}/compensation", response_model=dict)
async def request_compensation(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = OrderService(db)
    result, err = await svc.request_compensation(order_id, current_user.id)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return result
