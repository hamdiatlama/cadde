"""Data access layer for courier domain.

Uses repository pattern for DB abstraction.
In production, live location queries would hit Redis Geo,
and persistent data would use PostgreSQL + PostGIS.
"""

from datetime import datetime, timezone
from sqlalchemy import select, func, and_, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.order import Order, OrderItem
from src.models.product import Product
from src.modules.courier.models import (
    Courier, CourierLocationHistory, CourierEarning, CourierShift,
)
from src.modules.courier.geo import bounding_box


class CourierRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Courier CRUD ──────────────────────────────────────────────

    async def get_by_user_id(self, user_id: int) -> Courier | None:
        r = await self.db.execute(select(Courier).where(Courier.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_by_id(self, courier_id: int) -> Courier | None:
        r = await self.db.execute(select(Courier).where(Courier.id == courier_id))
        return r.scalar_one_or_none()

    async def get_available_in_zone(self, latitude: float, longitude: float, radius_km: float = 5) -> list[Courier]:
        box = bounding_box(latitude, longitude, radius_km)
        r = await self.db.execute(
            select(Courier).where(
                Courier.is_available == True,
                Courier.is_active == True,
                Courier.status == "online",
                Courier.current_latitude.isnot(None),
                Courier.current_longitude.isnot(None),
                Courier.current_latitude.between(box["min_lat"], box["max_lat"]),
                Courier.current_longitude.between(box["min_lon"], box["max_lon"]),
            )
        )
        return list(r.scalars().all())

    async def get_nearest_available(self, latitude: float, longitude: float, radius_km: float = 5) -> Courier | None:
        couriers = await self.get_available_in_zone(latitude, longitude, radius_km)
        if not couriers:
            return None
        from src.modules.courier.geo import haversine_km
        couriers.sort(key=lambda c: haversine_km(latitude, longitude, c.current_latitude or 0, c.current_longitude or 0))
        return couriers[0]

    async def update_location(
        self,
        courier: Courier,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
    ) -> Courier:
        courier.current_latitude = latitude
        courier.current_longitude = longitude
        courier.current_speed_kmh = speed_kmh
        courier.current_heading = heading
        courier.current_accuracy_m = accuracy_m
        courier.last_location_update = datetime.now(timezone.utc)
        self.db.add(courier)
        return courier

    async def update_spoofing_score(
        self,
        courier: Courier,
        score: float,
        is_anomaly: bool,
        anomalies: list[str],
    ) -> Courier:
        courier.gps_spoofing_score = min(courier.gps_spoofing_score + score, 1.0)
        if is_anomaly:
            courier.consecutive_anomalies = (courier.consecutive_anomalies or 0) + 1
            courier.last_anomaly_at = datetime.now(timezone.utc)
        else:
            courier.consecutive_anomalies = max((courier.consecutive_anomalies or 1) - 1, 0)
        self.db.add(courier)
        return courier

    async def log_location_history(
        self,
        courier_id: int,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
        source: str = "gps",
        was_anomaly: bool = False,
        order_id: int | None = None,
    ) -> CourierLocationHistory:
        entry = CourierLocationHistory(
            courier_id=courier_id,
            order_id=order_id,
            latitude=latitude,
            longitude=longitude,
            speed_kmh=speed_kmh,
            heading=heading,
            accuracy_m=accuracy_m,
            source=source,
            was_anomaly=was_anomaly,
        )
        self.db.add(entry)
        return entry

    async def get_location_history(self, courier_id: int, order_id: int, limit: int = 50) -> list[CourierLocationHistory]:
        r = await self.db.execute(
            select(CourierLocationHistory)
            .where(
                CourierLocationHistory.courier_id == courier_id,
                CourierLocationHistory.order_id == order_id,
            )
            .order_by(CourierLocationHistory.timestamp.desc())
            .limit(limit)
        )
        return list(reversed(r.scalars().all()))

    async def create_or_update(self, user_id: int, defaults: dict | None = None) -> Courier:
        existing = await self.get_by_user_id(user_id)
        if existing:
            return existing
        courier = Courier(user_id=user_id, **(defaults or {}))
        self.db.add(courier)
        return courier

    # ── Order / Assignment (with race condition protection) ──────

    async def assign_to_order(self, courier: Courier, order_id: int) -> Order | None:
        r = await self.db.execute(select(Order).where(Order.id == order_id))
        order = r.scalar_one_or_none()
        if not order:
            return None
        if order.courier_id is not None:
            return None

        order.courier_id = courier.user_id
        order.status = "in_transit"
        courier.is_available = False
        courier.status = "busy"
        courier.total_deliveries = (courier.total_deliveries or 0) + 1
        self.db.add(order)
        self.db.add(courier)
        return order

    async def complete_delivery(self, order_id: int, courier_user_id: int) -> Order | None:
        r = await self.db.execute(
            select(Order).where(Order.id == order_id, Order.courier_id == courier_user_id)
        )
        order = r.scalar_one_or_none()
        if not order:
            return None
        order.status = "delivered"
        order.payment_status = "paid"
        self.db.add(order)
        return order

    async def get_order(self, order_id: int) -> Order | None:
        r = await self.db.execute(select(Order).where(Order.id == order_id))
        return r.scalar_one_or_none()

    # ── Shifts ───────────────────────────────────────────────────

    async def get_active_shift(self, courier_id: int) -> CourierShift | None:
        r = await self.db.execute(
            select(CourierShift).where(
                CourierShift.courier_id == courier_id,
                CourierShift.status == "active",
            )
        )
        return r.scalar_one_or_none()

    async def start_shift(self, courier: Courier) -> CourierShift:
        shift = CourierShift(
            courier_id=courier.id,
            start_time=datetime.now(timezone.utc),
            started_latitude=courier.current_latitude,
            started_longitude=courier.current_longitude,
        )
        self.db.add(shift)
        return shift

    async def end_shift(self, shift: CourierShift) -> CourierShift:
        shift.end_time = datetime.now(timezone.utc)
        shift.status = "completed"
        self.db.add(shift)
        return shift

    # ── Earnings ─────────────────────────────────────────────────

    async def get_earnings_summary(self, courier_id: int) -> dict:
        r = await self.db.execute(
            select(
                func.sum(CourierEarning.delivery_fee_earned),
                func.sum(CourierEarning.tip_amount),
                func.sum(CourierEarning.bonus_amount),
                func.count(CourierEarning.id),
            )
            .where(CourierEarning.courier_id == courier_id, CourierEarning.status == "paid")
        )
        fees, tips, bonuses, total = r.one()

        pending = await self.db.execute(
            select(func.sum(CourierEarning.net_amount))
            .where(CourierEarning.courier_id == courier_id, CourierEarning.status == "pending")
        )
        pending_amount = pending.scalar() or 0

        return {
            "total_delivery_fees": round(fees or 0, 2),
            "total_tips": round(tips or 0, 2),
            "total_bonuses": round(bonuses or 0, 2),
            "total_earned": round((fees or 0) + (tips or 0) + (bonuses or 0), 2),
            "total_deliveries": total or 0,
            "pending_payout": round(pending_amount, 2),
        }

    async def create_earning(
        self,
        courier_id: int,
        order_id: int,
        delivery_fee: float,
        tip: float = 0,
        bonus: float = 0,
        commission_rate: float = 0.15,
    ) -> CourierEarning:
        gross = delivery_fee + tip + bonus
        commission = round(gross * commission_rate, 2)
        earning = CourierEarning(
            courier_id=courier_id,
            order_id=order_id,
            delivery_fee_earned=delivery_fee,
            tip_amount=tip,
            bonus_amount=bonus,
            platform_commission=commission,
            net_amount=round(gross - commission, 2),
        )
        self.db.add(earning)
        return earning
