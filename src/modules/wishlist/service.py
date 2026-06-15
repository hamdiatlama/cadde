from src.modules.wishlist.repository import WishlistRepository


class WishlistService:
    def __init__(self, db):
        self.repo = WishlistRepository(db)

    async def list_my_wishlists(self, user_id: int):
        wishlists = await self.repo.get_user_wishlists(user_id)
        result = []
        for wl in wishlists:
            items = await self.repo.get_items(wl.id)
            result.append({
                "id": wl.id, "name": wl.name, "is_public": wl.is_public,
                "share_code": wl.share_code, "item_count": len(items),
                "created_at": wl.created_at.isoformat() if wl.created_at else None,
            })
        return result

    async def create_wishlist(self, user_id: int, name: str, is_public: bool = False):
        wl = await self.repo.create_wishlist(user_id, name, is_public)
        return {"id": wl.id, "name": wl.name, "share_code": wl.share_code, "is_public": wl.is_public}

    async def update_wishlist(self, wishlist_id: int, user_id: int, name: str = None, is_public: bool = None):
        wl = await self.repo.get_wishlist(wishlist_id, user_id)
        if not wl:
            return None
        kwargs = {}
        if name is not None: kwargs["name"] = name
        if is_public is not None: kwargs["is_public"] = is_public
        await self.repo.update_wishlist(wl, **kwargs)
        return {"id": wl.id, "name": wl.name, "is_public": wl.is_public}

    async def delete_wishlist(self, wishlist_id: int, user_id: int):
        wl = await self.repo.get_wishlist(wishlist_id, user_id)
        if not wl:
            return False
        await self.repo.delete_wishlist(wishlist_id)
        return True

    async def get_wishlist_items(self, wishlist_id: int, user_id: int = None, share_code: str = None):
        wl = None
        if share_code:
            wl = await self.repo.get_by_share_code(share_code)
        elif user_id:
            wl = await self.repo.get_wishlist(wishlist_id, user_id)
        if not wl:
            return None
        if not wl.is_public and (not user_id or wl.user_id != user_id):
            return None
        rows = await self.repo.get_items(wl.id)
        items = []
        for item, product in rows:
            items.append({
                "id": item.id, "product_id": product.id, "name": product.name,
                "price": product.price, "image_url": product.image_url,
                "added_at": item.added_at.isoformat() if item.added_at else None,
            })
        return {"wishlist": {"id": wl.id, "name": wl.name, "share_code": wl.share_code}, "items": items}

    async def add_item(self, wishlist_id: int, user_id: int, product_id: int):
        wl = await self.repo.get_wishlist(wishlist_id, user_id)
        if not wl:
            return None, "Wishlist not found"
        item = await self.repo.add_item(wishlist_id, product_id)
        if not item:
            return None, "Product already in wishlist"
        return {"id": item.id, "product_id": product_id, "message": "Added to wishlist"}, None

    async def remove_item(self, item_id: int, wishlist_id: int, user_id: int):
        wl = await self.repo.get_wishlist(wishlist_id, user_id)
        if not wl:
            return False
        await self.repo.remove_item(item_id)
        return True
