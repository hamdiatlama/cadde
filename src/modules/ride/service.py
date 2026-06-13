from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.geo import routing


def _ensure_tz(dt: datetime | None) -> datetime | None:
    if dt is not None and dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt

from src.modules.ride.repository import RideRepository
from src.modules.ride.geo import haversine_km, estimate_duration_seconds, detect_gps_anomaly
from src.modules.ride.events import publish_event, RideEvent
from src.modules.ride.websocket_manager import manager as ws_manager
from src.modules.ride.models import Driver, Ride

BASE_FARE_TL = 19.90
PER_KM_RATE_TL = 8.50
SURGE_THRESHOLD_DRIVERS = 3
SURGE_MULTIPLIERS = [1.0, 1.2, 1.5, 2.0, 2.5]
MAX_CANCELLATIONS_BEFORE_PENALTY = 3


def calculate_fare(dist_km: float, multiplier: float = 1.0) -> float:
    return round((BASE_FARE_TL + dist_km * PER_KM_RATE_TL) * multiplier, 2)


class RideService:
    def __init__(self, db: AsyncSession):
        self.repo = RideRepository(db)

    # ── Create Ride ────────────────────────────────────────────

    async def create_ride(self, customer_id: int, data) -> dict:
        osrm_result = await routing.route(
            (data.pickup_latitude, data.pickup_longitude),
            (data.dropoff_latitude, data.dropoff_longitude),
        )
        if osrm_result:
            dist_km = osrm_result["distance_km"]
            eta_seconds = osrm_result["duration_seconds"]
        else:
            dist_km = haversine_km(
                data.pickup_latitude, data.pickup_longitude,
                data.dropoff_latitude, data.dropoff_longitude,
            )
            eta_seconds = estimate_duration_seconds(dist_km)

        nearby = await self.repo.get_nearby_available_drivers(
            data.pickup_latitude, data.pickup_longitude, 5
        )
        available_drivers = len(nearby)

        surge_idx = min(available_drivers // SURGE_THRESHOLD_DRIVERS, len(SURGE_MULTIPLIERS) - 1)
        surge_multiplier = SURGE_MULTIPLIERS[surge_idx]
        estimated_fare = calculate_fare(dist_km, surge_multiplier)

        ride = await self.repo.create_ride(
            customer_id=customer_id,
            status="waiting_for_driver",
            pickup_address=data.pickup_address,
            pickup_latitude=data.pickup_latitude,
            pickup_longitude=data.pickup_longitude,
            dropoff_address=data.dropoff_address,
            dropoff_latitude=data.dropoff_latitude,
            dropoff_longitude=data.dropoff_longitude,
            estimated_fare=estimated_fare,
            surge_multiplier=surge_multiplier,
            optimal_distance_km=round(dist_km, 2),
            eta_at_booking=eta_seconds,
            payment_method=data.payment_method,
            notes=data.notes,
        )

        await publish_event(RideEvent.RIDE_CREATED, {
            "ride_id": ride.id,
            "customer_id": customer_id,
            "estimated_fare": estimated_fare,
        })

        return ride

    # ── Accept Ride ────────────────────────────────────────────

    async def accept_ride(self, ride_id: int, driver: Driver) -> Ride:
        ride = await self.repo.get_ride_for_accept(ride_id)
        if not ride:
            raise ValueError("Ride not found or already taken")

        if not driver.is_available:
            raise ValueError("You are not available for rides")

        now = datetime.now(timezone.utc)
        penalty_until = _ensure_tz(driver.penalty_until)
        if penalty_until and penalty_until > now:
            raise ValueError("You are under a time-based penalty. Please wait.")

        d_dist = haversine_km(
            driver.current_latitude or ride.pickup_latitude,
            driver.current_longitude or ride.pickup_longitude,
            ride.pickup_latitude, ride.pickup_longitude,
        ) if driver.current_latitude else 0

        ride = await self.repo.accept_ride(ride, driver, d_dist)

        await publish_event(RideEvent.RIDE_ACCEPTED, {
            "ride_id": ride.id,
            "driver_id": driver.id,
            "driver_distance_km": round(d_dist, 2),
        })

        await ws_manager.broadcast_status(ride.id, "accepted", driver_id=driver.id)

        return ride

    # ── Reject Ride ────────────────────────────────────────────

    async def reject_ride(self, ride_id: int, driver: Driver) -> Ride:
        ride = await self.repo.get_ride_for_accept(ride_id)
        if not ride:
            raise ValueError("Ride not found or already taken")

        ride = await self.repo.reject_ride(ride, driver)

        if (driver.cancelled_rides or 0) >= MAX_CANCELLATIONS_BEFORE_PENALTY:
            await self.repo.apply_penalty(driver)

        await publish_event(RideEvent.RIDE_REJECTED, {
            "ride_id": ride.id,
            "driver_id": driver.id,
            "cancelled_rides": driver.cancelled_rides,
        })

        return ride

    # ── Driver Arrived ─────────────────────────────────────────

    async def driver_arrived(self, ride_id: int, driver: Driver) -> Ride:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.driver_id != driver.id or ride.status != "accepted":
            raise ValueError("Ride not found or not in accepted status")

        wait_seconds = 0
        accepted_at = _ensure_tz(ride.accepted_at)
        if accepted_at:
            wait_seconds = int((datetime.now(timezone.utc) - accepted_at).total_seconds())

        ride = await self.repo.mark_arrived(ride, wait_seconds)

        await publish_event(RideEvent.RIDE_ARRIVED, {
            "ride_id": ride.id,
            "driver_id": driver.id,
            "wait_seconds": wait_seconds,
        })

        await ws_manager.broadcast_status(ride.id, "arrived")

        return ride

    # ── Start Ride ─────────────────────────────────────────────

    async def start_ride(self, ride_id: int, driver: Driver) -> Ride:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.driver_id != driver.id or ride.status != "arrived":
            raise ValueError("Ride not found or driver has not arrived yet")

        ride = await self.repo.mark_started(ride)

        await publish_event(RideEvent.RIDE_STARTED, {
            "ride_id": ride.id,
            "driver_id": driver.id,
        })

        await ws_manager.broadcast_status(ride.id, "in_progress")

        return ride

    # ── Complete Ride ──────────────────────────────────────────

    async def complete_ride(self, ride_id: int, driver: Driver, actual_lat: float | None, actual_lon: float | None) -> Ride:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.driver_id != driver.id or ride.status != "in_progress":
            raise ValueError("Ride not found or not in progress")

        actual_dist = None
        if actual_lat and actual_lon:
            actual_dist = haversine_km(
                ride.pickup_latitude, ride.pickup_longitude,
                actual_lat, actual_lon,
            )

        ride = await self.repo.complete_ride(ride, driver, actual_dist)

        await publish_event(RideEvent.RIDE_COMPLETED, {
            "ride_id": ride.id,
            "driver_id": driver.id,
            "actual_fare": ride.actual_fare,
            "actual_distance_km": ride.actual_distance_km,
        })

        await ws_manager.broadcast_status(ride.id, "completed")

        return ride

    # ── Cancel Ride (customer) ─────────────────────────────────

    async def cancel_ride(self, ride_id: int, customer_id: int, reason: str) -> Ride:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id:
            raise ValueError("Ride not found")
        if ride.status not in ("waiting_for_driver", "accepted"):
            raise ValueError(f"Cannot cancel ride in '{ride.status}' status")

        ride = await self.repo.cancel_ride(ride, reason, "customer")

        await publish_event(RideEvent.RIDE_CANCELLED, {
            "ride_id": ride.id,
            "customer_id": customer_id,
            "reason": reason,
        })

        await ws_manager.broadcast_status(ride.id, "cancelled")

        return ride

    # ── Safety Operations ──────────────────────────────────────

    async def confirm_safety(self, ride_id: int, customer_id: int, plate_ok: bool, photo_ok: bool) -> dict:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id:
            raise ValueError("Ride not found")

        await self.repo.create_or_update_safety(
            ride_id=ride.id,
            driver_plate_confirmed=plate_ok,
            driver_photo_confirmed=photo_ok,
        )
        return {"status": "confirmed", "plate_ok": plate_ok, "photo_ok": photo_ok}

    async def set_emergency_contact(self, ride_id: int, customer_id: int, phone: str) -> dict:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id:
            raise ValueError("Ride not found")

        await self.repo.create_or_update_safety(
            ride_id=ride.id,
            emergency_contact_phone=phone,
        )
        return {"status": "emergency_contact_set", "phone": phone}

    async def report_incident(self, ride_id: int, customer_id: int, incident_type: str, description: str) -> dict:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id:
            raise ValueError("Ride not found")

        await self.repo.create_or_update_safety(
            ride_id=ride.id,
            incident_reported=True,
            incident_type=incident_type,
            incident_description=description,
            reported_at=datetime.now(timezone.utc),
        )

        await publish_event(RideEvent.RIDE_INCIDENT_REPORTED, {
            "ride_id": ride.id,
            "customer_id": customer_id,
            "incident_type": incident_type,
        })

        return {"status": "incident_reported", "incident_type": incident_type}

    async def share_ride(self, ride_id: int, customer_id: int) -> dict:
        import secrets
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id:
            raise ValueError("Ride not found")

        share_token = secrets.token_urlsafe(16)
        await self.repo.create_or_update_safety(
            ride_id=ride.id,
            share_link=share_token,
        )
        return {
            "status": "share_link_created",
            "share_url": f"/rides/share/{share_token}",
        }

    # ── Rating ─────────────────────────────────────────────────

    async def rate_ride(self, ride_id: int, customer_id: int, rating: int, comment: str | None, categories: str | None) -> dict:
        ride = await self.repo.get_ride_by_id(ride_id)
        if not ride or ride.customer_id != customer_id or ride.status != "completed":
            raise ValueError("Completed ride not found")

        existing = await self.repo.get_existing_rating(ride.id, customer_id)
        if existing:
            raise ValueError("You have already rated this ride")

        await self.repo.create_rating(ride.id, customer_id, rating, comment, categories)

        if ride.driver_id:
            await self.repo.update_driver_rating(ride.driver_id)

        await publish_event(RideEvent.RIDE_RATED, {
            "ride_id": ride.id,
            "customer_id": customer_id,
            "rating": rating,
        })

        return {"status": "rated", "rating": rating}

    # ── Driver Location Update (with GPS spoofing) ──────────────

    async def update_driver_location(
        self,
        driver: Driver,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
        source: str = "gps",
    ) -> dict:
        prev_lat = driver.current_latitude
        prev_lon = driver.current_longitude
        prev_time = _ensure_tz(driver.last_location_update)

        anomaly = detect_gps_anomaly(
            latitude, longitude,
            prev_lat, prev_lon, prev_time,
            speed_kmh, accuracy_m,
        )

        await self.repo.update_driver_location(driver, latitude, longitude, speed_kmh, heading, accuracy_m)
        await self.repo.update_spoofing_score(driver, anomaly["score"], anomaly["is_anomaly"], anomaly["anomalies"])
        await self.repo.log_location_history(
            driver.id, latitude, longitude, speed_kmh, heading, accuracy_m,
            source=source, was_anomaly=anomaly["is_anomaly"],
        )

        if anomaly["is_anomaly"]:
            await publish_event(RideEvent.RIDE_GPS_ANOMALY, {
                "driver_id": driver.id,
                "user_id": driver.user_id,
                "anomalies": anomaly["anomalies"],
                "score": anomaly["score"],
            })

        return {
            "latitude": latitude,
            "longitude": longitude,
            "speed_kmh": speed_kmh,
            "heading": heading,
            "anomaly_detected": anomaly["is_anomaly"],
            "spoofing_score": driver.gps_spoofing_score,
        }

    # ── Spoofing Status ────────────────────────────────────────

    async def get_spoofing_status(self, driver: Driver) -> dict:
        return {
            "driver_id": driver.id,
            "spoofing_score": driver.gps_spoofing_score or 0,
            "consecutive_anomalies": driver.consecutive_anomalies or 0,
            "is_suspicious": (driver.gps_spoofing_score or 0) >= 0.5,
            "last_anomaly_at": driver.last_anomaly_at.isoformat() if driver.last_anomaly_at else None,
        }
