from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.seller_performance.models import SellerRating, SellerBadge, SellerPerformanceMetric


class SellerPerformanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_rating(self, seller_id: int, buyer_id: int, order_id: int, rating: int, review: str = None) -> SellerRating:
        sr = SellerRating(seller_id=seller_id, buyer_id=buyer_id, order_id=order_id, rating=rating, review=review)
        self.db.add(sr); return sr

    async def get_avg_rating(self, seller_id: int) -> float:
        r = await self.db.execute(
            select(func.avg(SellerRating.rating)).where(SellerRating.seller_id == seller_id)
        )
        return round(r.scalar() or 0, 2)

    async def get_rating_count(self, seller_id: int) -> int:
        r = await self.db.execute(
            select(func.count(SellerRating.id)).where(SellerRating.seller_id == seller_id)
        )
        return r.scalar() or 0

    async def list_ratings(self, seller_id: int, limit: int = 50):
        r = await self.db.execute(
            select(SellerRating).where(SellerRating.seller_id == seller_id).order_by(SellerRating.created_at.desc()).limit(limit)
        )
        return r.scalars().all()

    async def award_badge(self, seller_id: int, badge_type: str) -> SellerBadge:
        b = SellerBadge(seller_id=seller_id, badge_type=badge_type)
        self.db.add(b); return b

    async def get_badges(self, seller_id: int):
        r = await self.db.execute(select(SellerBadge).where(SellerBadge.seller_id == seller_id))
        return r.scalars().all()

    async def calculate_metrics(self, seller_id: int, period: str = "30d"):
        from datetime import datetime, timezone, timedelta
        cut = {
            "7d": datetime.now(timezone.utc) - timedelta(days=7),
            "30d": datetime.now(timezone.utc) - timedelta(days=30),
            "90d": datetime.now(timezone.utc) - timedelta(days=90),
        }.get(period, datetime.now(timezone.utc) - timedelta(days=30))

        from src.modules.store.models import Order
        r = await self.db.execute(
            select(
                func.count(Order.id),
                func.sum(func.cast(Order.status == "completed", func.Integer)),
                func.sum(func.cast(Order.status == "cancelled", func.Integer)),
            ).where(Order.seller_id == seller_id, Order.created_at >= cut)
        )
        row = r.one()
        total = row[0] or 0
        completed = row[1] or 0
        cancelled = row[2] or 0
        avg = await self.get_avg_rating(seller_id)

        metric = SellerPerformanceMetric(
            seller_id=seller_id, period=period, total_orders=total, completed_orders=completed,
            cancelled_orders=cancelled, avg_rating=avg,
            on_time_rate=round((completed / total * 100) if total > 0 else 100, 2)
        )
        self.db.add(metric)
        return metric

    async def get_metrics(self, seller_id: int, period: str = "30d"):
        r = await self.db.execute(
            select(SellerPerformanceMetric).where(
                SellerPerformanceMetric.seller_id == seller_id, SellerPerformanceMetric.period == period
            ).order_by(SellerPerformanceMetric.calculated_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()
