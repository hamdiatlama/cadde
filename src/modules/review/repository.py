from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.review import Review
from src.models.order import Order
from src.models.product import Product

class ReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order(self, order_id: int, user_id: int):
        r = await self.db.execute(
            select(Order).where(Order.id == order_id, Order.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def get_product(self, product_id: int):
        r = await self.db.execute(select(Product).where(Product.id == product_id))
        return r.scalar_one_or_none()

    async def get_existing_review(self, order_id: int, product_id: int, user_id: int):
        r = await self.db.execute(
            select(Review).where(
                Review.order_id == order_id, Review.product_id == product_id,
                Review.user_id == user_id,
            )
        )
        return r.scalar_one_or_none()

    async def create_review(self, review: Review):
        self.db.add(review)

    async def get_product_stats(self, product_id: int):
        r = await self.db.execute(
            select(func.avg(Review.rating), func.count(Review.id))
            .where(Review.product_id == product_id, Review.is_approved == True)
        )
        return r.one()

    async def get_product_reviews(self, product_id: int, offset: int, limit: int):
        r = await self.db.execute(
            select(Review).where(Review.product_id == product_id, Review.is_approved == True)
            .order_by(Review.created_at.desc()).offset(offset).limit(limit)
        )
        return r.scalars().all()

    async def get_user_reviews(self, user_id: int):
        r = await self.db.execute(
            select(Review).where(Review.user_id == user_id)
            .order_by(Review.created_at.desc())
        )
        return r.scalars().all()
