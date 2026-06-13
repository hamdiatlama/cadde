from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.models.seller import Seller
from src.models.user import User
from src.models.substitution import Substitution

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product(self, product_id: int):
        r = await self.db.execute(
            select(Product).where(Product.id == product_id, Product.is_active == True)
        )
        return r.scalar_one_or_none()

    async def get_seller(self, seller_id: int):
        r = await self.db.execute(select(Seller).where(Seller.id == seller_id))
        return r.scalar_one_or_none()

    async def get_seller_by_user(self, user_id: int):
        r = await self.db.execute(select(Seller).where(Seller.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_user(self, user_id: int):
        r = await self.db.execute(select(User).where(User.id == user_id))
        return r.scalar_one_or_none()

    async def create_order(self, order: Order):
        self.db.add(order)

    async def create_order_item(self, item: OrderItem):
        self.db.add(item)

    async def get_order(self, order_id: int, user_id: int = None):
        query = select(Order).where(Order.id == order_id)
        if user_id is not None:
            query = query.where(Order.user_id == user_id)
        r = await self.db.execute(query)
        return r.scalar_one_or_none()

    async def get_order_by_id(self, order_id: int):
        r = await self.db.execute(select(Order).where(Order.id == order_id))
        return r.scalar_one_or_none()

    async def list_user_orders(self, user_id: int, status_filter: str = None):
        query = select(Order).where(Order.user_id == user_id)
        if status_filter:
            query = query.where(Order.status == status_filter)
        query = query.order_by(Order.created_at.desc())
        r = await self.db.execute(query)
        return r.scalars().all()

    async def list_seller_orders(self, seller_id: int):
        r = await self.db.execute(
            select(Order).where(Order.seller_id == seller_id)
            .order_by(Order.created_at.desc())
        )
        return r.scalars().all()

    async def get_order_items(self, order_id: int):
        r = await self.db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
        return r.scalars().all()

    async def get_order_item(self, item_id: int, order_id: int):
        r = await self.db.execute(
            select(OrderItem).where(OrderItem.id == item_id, OrderItem.order_id == order_id)
        )
        return r.scalar_one_or_none()

    async def get_substitution(self, sub_id: int):
        r = await self.db.execute(select(Substitution).where(Substitution.id == sub_id))
        return r.scalar_one_or_none()

    async def get_substitutions(self, order_id: int):
        r = await self.db.execute(
            select(Substitution).where(Substitution.order_id == order_id)
            .order_by(Substitution.created_at.desc())
        )
        return r.scalars().all()

    async def create_substitution(self, sub: Substitution):
        self.db.add(sub)

    async def get_order_subtotal_sum(self, order_id: int):
        r = await self.db.execute(
            select(func.sum(OrderItem.unit_price * OrderItem.quantity))
            .where(OrderItem.order_id == order_id)
        )
        return r.scalar() or 0
