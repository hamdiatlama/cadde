from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.commission.models import CommissionRule, CommissionTransaction


class CommissionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def set_commission_rule(self, rate: float, category_id: int = None, seller_id: int = None) -> CommissionRule:
        rule = CommissionRule(rate=rate, category_id=category_id, seller_id=seller_id, is_active=True)
        self.db.add(rule)
        return rule

    async def get_commission_rate(self, category_id: int = None, seller_id: int = None) -> float:
        if seller_id:
            r = await self.db.execute(
                select(CommissionRule).where(
                    CommissionRule.seller_id == seller_id,
                    CommissionRule.is_active == True,
                ).order_by(CommissionRule.created_at.desc()).limit(1)
            )
            rule = r.scalar_one_or_none()
            if rule:
                return rule.rate
        if category_id:
            r = await self.db.execute(
                select(CommissionRule).where(
                    CommissionRule.category_id == category_id,
                    CommissionRule.is_active == True,
                ).order_by(CommissionRule.created_at.desc()).limit(1)
            )
            rule = r.scalar_one_or_none()
            if rule:
                return rule.rate
        r = await self.db.execute(
            select(CommissionRule).where(
                CommissionRule.category_id.is_(None),
                CommissionRule.seller_id.is_(None),
                CommissionRule.is_active == True,
            ).order_by(CommissionRule.created_at.desc()).limit(1)
        )
        rule = r.scalar_one_or_none()
        return rule.rate if rule else 0.0

    async def calculate_commission(self, order_id: int, amount: float, seller_id: int) -> CommissionTransaction:
        rate = await self.get_commission_rate(seller_id=seller_id)
        if rate == 0:
            rate = await self.get_commission_rate(category_id=None)
        commission_amount = round(amount * rate / 100, 2)
        txn = CommissionTransaction(
            order_id=order_id, seller_id=seller_id,
            amount=commission_amount, rate=rate,
        )
        self.db.add(txn)
        return txn

    async def list_commission_transactions(self, seller_id: int, limit: int = 50):
        r = await self.db.execute(
            select(CommissionTransaction).where(CommissionTransaction.seller_id == seller_id)
            .order_by(CommissionTransaction.created_at.desc()).limit(limit)
        )
        return r.scalars().all()

    async def list_active_rules(self):
        r = await self.db.execute(
            select(CommissionRule).where(CommissionRule.is_active == True)
            .order_by(CommissionRule.created_at.desc())
        )
        return r.scalars().all()
