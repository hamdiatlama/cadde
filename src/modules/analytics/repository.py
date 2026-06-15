from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from src.modules.analytics.models import AnalyticsReport, SavedDashboard, RfmSegment


class AnalyticsReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> AnalyticsReport:
        report = AnalyticsReport(**data)
        self.db.add(report)
        return report

    async def generate(self, report: AnalyticsReport):
        from src.modules.ecommerce.order.models import Order, OrderItem
        from src.modules.store.models import Product
        from src.models.user import User
        seller_id = report.seller_id
        df = report.date_from
        dt = report.date_to
        base = select(func.count(Order.id)).where(
            Order.seller_id == seller_id, Order.created_at.between(df, dt)
        )
        if report.report_type == "sales":
            total_r = await self.db.execute(
                select(func.coalesce(func.sum(Order.total), 0)).where(
                    Order.seller_id == seller_id, Order.created_at.between(df, dt)
                )
            )
            count_r = await self.db.execute(base.where(Order.status == "completed"))
            return {
                "total_revenue": float(total_r.scalar()),
                "total_orders": count_r.scalar(),
                "report_type": "sales"
            }
        elif report.report_type == "products":
            r = await self.db.execute(
                select(Product.id, Product.name, func.coalesce(func.sum(OrderItem.quantity), 0))
                .outerjoin(OrderItem, OrderItem.product_id == Product.id)
                .outerjoin(Order, OrderItem.order_id == Order.id)
                .where(Product.seller_id == seller_id)
                .group_by(Product.id, Product.name).limit(20)
            )
            return [{"product_id": row[0], "name": row[1], "sold": row[2]} for row in r.all()]
        elif report.report_type == "customers":
            r = await self.db.execute(
                select(
                    func.count(func.distinct(Order.buyer_id)),
                    func.coalesce(func.avg(Order.total), 0)
                ).where(Order.seller_id == seller_id, Order.created_at.between(df, dt))
            )
            row = r.one()
            return {"unique_customers": row[0], "avg_order_value": float(row[1])}
        elif report.report_type == "inventory":
            r = await self.db.execute(
                select(
                    func.count(Product.id),
                    func.coalesce(func.sum(Product.stock), 0),
                    func.coalesce(func.sum(Product.stock * Product.price), 0)
                ).where(Product.seller_id == seller_id)
            )
            row = r.one()
            return {
                "total_products": row[0], "total_stock": row[1],
                "inventory_value": float(row[2]), "report_type": "inventory"
            }
        return {}

    async def list_reports(self, seller_id: int):
        r = await self.db.execute(
            select(AnalyticsReport).where(AnalyticsReport.seller_id == seller_id)
            .order_by(AnalyticsReport.created_at.desc())
        )
        return r.scalars().all()


class SavedDashboardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SavedDashboard:
        d = SavedDashboard(**data)
        self.db.add(d)
        return d

    async def list_all(self, seller_id: int):
        r = await self.db.execute(
            select(SavedDashboard).where(SavedDashboard.seller_id == seller_id)
            .order_by(SavedDashboard.created_at.desc())
        )
        return r.scalars().all()

    async def set_default(self, dashboard_id: int, seller_id: int):
        r = await self.db.execute(
            select(SavedDashboard).where(SavedDashboard.id == dashboard_id,
                                          SavedDashboard.seller_id == seller_id)
        )
        d = r.scalar_one_or_none()
        if not d:
            return None
        await self.db.execute(
            update(SavedDashboard).where(SavedDashboard.seller_id == seller_id)
            .values(is_default=False)
        )
        d.is_default = True
        return d


class RfmSegmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate(self, seller_id: int):
        from src.modules.ecommerce.order.models import Order
        from src.models.user import User
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(
                Order.buyer_id,
                func.max(Order.created_at),
                func.count(Order.id),
                func.coalesce(func.sum(Order.total), 0)
            ).where(Order.seller_id == seller_id, Order.status == "completed")
            .group_by(Order.buyer_id)
        )
        rows = r.all()
        segments = {"champions": 0, "loyal": 0, "potential": 0, "at_risk": 0, "lost": 0}
        for row in rows:
            buyer_id, last_order, freq, monetary = row
            days_since = (now - last_order).days if last_order else 999
            r_score = 5 if days_since <= 30 else 4 if days_since <= 90 else 3 if days_since <= 180 else 2 if days_since <= 365 else 1
            f_score = 5 if freq >= 10 else 4 if freq >= 5 else 3 if freq >= 3 else 2 if freq >= 1 else 1
            m_score = 5 if monetary >= 10000 else 4 if monetary >= 5000 else 3 if monetary >= 1000 else 2 if monetary >= 100 else 1
            combined = r_score + f_score + m_score
            if combined >= 13:
                segments["champions"] += 1
            elif combined >= 10:
                segments["loyal"] += 1
            elif combined >= 7:
                segments["potential"] += 1
            elif combined >= 4:
                segments["at_risk"] += 1
            else:
                segments["lost"] += 1
        results = []
        for name, count in segments.items():
            seg = RfmSegment(seller_id=seller_id, name=name,
                             r_score=0, f_score=0, m_score=0, customer_count=count)
            self.db.add(seg)
            results.append(seg)
        return results

    async def get_segments(self, seller_id: int):
        r = await self.db.execute(
            select(RfmSegment).where(RfmSegment.seller_id == seller_id)
            .order_by(RfmSegment.created_at.desc())
        )
        return r.scalars().all()
