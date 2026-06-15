from datetime import datetime, timezone
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.comparison.models import Comparison, ComparisonItem
from src.models.product import Product


class ComparisonService:
    def __init__(self, db):
        self.db = db

    async def get_or_create(self, user_id: int):
        r = await self.db.execute(
            select(Comparison).where(Comparison.user_id == user_id).order_by(Comparison.created_at.desc())
        )
        c = r.scalar_one_or_none()
        if not c:
            c = Comparison(user_id=user_id)
            self.db.add(c)
        return c

    async def add_product(self, user_id: int, product_id: int):
        c = await self.get_or_create(user_id)
        existing = await self.db.execute(
            select(ComparisonItem).where(ComparisonItem.comparison_id == c.id, ComparisonItem.product_id == product_id)
        )
        if existing.scalar_one_or_none():
            return None, "Already in comparison"
        ci = ComparisonItem(comparison_id=c.id, product_id=product_id)
        self.db.add(ci)
        return {"id": ci.id, "product_id": product_id, "message": "Added to comparison"}, None

    async def remove_product(self, user_id: int, product_id: int):
        c = await self.get_or_create(user_id)
        await self.db.execute(
            delete(ComparisonItem).where(ComparisonItem.comparison_id == c.id, ComparisonItem.product_id == product_id)
        )

    async def get_comparison(self, user_id: int):
        c = await self.get_or_create(user_id)
        r = await self.db.execute(
            select(ComparisonItem, Product).join(Product, Product.id == ComparisonItem.product_id)
            .where(ComparisonItem.comparison_id == c.id, Product.is_active == True)
        )
        rows = r.all()
        if not rows:
            return {"products": []}
        products = []
        for _, p in rows:
            products.append({
                "id": p.id, "name": p.name, "price": p.price, "compare_price": p.compare_price,
                "image_url": p.image_url, "category": p.category, "description": p.description,
                "rating": p.rating, "review_count": p.review_count, "stock": p.stock,
            })
        return {"products": products}
