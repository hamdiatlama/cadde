from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.wishlist.service import WishlistService

router = APIRouter(prefix="/wishlist", tags=["wishlist"])


@router.get("/")
async def list_wishlists(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    return await svc.list_my_wishlists(current_user.id)


@router.post("/", status_code=201)
async def create_wishlist(
    name: str = "Favorilerim", is_public: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    result = await svc.create_wishlist(current_user.id, name, is_public)
    await db.commit()
    return result


@router.put("/{wishlist_id}")
async def update_wishlist(
    wishlist_id: int, name: str = None, is_public: bool = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    result = await svc.update_wishlist(wishlist_id, current_user.id, name, is_public)
    if not result:
        raise HTTPException(404, "Wishlist not found")
    await db.commit()
    return result


@router.delete("/{wishlist_id}")
async def delete_wishlist(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    ok = await svc.delete_wishlist(wishlist_id, current_user.id)
    if not ok:
        raise HTTPException(404, "Wishlist not found")
    await db.commit()
    return {"ok": True}


@router.get("/{wishlist_id}/items")
async def get_wishlist_items(
    wishlist_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    result = await svc.get_wishlist_items(wishlist_id, user_id=current_user.id)
    if not result:
        raise HTTPException(404, "Wishlist not found")
    return result


@router.get("/shared/{share_code}")
async def get_shared_wishlist(
    share_code: str,
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    result = await svc.get_wishlist_items(0, share_code=share_code)
    if not result:
        raise HTTPException(404, "Wishlist not found")
    return result


@router.post("/{wishlist_id}/items", status_code=201)
async def add_item(
    wishlist_id: int, product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    result, err = await svc.add_item(wishlist_id, current_user.id, product_id)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.delete("/{wishlist_id}/items/{item_id}")
async def remove_item(
    wishlist_id: int, item_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = WishlistService(db)
    ok = await svc.remove_item(item_id, wishlist_id, current_user.id)
    if not ok:
        raise HTTPException(404, "Item not found")
    await db.commit()
    return {"ok": True}
