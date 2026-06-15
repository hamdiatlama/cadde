from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.compliance.models import (
    MapPolicy, MapViolation, CounterfeitReport, ProductCompliance,
    ProductRecall, PolicyViolation,
)


class MapPolicyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_policy(self, seller_id: int, product_id: int, min_advertised_price: float) -> MapPolicy:
        mp = MapPolicy(seller_id=seller_id, product_id=product_id, min_advertised_price=min_advertised_price)
        self.db.add(mp)
        return mp

    async def check_violation(self, product_id: int, price: float) -> dict:
        r = await self.db.execute(
            select(MapPolicy).where(MapPolicy.product_id == product_id, MapPolicy.is_active == True)
        )
        policy = r.scalar_one_or_none()
        if not policy:
            return {"violation": False, "message": "No MAP policy set"}
        if price < policy.min_advertised_price:
            return {"violation": True, "message": f"Price {price} below MAP {policy.min_advertised_price}", "policy_id": policy.id}
        return {"violation": False, "message": "Price compliant"}

    async def list_violations(self) -> list[MapViolation]:
        r = await self.db.execute(select(MapViolation).order_by(MapViolation.created_at.desc()))
        return list(r.scalars().all())

    async def create_violation(self, policy_id: int, reported_price: float, reported_by: int) -> MapViolation:
        mv = MapViolation(policy_id=policy_id, reported_price=reported_price, reported_by=reported_by)
        self.db.add(mv)
        return mv


class CounterfeitRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def report(self, product_id: int, reported_by: int, **kwargs) -> CounterfeitReport:
        cr = CounterfeitReport(product_id=product_id, reported_by=reported_by, **kwargs)
        self.db.add(cr)
        return cr

    async def list_reports(self) -> list[CounterfeitReport]:
        r = await self.db.execute(select(CounterfeitReport).order_by(CounterfeitReport.created_at.desc()))
        return list(r.scalars().all())

    async def resolve_report(self, report_id: int) -> CounterfeitReport | None:
        r = await self.db.execute(select(CounterfeitReport).where(CounterfeitReport.id == report_id))
        cr = r.scalar_one_or_none()
        if cr:
            cr.status = "resolved"
            cr.resolved_at = datetime.now(timezone.utc)
        return cr


class ProductComplianceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_certificate(self, product_id: int, **kwargs) -> ProductCompliance:
        pc = ProductCompliance(product_id=product_id, **kwargs)
        self.db.add(pc)
        return pc

    async def list_certificates(self, product_id: int) -> list[ProductCompliance]:
        r = await self.db.execute(
            select(ProductCompliance).where(ProductCompliance.product_id == product_id)
            .order_by(ProductCompliance.created_at.desc())
        )
        return list(r.scalars().all())

    async def get_expiring(self, days: int = 30) -> list[ProductCompliance]:
        from sqlalchemy import func
        cutoff = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(ProductCompliance).where(
                ProductCompliance.expires_at != None,
                ProductCompliance.expires_at <= func.now() + func.make_interval(0, 0, 0, days),
            )
        )
        return list(r.scalars().all())


class ProductRecallRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_recall(self, product_id: int, reason: str, **kwargs) -> ProductRecall:
        pr = ProductRecall(product_id=product_id, reason=reason, **kwargs)
        self.db.add(pr)
        return pr

    async def list_active(self) -> list[ProductRecall]:
        r = await self.db.execute(
            select(ProductRecall).where(ProductRecall.status == "active")
            .order_by(ProductRecall.created_at.desc())
        )
        return list(r.scalars().all())

    async def resolve_recall(self, recall_id: int) -> ProductRecall | None:
        r = await self.db.execute(select(ProductRecall).where(ProductRecall.id == recall_id))
        pr = r.scalar_one_or_none()
        if pr:
            pr.status = "resolved"
        return pr


class PolicyViolationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def report_violation(self, seller_id: int, violation_type: str, **kwargs) -> PolicyViolation:
        pv = PolicyViolation(seller_id=seller_id, violation_type=violation_type, **kwargs)
        self.db.add(pv)
        return pv

    async def list_by_seller(self, seller_id: int = None) -> list[PolicyViolation]:
        q = select(PolicyViolation)
        if seller_id:
            q = q.where(PolicyViolation.seller_id == seller_id)
        q = q.order_by(PolicyViolation.created_at.desc())
        r = await self.db.execute(q)
        return list(r.scalars().all())

    async def resolve(self, violation_id: int) -> PolicyViolation | None:
        r = await self.db.execute(select(PolicyViolation).where(PolicyViolation.id == violation_id))
        pv = r.scalar_one_or_none()
        if pv:
            pv.status = "resolved"
            pv.resolved_at = datetime.now(timezone.utc)
        return pv
