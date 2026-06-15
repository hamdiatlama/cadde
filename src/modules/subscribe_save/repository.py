from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.subscribe_save.models import SubscriptionPlan, SubscriptionSaveOrder


class SubscribeSaveRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_plan(self, product_id: int, seller_id: int, interval_days: int,
                          discount_rate: float = 5, max_orders: int = None) -> SubscriptionPlan:
        p = SubscriptionPlan(product_id=product_id, seller_id=seller_id, interval_days=interval_days,
                             discount_rate=discount_rate, max_orders=max_orders)
        self.db.add(p); return p

    async def list_plans(self, product_id: int):
        r = await self.db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.product_id == product_id,
                                           SubscriptionPlan.is_active == True)
        )
        return r.scalars().all()

    async def subscribe(self, plan_id: int, user_id: int) -> SubscriptionSaveOrder:
        from datetime import datetime, timezone, timedelta
        r = await self.db.execute(select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id))
        plan = r.scalar_one_or_none()
        if not plan:
            return None
        next_date = datetime.now(timezone.utc) + timedelta(days=plan.interval_days)
        sub = SubscriptionSaveOrder(plan_id=plan_id, user_id=user_id, next_order_date=next_date)
        self.db.add(sub); return sub

    async def cancel_subscription(self, sub_id: int) -> SubscriptionSaveOrder:
        r = await self.db.execute(select(SubscriptionSaveOrder).where(SubscriptionSaveOrder.id == sub_id))
        sub = r.scalar_one_or_none()
        if sub:
            sub.is_active = False
        return sub

    async def get_user_subscriptions(self, user_id: int):
        r = await self.db.execute(
            select(SubscriptionSaveOrder).where(SubscriptionSaveOrder.user_id == user_id,
                                                SubscriptionSaveOrder.is_active == True)
        )
        return r.scalars().all()

    async def generate_orders(self) -> list:
        from datetime import datetime, timezone, timedelta
        from sqlalchemy import func
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(SubscriptionSaveOrder).where(SubscriptionSaveOrder.is_active == True,
                                                SubscriptionSaveOrder.next_order_date <= now)
        )
        subs = r.scalars().all()
        for sub in subs:
            sub.total_orders += 1
            r2 = await self.db.execute(select(SubscriptionPlan).where(SubscriptionPlan.id == sub.plan_id))
            plan = r2.scalar_one_or_none()
            if plan:
                sub.next_order_date = now + timedelta(days=plan.interval_days)
        return subs
