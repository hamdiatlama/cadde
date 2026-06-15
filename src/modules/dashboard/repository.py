from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.models.review import Review
from src.modules.escrow.models import EscrowTransaction


class DashboardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def seller_stats(self, seller_id: int):
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = today_start.replace(day=1)

        r = await self.db.execute(
            select(func.count(), func.coalesce(func.sum(Order.total), 0))
            .where(Order.seller_id == seller_id, Order.created_at >= today_start)
        )
        today_count, today_rev = r.one()

        r = await self.db.execute(
            select(func.count(), func.coalesce(func.sum(Order.total), 0))
            .where(Order.seller_id == seller_id, Order.created_at >= month_start)
        )
        month_count, month_rev = r.one()

        r = await self.db.execute(
            select(func.count()).where(Order.seller_id == seller_id, Order.status == "pending_approval")
        )
        pending = r.scalar()

        r = await self.db.execute(
            select(func.count()).where(Order.seller_id == seller_id, Order.status == "delivered")
        )
        delivered = r.scalar()

        r = await self.db.execute(
            select(func.coalesce(func.avg(Review.rating), 0))
            .select_from(Order).join(Review, Review.order_id == Order.id)
            .where(Order.seller_id == seller_id)
        )
        avg_rating = r.scalar()

        return {
            "today_orders": today_count, "today_revenue": round(float(today_rev or 0), 2),
            "month_orders": month_count, "month_revenue": round(float(month_rev or 0), 2),
            "pending_orders": pending, "delivered_orders": delivered,
            "avg_rating": round(float(avg_rating or 0), 1),
        }

    async def seller_monthly_sales(self, seller_id: int, months: int = 6):
        from datetime import datetime, timezone, timedelta
        since = datetime.now(timezone.utc) - timedelta(days=months * 30)
        r = await self.db.execute(
            select(
                func.strftime("%Y-%m", Order.created_at).label("month"),
                func.count().label("order_count"),
                func.coalesce(func.sum(Order.total), 0).label("revenue"),
            )
            .where(Order.seller_id == seller_id, Order.created_at >= since, Order.status == "delivered")
            .group_by("month").order_by("month")
        )
        return [{"month": row[0], "orders": row[1], "revenue": round(float(row[2]), 2)} for row in r.all()]

    async def top_products(self, seller_id: int, limit: int = 5):
        r = await self.db.execute(
            select(
                Product.id, Product.name, Product.price, Product.image_url,
                func.sum(OrderItem.quantity).label("sold"),
                func.coalesce(func.sum(OrderItem.unit_price * OrderItem.quantity), 0).label("revenue"),
            )
            .select_from(OrderItem)
            .join(Product, Product.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Product.seller_id == seller_id, Order.status == "delivered")
            .group_by(Product.id, Product.name, Product.price, Product.image_url)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        )
        return [{"id": row[0], "name": row[1], "price": row[2], "image_url": row[3],
                 "sold_count": row[4], "revenue": round(float(row[5]), 2)} for row in r.all()]

    async def admin_stats(self):
        r = await self.db.execute(select(func.count()).select_from(Product))
        total_products = r.scalar()
        r = await self.db.execute(select(func.count()).select_from(Order))
        total_orders = r.scalar()
        r = await self.db.execute(
            select(func.coalesce(func.sum(Order.total), 0))
            .where(Order.status == "delivered")
        )
        total_revenue = r.scalar()
        r = await self.db.execute(select(func.count()).where(Order.status == "pending_approval"))
        pending_orders = r.scalar()
        r = await self.db.execute(select(func.count()).select_from(EscrowTransaction))
        escrow_count = r.scalar()
        return {
            "total_products": total_products, "total_orders": total_orders,
            "total_revenue": round(float(total_revenue or 0), 2),
            "pending_orders": pending_orders, "escrow_transactions": escrow_count,
        }
