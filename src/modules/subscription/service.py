from datetime import datetime, timezone, timedelta
from src.modules.subscription.repository import SubscriptionRepository
from src.models.subscription import SubscriptionPlan, Subscription, SubscriptionDelivery

class SubscriptionService:
    def __init__(self, db):
        self.repo = SubscriptionRepository(db)

    async def list_plans(self):
        plans = await self.repo.list_active_plans()
        return [{
            "id": p.id, "name": p.name, "description": p.description,
            "interval_days": p.interval_days, "duration_months": p.duration_months,
            "price_per_delivery": p.price_per_delivery, "total_price": p.total_price,
            "delivery_count": p.duration_months * 30 // p.interval_days,
        } for p in plans]

    async def create_plan(self, name: str, interval_days: int, duration_months: int,
                           price_per_delivery: float, description: str = None, role: str = None):
        if role != "admin":
            return None, "Only admins can create plans"
        delivery_count = duration_months * 30 // interval_days
        total_price = round(price_per_delivery * delivery_count, 2)
        plan = SubscriptionPlan(
            name=name, description=description, interval_days=interval_days,
            duration_months=duration_months, price_per_delivery=price_per_delivery,
            total_price=total_price,
        )
        await self.repo.create_plan(plan)
        return {"id": plan.id, "name": plan.name, "delivery_count": delivery_count, "total_price": total_price}, None

    async def create_subscription(self, user_id: int, plan_id: int, seller_id: int, product_id: int,
                                   start_date: str = None, recipient_name: str = None,
                                   recipient_phone: str = None, delivery_address: str = None,
                                   notes: str = None, card_message: str = None, is_gift: bool = False):
        plan = await self.repo.get_plan(plan_id)
        if not plan:
            return None, "Plan not found"
        from src.models.product import Product
        pr = await self.repo.db.execute(
            __import__("sqlalchemy").select(Product).where(Product.id == product_id)
        )
        product = pr.scalar_one_or_none()
        if not product:
            return None, "Product not found"

        if start_date:
            try:
                start = datetime.fromisoformat(start_date)
            except ValueError:
                return None, "Invalid date format. Use ISO format (YYYY-MM-DD)"
        else:
            start = datetime.now(timezone.utc)
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)

        delivery_count = plan.duration_months * 30 // plan.interval_days
        end = start + timedelta(days=plan.interval_days * delivery_count)
        sub = Subscription(
            user_id=user_id, plan_id=plan_id, seller_id=seller_id, product_id=product_id,
            start_date=start, end_date=end, next_delivery_date=start,
            recipient_name=recipient_name, recipient_phone=recipient_phone,
            delivery_address=delivery_address, notes=notes, card_message=card_message,
            is_gift=is_gift,
        )
        await self.repo.create_subscription(sub)

        for i in range(delivery_count):
            delivery_date = start + timedelta(days=plan.interval_days * i)
            await self.repo.create_delivery(SubscriptionDelivery(
                subscription_id=sub.id, delivery_number=i + 1,
                scheduled_date=delivery_date, is_gift=is_gift,
            ))

        return {"id": sub.id, "plan": plan.name, "status": sub.status,
                "start_date": sub.start_date.isoformat(), "end_date": sub.end_date.isoformat(),
                "next_delivery": sub.next_delivery_date.isoformat() if sub.next_delivery_date else None,
                "delivery_count": delivery_count, "total_price": plan.total_price,
                "message": f"Subscription started! {delivery_count} deliveries planned."}, None

    async def get_my_subscriptions(self, user_id: int):
        subs = await self.repo.list_user_subscriptions(user_id)
        result = []
        for s in subs:
            total_d, completed_d = await self.repo.get_delivery_stats(s.id)
            result.append({
                "id": s.id, "plan_id": s.plan_id, "product_id": s.product_id,
                "status": s.status,
                "start_date": s.start_date.isoformat() if s.start_date else None,
                "end_date": s.end_date.isoformat() if s.end_date else None,
                "next_delivery": s.next_delivery_date.isoformat() if s.next_delivery_date else None,
                "total_deliveries": total_d, "completed_deliveries": completed_d or 0,
                "recipient_name": s.recipient_name, "delivery_address": s.delivery_address,
                "is_gift": s.is_gift, "created_at": s.created_at.isoformat() if s.created_at else None,
            })
        return result

    async def get_subscription(self, sub_id: int, user_id: int, role: str):
        sub = await self.repo.get_subscription(sub_id)
        if not sub:
            return None
        if sub.user_id != user_id and role != "admin":
            return None
        return {"id": sub.id, "plan_id": sub.plan_id, "product_id": sub.product_id,
                "status": sub.status,
                "start_date": sub.start_date.isoformat() if sub.start_date else None,
                "end_date": sub.end_date.isoformat() if sub.end_date else None,
                "next_delivery": sub.next_delivery_date.isoformat() if sub.next_delivery_date else None,
                "recipient_name": sub.recipient_name, "recipient_phone": sub.recipient_phone,
                "delivery_address": sub.delivery_address, "notes": sub.notes,
                "card_message": sub.card_message, "is_gift": sub.is_gift}

    async def pause_subscription(self, sub_id: int, user_id: int):
        sub = await self.repo.get_subscription(sub_id)
        if not sub or sub.user_id != user_id:
            return None, "Subscription not found"
        if sub.status != "active":
            return None, f"Cannot pause subscription in '{sub.status}' status"
        sub.status = "paused"
        sub.paused_at = datetime.now(timezone.utc)
        return {"id": sub.id, "status": "paused", "message": "Subscription paused. Resume anytime."}, None

    async def resume_subscription(self, sub_id: int, user_id: int):
        sub = await self.repo.get_subscription(sub_id)
        if not sub or sub.user_id != user_id:
            return None, "Subscription not found"
        if sub.status != "paused":
            return None, "Subscription is not paused"
        sub.status = "active"
        if sub.paused_at:
            pause_duration = datetime.now(timezone.utc) - sub.paused_at
            if sub.next_delivery_date:
                sub.next_delivery_date += pause_duration
        sub.paused_at = None
        return {"id": sub.id, "status": "active", "message": "Subscription resumed!"}, None

    async def cancel_subscription(self, sub_id: int, user_id: int, reason: str = None):
        sub = await self.repo.get_subscription(sub_id)
        if not sub or sub.user_id != user_id:
            return None, "Subscription not found"
        if sub.status in ("cancelled", "completed"):
            return None, f"Subscription already {sub.status}"
        sub.status = "cancelled"
        sub.cancelled_at = datetime.now(timezone.utc)
        sub.cancel_reason = reason
        return {"id": sub.id, "status": "cancelled", "message": "Subscription cancelled."}, None

    async def get_deliveries(self, sub_id: int, user_id: int, role: str):
        sub = await self.repo.get_subscription(sub_id)
        if not sub:
            return None
        if sub.user_id != user_id and role != "admin":
            return None
        deliveries = await self.repo.get_deliveries(sub_id)
        return [{"id": d.id, "delivery_number": d.delivery_number,
                 "scheduled_date": d.scheduled_date.isoformat() if d.scheduled_date else None,
                 "status": d.status, "order_id": d.order_id, "is_gift": d.is_gift}
                for d in deliveries]

    async def skip_delivery(self, delivery_id: int, user_id: int):
        delivery = await self.repo.get_delivery(delivery_id)
        if not delivery:
            return None, "Delivery not found"
        sub = await self.repo.get_subscription(delivery.subscription_id)
        if not sub or sub.user_id != user_id:
            return None, "Access denied"
        if delivery.status != "pending":
            return None, f"Delivery already {delivery.status}"
        delivery.status = "skipped"
        return {"id": delivery.id, "status": "skipped", "message": f"Delivery #{delivery.delivery_number} skipped"}, None

    async def change_product(self, sub_id: int, user_id: int, new_product_id: int):
        sub = await self.repo.get_subscription(sub_id)
        if not sub or sub.user_id != user_id:
            return None, "Subscription not found"
        from src.models.product import Product
        pr = await self.repo.db.execute(
            __import__("sqlalchemy").select(Product).where(Product.id == new_product_id)
        )
        if not pr.scalar_one_or_none():
            return None, "Product not found"
        sub.product_id = new_product_id
        return {"id": sub.id, "product_id": new_product_id, "message": "Product changed for future deliveries"}, None
