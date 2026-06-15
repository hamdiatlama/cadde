from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.recommendation.models import ProductView, SearchHistory
from src.models.product import Product


class RecommendationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_view(self, user_id: int, product_id: int, session_id: str = None):
        v = ProductView(user_id=user_id, product_id=product_id, session_id=session_id)
        self.db.add(v)
        return v

    async def record_search(self, user_id: int, query: str, session_id: str = None):
        s = SearchHistory(user_id=user_id, query=query, session_id=session_id)
        self.db.add(s)
        return s

    async def get_recent_views(self, user_id: int, limit: int = 20):
        r = await self.db.execute(
            select(ProductView).where(ProductView.user_id == user_id)
            .order_by(ProductView.viewed_at.desc()).limit(limit)
        )
        return r.scalars().all()

    async def get_popular_products(self, limit: int = 10):
        r = await self.db.execute(
            select(Product, func.count(ProductView.product_id).label("views"))
            .join(ProductView, Product.id == ProductView.product_id)
            .where(Product.is_active == True)
            .group_by(Product.id)
            .order_by(func.count(ProductView.product_id).desc())
            .limit(limit)
        )
        return r.all()

    async def get_similar_products(self, product_id: int, limit: int = 6):
        r = await self.db.execute(select(Product).where(Product.id == product_id))
        product = r.scalar_one_or_none()
        if not product or not product.category:
            return []
        r = await self.db.execute(
            select(Product).where(
                Product.category == product.category,
                Product.id != product_id,
                Product.is_active == True
            ).limit(limit)
        )
        return r.scalars().all()

    async def get_recommendations(self, user_id: int):
        views = await self.db.execute(
            select(ProductView.product_id).where(ProductView.user_id == user_id)
            .order_by(ProductView.viewed_at.desc()).limit(50)
        )
        viewed_ids = set(r[0] for r in views.all())
        if not viewed_ids:
            return []
        visited = await self.db.execute(
            select(Product.category).where(Product.id.in_(viewed_ids), Product.is_active == True)
        )
        categories = set(r[0] for r in visited.all() if r[0])
        if not categories:
            return []
        r = await self.db.execute(
            select(Product).where(
                Product.category.in_(categories),
                Product.id.notin_(viewed_ids),
                Product.is_active == True
            ).limit(20)
        )
        return r.scalars().all()
