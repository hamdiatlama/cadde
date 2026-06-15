from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.abandoned_cart.models import AbandonedCart, CartReminderTemplate


class AbandonedCartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def mark_abandoned(self, user_id: int, cart_data: str, total: int):
        r = await self.db.execute(select(AbandonedCart).where(AbandonedCart.user_id == user_id, AbandonedCart.recovered == False))
        existing = r.scalar_one_or_none()
        if existing:
            existing.cart_data = cart_data
            existing.total = total
            return existing
        ac = AbandonedCart(user_id=user_id, cart_data=cart_data, total=total)
        self.db.add(ac); return ac

    async def get_abandoned_carts(self, hours: int = 24):
        from sqlalchemy import func
        from datetime import datetime, timezone, timedelta
        cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
        r = await self.db.execute(
            select(AbandonedCart).where(
                AbandonedCart.recovered == False,
                AbandonedCart.created_at <= cutoff,
                AbandonedCart.reminder_sent == False
            )
        )
        return r.scalars().all()

    async def mark_reminder_sent(self, cart_id: int):
        r = await self.db.execute(select(AbandonedCart).where(AbandonedCart.id == cart_id))
        ac = r.scalar_one_or_none()
        if ac:
            ac.reminder_sent = True
            ac.reminder_count = (ac.reminder_count or 0) + 1
            from sqlalchemy import func
            ac.last_reminder_at = func.now()

    async def mark_recovered(self, cart_id: int, order_id: int):
        r = await self.db.execute(select(AbandonedCart).where(AbandonedCart.id == cart_id))
        ac = r.scalar_one_or_none()
        if ac:
            ac.recovered = True
            ac.recovered_order_id = order_id

    async def create_reminder_template(self, name: str, subject: str, body: str, delay_hours: int = 24):
        t = CartReminderTemplate(name=name, subject=subject, body=body, delay_hours=delay_hours)
        self.db.add(t); return t

    async def get_active_reminder_templates(self):
        r = await self.db.execute(select(CartReminderTemplate).where(CartReminderTemplate.is_active == True))
        return r.scalars().all()
