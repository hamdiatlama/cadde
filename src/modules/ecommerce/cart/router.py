from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.ecommerce.cart.service import CartService
from src.modules.ecommerce.cart.schemas import AddItem, UpdateItem

router = APIRouter(prefix="/cart", tags=["cart"])

@router.get("", response_model=dict)
async def get_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CartService(db)
    return await svc.get_cart(current_user.id)

@router.post("/add", response_model=dict, status_code=201)
async def add_to_cart(
    data: AddItem,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CartService(db)
    result, err = await svc.add_to_cart(current_user.id, data.product_id, data.quantity, data.variant_label)
    if err:
        raise HTTPException(status_code=404, detail=err)
    await db.commit()
    return {"status": "added", "item_id": result.id}

@router.put("/items/{item_id}", response_model=dict)
async def update_cart_item(
    item_id: int, data: UpdateItem,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CartService(db)
    item = await svc.update_item(current_user.id, item_id, data.quantity)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await db.commit()
    return {"status": "updated"}

@router.delete("/items/{item_id}", response_model=dict)
async def remove_cart_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CartService(db)
    item = await svc.remove_item(current_user.id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    await db.commit()
    return {"status": "removed"}

@router.delete("", response_model=dict)
async def clear_cart(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = CartService(db)
    await svc.clear_cart(current_user.id)
    await db.commit()
    return {"status": "cleared"}
