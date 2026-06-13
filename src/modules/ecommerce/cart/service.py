from src.modules.ecommerce.cart.repository import CartRepository
from src.models.cart import CartItem

class CartService:
    def __init__(self, db):
        self.repo = CartRepository(db)

    async def get_cart(self, user_id: int):
        cart = await self.repo.get_cart(user_id)
        if not cart:
            return {"items": [], "total": 0}
        items_raw = await self.repo.get_cart_items(cart.id)
        items = []
        total = 0.0
        for ci in items_raw:
            p = await self.repo.get_product(ci.product_id)
            if not p:
                continue
            subtotal = p.price * ci.quantity
            total += subtotal
            items.append({
                "id": ci.id, "product_id": ci.product_id, "name": p.name,
                "price": p.price, "quantity": ci.quantity,
                "variant_label": ci.variant_label, "image_url": p.image_url,
                "subtotal": subtotal,
            })
        return {"items": items, "total": round(total, 2)}

    async def add_to_cart(self, user_id: int, product_id: int, quantity: int, variant_label: str | None):
        p = await self.repo.get_product(product_id)
        if not p:
            return None, "Product not found"
        cart = await self.repo.get_cart(user_id)
        if not cart:
            cart = await self.repo.create_cart(user_id)
        existing = await self.repo.find_cart_item(cart.id, product_id, variant_label)
        if existing:
            existing.quantity += quantity
            item_id = existing.id
        else:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity, variant_label=variant_label)
            self.repo.db.add(item)
            return item, None
        return existing, None

    async def update_item(self, user_id: int, item_id: int, quantity: int):
        cart = await self.repo.get_cart(user_id)
        if not cart:
            return None
        item = await self.repo.get_cart_item(item_id, cart.id)
        if not item:
            return None
        item.quantity = quantity
        return item

    async def remove_item(self, user_id: int, item_id: int):
        cart = await self.repo.get_cart(user_id)
        if not cart:
            return None
        item = await self.repo.get_cart_item(item_id, cart.id)
        if not item:
            return None
        await self.repo.delete_item(item)
        return item

    async def clear_cart(self, user_id: int):
        cart = await self.repo.get_cart(user_id)
        if not cart:
            return False
        await self.repo.clear_cart(cart.id)
        return True
