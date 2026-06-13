from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func, case
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.subscription import SubscriptionPlan, Subscription, SubscriptionDelivery

class SubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_active_plans(self):
        r = await self.db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.is_active == True)
            .order_by(SubscriptionPlan.price_per_delivery.asc())
        )
        return r.scalars().all()

    async def get_plan(self, plan_id: int):
        r = await self.db.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.id == plan_id, SubscriptionPlan.is_active == True)
        )
        return r.scalar_one_or_none()

    async def create_plan(self, plan: SubscriptionPlan):
        self.db.add(plan)

    async def get_subscription(self, sub_id: int):
        r = await self.db.execute(select(Subscription).where(Subscription.id == sub_id))
        return r.scalar_one_or_none()

    async def list_user_subscriptions(self, user_id: int):
        r = await self.db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
            .order_by(Subscription.created_at.desc())
        )
        return r.scalars().all()

    async def create_subscription(self, sub: Subscription):
        self.db.add(sub)

    async def create_delivery(self, delivery: SubscriptionDelivery):
        self.db.add(delivery)

    async def get_delivery_stats(self, sub_id: int):
        r = await self.db.execute(
            select(func.count(), func.sum(case((SubscriptionDelivery.status == "delivered", 1), else_=0)))
            .where(SubscriptionDelivery.subscription_id == sub_id)
        )
        return r.one()

    async def get_deliveries(self, sub_id: int):
        r = await self.db.execute(
            select(SubscriptionDelivery).where(SubscriptionDelivery.subscription_id == sub_id)
            .order_by(SubscriptionDelivery.delivery_number.asc())
        )
        return r.scalars().all()

    async def get_delivery(self, delivery_id: int):
        r = await self.db.execute(select(SubscriptionDelivery).where(SubscriptionDelivery.id == delivery_id))
        return r.scalar_one_or_none()
