from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.wishlist.models import Wishlist, WishlistItem
from src.models.product import Product


class WishlistRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_wishlists(self, user_id: int):
        r = await self.db.execute(
            select(Wishlist).where(Wishlist.user_id == user_id).order_by(Wishlist.created_at.desc())
        )
        return r.scalars().all()

    async def get_wishlist(self, wishlist_id: int, user_id: int = None):
        q = select(Wishlist).where(Wishlist.id == wishlist_id)
        if user_id:
            q = q.where(Wishlist.user_id == user_id)
        r = await self.db.execute(q)
        return r.scalar_one_or_none()

    async def get_by_share_code(self, code: str):
        r = await self.db.execute(select(Wishlist).where(Wishlist.share_code == code))
        return r.scalar_one_or_none()

    async def create_wishlist(self, user_id: int, name: str, is_public: bool = False):
        import uuid
        wl = Wishlist(user_id=user_id, name=name, is_public=is_public, share_code=uuid.uuid4().hex[:8])
        self.db.add(wl)
        return wl

    async def update_wishlist(self, wl: Wishlist, **kwargs):
        for k, v in kwargs.items():
            setattr(wl, k, v)

    async def delete_wishlist(self, wishlist_id: int):
        await self.db.execute(delete(WishlistItem).where(WishlistItem.wishlist_id == wishlist_id))
        await self.db.execute(delete(Wishlist).where(Wishlist.id == wishlist_id))

    async def get_items(self, wishlist_id: int):
        r = await self.db.execute(
            select(WishlistItem, Product).join(Product, Product.id == WishlistItem.product_id)
            .where(WishlistItem.wishlist_id == wishlist_id)
        )
        return r.all()

    async def add_item(self, wishlist_id: int, product_id: int):
        existing = await self.db.execute(
            select(WishlistItem).where(WishlistItem.wishlist_id == wishlist_id, WishlistItem.product_id == product_id)
        )
        if existing.scalar_one_or_none():
            return None
        item = WishlistItem(wishlist_id=wishlist_id, product_id=product_id)
        self.db.add(item)
        return item

    async def remove_item(self, item_id: int):
        await self.db.execute(delete(WishlistItem).where(WishlistItem.id == item_id))
