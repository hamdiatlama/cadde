from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.ride import Driver, DriverLocationHistory, Ride, RideSafety, RideRating
from src.models.user import User
from src.modules.ride.geo import bounding_box


class RideRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Driver CRUD ────────────────────────────────────────────

    async def get_driver_by_user_id(self, user_id: int) -> Driver | None:
        r = await self.db.execute(select(Driver).where(Driver.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_driver_by_id(self, driver_id: int) -> Driver | None:
        r = await self.db.execute(select(Driver).where(Driver.id == driver_id))
        return r.scalar_one_or_none()

    async def create_driver(self, user_id: int, **kwargs) -> Driver:
        existing = await self.get_driver_by_user_id(user_id)
        if existing:
            for k, v in kwargs.items():
                setattr(existing, k, v)
            return existing
        driver = Driver(user_id=user_id, **kwargs)
        self.db.add(driver)
        return driver

    async def update_driver_location(
        self,
        driver: Driver,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
    ) -> Driver:
        driver.current_latitude = latitude
        driver.current_longitude = longitude
        driver.current_speed_kmh = speed_kmh
        driver.current_heading = heading
        driver.current_accuracy_m = accuracy_m
        driver.last_location_update = datetime.now(timezone.utc)
        self.db.add(driver)
        return driver

    async def update_spoofing_score(
        self,
        driver: Driver,
        score: float,
        is_anomaly: bool,
        anomalies: list[str],
    ) -> Driver:
        driver.gps_spoofing_score = min((driver.gps_spoofing_score or 0) + score, 1.0)
        if is_anomaly:
            driver.consecutive_anomalies = (driver.consecutive_anomalies or 0) + 1
            driver.last_anomaly_at = datetime.now(timezone.utc)
        else:
            driver.consecutive_anomalies = max((driver.consecutive_anomalies or 1) - 1, 0)
        self.db.add(driver)
        return driver

    async def log_location_history(
        self,
        driver_id: int,
        latitude: float,
        longitude: float,
        speed_kmh: float = 0,
        heading: float = 0,
        accuracy_m: float = 0,
        source: str = "gps",
        was_anomaly: bool = False,
        ride_id: int | None = None,
    ) -> DriverLocationHistory:
        entry = DriverLocationHistory(
            driver_id=driver_id,
            ride_id=ride_id,
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

    async def get_nearby_available_drivers(
        self, latitude: float, longitude: float, radius_km: float = 5
    ) -> list[Driver]:
        now = datetime.now(timezone.utc)
        box = bounding_box(latitude, longitude, radius_km)
        r = await self.db.execute(
            select(Driver).where(
                Driver.is_available == True,
                Driver.is_active == True,
                Driver.current_latitude.isnot(None),
                Driver.current_longitude.isnot(None),
                Driver.current_latitude.between(box["min_lat"], box["max_lat"]),
                Driver.current_longitude.between(box["min_lon"], box["max_lon"]),
            )
        )
        drivers = list(r.scalars().all())
        # Filter out drivers under time-based penalty
        return [d for d in drivers if not d.penalty_until or d.penalty_until <= now]

    # ── Ride CRUD ──────────────────────────────────────────────

    async def create_ride(self, **kwargs) -> Ride:
        ride = Ride(**kwargs)
        self.db.add(ride)
        return ride

    async def get_ride_by_id(self, ride_id: int) -> Ride | None:
        r = await self.db.execute(select(Ride).where(Ride.id == ride_id))
        return r.scalar_one_or_none()

    async def get_ride_for_accept(self, ride_id: int) -> Ride | None:
        """Race-condition-safe: only fetches if still waiting_for_driver."""
        r = await self.db.execute(
            select(Ride).where(
                Ride.id == ride_id,
                Ride.status == "waiting_for_driver",
                Ride.driver_id.is_(None),
            )
        )
        return r.scalar_one_or_none()

    async def accept_ride(self, ride: Ride, driver: Driver, d_dist: float) -> Ride:
        ride.status = "accepted"
        ride.driver_id = driver.id
        ride.accepted_at = datetime.now(timezone.utc)
        ride.driver_distance_at_accept_km = round(d_dist, 2)
        driver.is_available = False
        self.db.add(ride)
        self.db.add(driver)
        return ride

    async def reject_ride(self, ride: Ride, driver: Driver) -> Ride:
        ride.status = "rejected_by_driver"
        ride.cancelled_by = "driver"
        driver.cancelled_rides = (driver.cancelled_rides or 0) + 1
        self.db.add(ride)
        self.db.add(driver)
        return ride

    async def mark_arrived(self, ride: Ride, wait_seconds: int) -> Ride:
        ride.status = "arrived"
        ride.arrived_at = datetime.now(timezone.utc)
        ride.actual_wait_seconds = wait_seconds
        self.db.add(ride)
        return ride

    async def mark_started(self, ride: Ride) -> Ride:
        ride.status = "in_progress"
        ride.started_at = datetime.now(timezone.utc)
        self.db.add(ride)
        return ride

    async def complete_ride(self, ride: Ride, driver: Driver, actual_dist: float | None) -> Ride:
        ride.status = "completed"
        ride.completed_at = datetime.now(timezone.utc)
        if actual_dist is not None:
            ride.actual_distance_km = round(actual_dist, 2)
            ride.route_deviation_km = round(abs(actual_dist - (ride.optimal_distance_km or 0)), 2)
        ride.actual_fare = ride.estimated_fare
        ride.payment_status = "paid"
        driver.is_available = True
        driver.total_rides = (driver.total_rides or 0) + 1
        self.db.add(ride)
        self.db.add(driver)
        return ride

    async def cancel_ride(self, ride: Ride, reason: str, cancelled_by: str) -> Ride:
        ride.status = "cancelled"
        ride.cancelled_at = datetime.now(timezone.utc)
        ride.cancel_reason = reason
        ride.cancelled_by = cancelled_by
        if ride.driver_id:
            d = await self.get_driver_by_id(ride.driver_id)
            if d:
                d.is_available = True
                self.db.add(d)
        self.db.add(ride)
        return ride

    async def get_customer_rides(self, customer_id: int) -> list[Ride]:
        r = await self.db.execute(
            select(Ride)
            .where(Ride.customer_id == customer_id)
            .order_by(Ride.created_at.desc())
        )
        return list(r.scalars().all())

    async def get_driver_rides(self, driver_id: int) -> list[Ride]:
        r = await self.db.execute(
            select(Ride)
            .where(Ride.driver_id == driver_id)
            .order_by(Ride.created_at.desc())
        )
        return list(r.scalars().all())

    async def get_pending_rides(self) -> list[Ride]:
        r = await self.db.execute(
            select(Ride)
            .where(Ride.status == "waiting_for_driver")
            .order_by(Ride.created_at.asc())
        )
        return list(r.scalars().all())

    # ── Safety ─────────────────────────────────────────────────

    async def get_safety(self, ride_id: int) -> RideSafety | None:
        r = await self.db.execute(select(RideSafety).where(RideSafety.ride_id == ride_id))
        return r.scalar_one_or_none()

    async def create_or_update_safety(self, ride_id: int, **kwargs) -> RideSafety:
        existing = await self.get_safety(ride_id)
        if existing:
            for k, v in kwargs.items():
                setattr(existing, k, v)
            return existing
        safety = RideSafety(ride_id=ride_id, **kwargs)
        self.db.add(safety)
        return safety

    # ── Rating ─────────────────────────────────────────────────

    async def get_existing_rating(self, ride_id: int, user_id: int) -> RideRating | None:
        r = await self.db.execute(
            select(RideRating).where(
                RideRating.ride_id == ride_id,
                RideRating.rated_by == user_id,
            )
        )
        return r.scalar_one_or_none()

    async def create_rating(self, ride_id: int, user_id: int, rating: int, comment: str | None, categories: str | None) -> RideRating:
        r = RideRating(
            ride_id=ride_id,
            rated_by=user_id,
            rating=rating,
            comment=comment,
            categories=categories,
        )
        self.db.add(r)
        return r

    async def update_driver_rating(self, driver_id: int) -> None:
        stats = await self.db.execute(
            select(func.avg(RideRating.rating), func.count(RideRating.id))
            .join(Ride, RideRating.ride_id == Ride.id)
            .where(Ride.driver_id == driver_id)
        )
        avg, cnt = stats.one()
        d = await self.get_driver_by_id(driver_id)
        if d:
            d.rating = round(avg, 1) if avg else d.rating
            d.total_ratings = cnt
            self.db.add(d)

    # ── Driver pending penalty ─────────────────────────────────

    async def apply_penalty(self, driver: Driver) -> None:
        from datetime import timedelta
        driver.is_available = False
        driver.penalty_until = datetime.now(timezone.utc) + timedelta(hours=2)
        self.db.add(driver)

    async def reset_penalty(self, driver: Driver) -> None:
        driver.cancelled_rides = 0
        driver.is_available = True
        driver.penalty_until = None
        self.db.add(driver)
