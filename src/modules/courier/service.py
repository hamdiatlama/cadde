"""Business logic for courier domain.

Coordinates repository, geo utilities, events, and WebSocket broadcasting.
"""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.courier.repository import CourierRepository
from src.modules.courier.geo import haversine_km, estimate_duration_seconds, detect_gps_anomaly
from src.modules.courier.events import publish_event, CourierEvent
from src.modules.courier.websocket_manager import manager as ws_manager
from src.modules.courier.models import Courier
from src.core.cache import cache


class CourierService:
    def __init__(self, db: AsyncSession):
        self.repo = CourierRepository(db)

    # ── Location Update ──────────────────────────────────────────

    async def update_location(
        self,
        courier: Courier,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
        source: str = "gps",
    ) -> dict:
        prev_lat = courier.current_latitude
        prev_lon = courier.current_longitude
        prev_time = courier.last_location_update

        anomaly = detect_gps_anomaly(
            latitude, longitude,
            prev_lat, prev_lon, prev_time,
            speed_kmh, accuracy_m,
        )

        await self.repo.update_location(courier, latitude, longitude, speed_kmh, heading, accuracy_m)
        await cache.geoadd("couriers:live", longitude, latitude, str(courier.id))
        await self.repo.update_spoofing_score(courier, anomaly["score"], anomaly["is_anomaly"], anomaly["anomalies"])
        await self.repo.log_location_history(
            courier.id, latitude, longitude, speed_kmh, heading, accuracy_m,
            source=source, was_anomaly=anomaly["is_anomaly"],
        )

        if anomaly["is_anomaly"]:
            await publish_event(CourierEvent.COURIER_GPS_ANOMALY, {
                "courier_id": courier.id,
                "user_id": courier.user_id,
                "anomalies": anomaly["anomalies"],
                "score": anomaly["score"],
            })

        return {
            "latitude": latitude,
            "longitude": longitude,
            "speed_kmh": speed_kmh,
            "heading": heading,
            "anomaly_detected": anomaly["is_anomaly"],
            "spoofing_score": courier.gps_spoofing_score,
        }

    # ── Nearby Couriers (Redis Geo + DB fallback) ───────────────

    async def find_nearby(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 5,
    ) -> list[dict]:
        cached = await cache.georadius("couriers:live", longitude, latitude, radius_km)
        if cached:
            return [
                {"id": int(r["member"]), "latitude": r["latitude"],
                 "longitude": r["longitude"], "distance_km": round(r["distance_km"], 2)}
                for r in cached
            ]
        couriers = await self.repo.get_available_in_zone(latitude, longitude, radius_km)
        results = []
        for c in couriers:
            dist = haversine_km(latitude, longitude, c.current_latitude or 0, c.current_longitude or 0)
            results.append({
                "id": c.id,
                "user_id": c.user_id,
                "latitude": c.current_latitude,
                "longitude": c.current_longitude,
                "distance_km": round(dist, 2),
                "vehicle_type": c.vehicle_type,
                "rating": c.rating,
                "total_deliveries": c.total_deliveries,
            })
        results.sort(key=lambda x: x["distance_km"])
        return results

    # ── Assign Courier ───────────────────────────────────────────

    async def assign_courier(self, order_id: int) -> dict:
        order = await self.repo.get_order(order_id)
        if not order:
            raise ValueError("Siparis bulunamadi")
        if order.courier_id is not None:
            raise ValueError("Bu siparise zaten kurye atanmis")

        courier = await self.repo.get_nearest_available(
            order.delivery_latitude or 41.01,
            order.delivery_longitude or 28.98,
        )
        if not courier:
            raise ValueError("Müsait kurye bulunamadi")

        assigned = await self.repo.assign_to_order(courier, order_id)
        if not assigned:
            raise ValueError("Kurye atanamadi")

        dist = haversine_km(
            courier.current_latitude or order.delivery_latitude or 0,
            courier.current_longitude or order.delivery_longitude or 0,
            order.delivery_latitude or 0,
            order.delivery_longitude or 0,
        )
        eta = estimate_duration_seconds(dist)

        await publish_event(CourierEvent.COURIER_ASSIGNED, {
            "order_id": order_id,
            "courier_id": courier.id,
            "user_id": courier.user_id,
            "eta_seconds": eta,
        })

        await ws_manager.broadcast_status(order_id, "courier_assigned",
                                          courier_id=courier.id)

        return {
            "message": "Kurye atandi",
            "courier_id": courier.id,
            "order_id": order_id,
            "courier_latitude": courier.current_latitude,
            "courier_longitude": courier.current_longitude,
            "eta_seconds": eta,
        }

    # ── Complete Delivery ────────────────────────────────────────

    async def complete_delivery(self, order_id: int, courier_user_id: int) -> dict:
        order = await self.repo.complete_delivery(order_id, courier_user_id)
        if not order:
            raise ValueError("Siparis bulunamadi veya size ait degil")

        courier = await self.repo.get_by_user_id(courier_user_id)
        if courier:
            courier.is_available = True
            courier.status = "online"

            # Create earning record
            await self.repo.create_earning(
                courier_id=courier.id,
                order_id=order_id,
                delivery_fee=order.delivery_fee or 29.90,
            )

        await publish_event(CourierEvent.COURIER_DELIVERED, {
            "order_id": order_id,
            "courier_user_id": courier_user_id,
        })

        await ws_manager.broadcast_status(order_id, "delivered")

        return {"message": "Teslimat tamamlandi", "order_id": order_id}

    # ── Tracking ─────────────────────────────────────────────────

    async def get_tracking(self, order_id: int) -> dict:
        order = await self.repo.get_order(order_id)
        if not order:
            raise ValueError("Siparis bulunamadi")
        if not order.courier_id:
            return {"status": "not_assigned", "message": "Henüz kurye atanmadi"}

        courier = await self.repo.get_by_user_id(order.courier_id)
        if not courier:
            return {"status": "courier_not_found", "message": "Kurye profili bulunamadi"}

        history = await self.repo.get_location_history(courier.id, order_id)
        return {
            "status": "tracking",
            "courier_id": courier.id,
            "current_location": {
                "latitude": courier.current_latitude,
                "longitude": courier.current_longitude,
                "speed_kmh": courier.current_speed_kmh,
                "heading": courier.current_heading,
            },
            "last_update": courier.last_location_update.isoformat() if courier.last_location_update else None,
            "history": [
                {"latitude": h.latitude, "longitude": h.longitude,
                 "speed_kmh": h.speed_kmh, "heading": h.heading,
                 "timestamp": h.timestamp}
                for h in history
            ],
        }

    # ── Shifts ───────────────────────────────────────────────────

    async def start_shift(self, courier: Courier) -> dict:
        active = await self.repo.get_active_shift(courier.id)
        if active:
            raise ValueError("Zaten aktif bir mesainiz var")

        shift = await self.repo.start_shift(courier)
        courier.is_available = True
        courier.status = "online"

        await publish_event(CourierEvent.COURIER_SHIFT_STARTED, {
            "courier_id": courier.id,
            "shift_id": shift.id,
        })

        return {"status": "shift_started", "shift_id": shift.id}

    async def end_shift(self, courier: Courier) -> dict:
        active = await self.repo.get_active_shift(courier.id)
        if not active:
            raise ValueError("Aktif mesai bulunamadi")

        earnings = await self.repo.get_earnings_summary(courier.id)

        await self.repo.end_shift(active)
        active.orders_completed = courier.total_deliveries
        active.total_earned = earnings["total_earned"]
        courier.is_available = False
        courier.status = "offline"

        await publish_event(CourierEvent.COURIER_SHIFT_ENDED, {
            "courier_id": courier.id,
            "shift_id": active.id,
            "total_earned": earnings["total_earned"],
            "orders_completed": courier.total_deliveries,
        })

        return {
            "status": "shift_ended",
            "total_earned": earnings["total_earned"],
            "orders_completed": courier.total_deliveries,
        }

    # ── Earnings ─────────────────────────────────────────────────

    async def get_earnings(self, courier: Courier) -> dict:
        return await self.repo.get_earnings_summary(courier.id)

    # ── Spoofing Status ──────────────────────────────────────────

    async def get_spoofing_status(self, courier: Courier) -> dict:
        return {
            "courier_id": courier.id,
            "spoofing_score": courier.gps_spoofing_score or 0,
            "consecutive_anomalies": courier.consecutive_anomalies or 0,
            "is_suspicious": (courier.gps_spoofing_score or 0) >= 0.5,
            "last_anomaly_at": courier.last_anomaly_at.isoformat() if courier.last_anomaly_at else None,
        }
