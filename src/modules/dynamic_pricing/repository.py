from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from src.modules.dynamic_pricing.models import PricingRule, PriceHistory, InventoryForecast
from src.modules.store.models import Product


class PricingRuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, rule_data: dict) -> PricingRule:
        rule = PricingRule(**rule_data)
        self.db.add(rule)
        return rule

    async def list_all(self, seller_id: int = None):
        q = select(PricingRule)
        if seller_id:
            q = q.where(PricingRule.seller_id == seller_id)
        q = q.order_by(PricingRule.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def toggle(self, rule_id: int):
        r = await self.db.execute(select(PricingRule).where(PricingRule.id == rule_id))
        rule = r.scalar_one_or_none()
        if rule:
            rule.is_active = not rule.is_active
        return rule

    async def apply_rules(self, product_id: int) -> float:
        r = await self.db.execute(select(PricingRule).where(
            PricingRule.product_id == product_id, PricingRule.is_active == True
        ))
        rules = r.scalars().all()
        if not rules:
            raise ValueError("No active rules found for this product")
        pr = await self.db.execute(select(Product).where(Product.id == product_id))
        product = pr.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")
        from decimal import Decimal
        new_price = float(product.price)
        cost = float(product.cost_price or product.price * 0.7)
        for rule in rules:
            if rule.rule_type == "demand_based":
                new_price *= 1 + (rule.adjustment_rate / 100)
            elif rule.rule_type == "competitor_based":
                new_price *= 1 - (rule.adjustment_rate / 200)
            elif rule.rule_type == "stock_based":
                new_price *= 1 - (rule.adjustment_rate / 100)
            elif rule.rule_type == "time_based":
                new_price *= 1 + (rule.adjustment_rate / 100)
            if rule.min_price:
                new_price = max(new_price, rule.min_price)
            if rule.max_price:
                new_price = min(new_price, rule.max_price)
        return round(new_price, 2)


class PriceHistoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record_change(self, product_id: int, old_price: float, new_price: float, reason: str) -> PriceHistory:
        ph = PriceHistory(product_id=product_id, old_price=old_price, new_price=new_price, reason=reason)
        self.db.add(ph)
        return ph

    async def get_history(self, product_id: int, limit: int = 50):
        r = await self.db.execute(
            select(PriceHistory).where(PriceHistory.product_id == product_id)
            .order_by(PriceHistory.changed_at.desc()).limit(limit)
        )
        return r.scalars().all()


class InventoryForecastRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_forecast(self, product_id: int):
        from src.modules.ecommerce.order.models import Order, OrderItem
        cut = datetime.now(timezone.utc) - timedelta(days=30)
        r = await self.db.execute(
            select(func.coalesce(func.sum(OrderItem.quantity), 0))
            .join(Order, OrderItem.order_id == Order.id)
            .where(OrderItem.product_id == product_id, Order.created_at >= cut,
                   Order.status == "completed")
        )
        total_sold = r.scalar() or 0
        avg_daily = total_sold / 30.0
        predicted_demand = int(avg_daily * 1.2 * 30)

        forecast = InventoryForecast(
            product_id=product_id,
            forecast_date=datetime.now(timezone.utc) + timedelta(days=30),
            predicted_demand=predicted_demand,
            confidence=0.8 if total_sold > 10 else 0.5,
            reorder_point=int(avg_daily * 7),
            suggested_order_qty=max(predicted_demand - int(avg_daily * 7), 0)
        )
        self.db.add(forecast)
        return forecast

    async def get_forecast(self, product_id: int):
        r = await self.db.execute(
            select(InventoryForecast).where(InventoryForecast.product_id == product_id)
            .order_by(InventoryForecast.calculated_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()
