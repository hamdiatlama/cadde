from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.cart import Cart, CartItem
from src.models.product import Product

class CartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart(self, user_id: int):
        r = await self.db.execute(select(Cart).where(Cart.user_id == user_id))
        return r.scalar_one_or_none()

    async def create_cart(self, user_id: int):
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        return cart

    async def get_cart_items(self, cart_id: int):
        r = await self.db.execute(select(CartItem).where(CartItem.cart_id == cart_id))
        return r.scalars().all()

    async def get_cart_item(self, item_id: int, cart_id: int):
        r = await self.db.execute(
            select(CartItem).where(CartItem.id == item_id, CartItem.cart_id == cart_id)
        )
        return r.scalar_one_or_none()

    async def get_product(self, product_id: int):
        r = await self.db.execute(select(Product).where(Product.id == product_id))
        return r.scalar_one_or_none()

    async def find_cart_item(self, cart_id: int, product_id: int, variant_label: str | None):
        r = await self.db.execute(
            select(CartItem).where(
                CartItem.cart_id == cart_id,
                CartItem.product_id == product_id,
                CartItem.variant_label == variant_label,
            )
        )
        return r.scalar_one_or_none()

    async def delete_item(self, item):
        await self.db.delete(item)

    async def clear_cart(self, cart_id: int):
        items = await self.get_cart_items(cart_id)
        for item in items:
            await self.db.delete(item)
