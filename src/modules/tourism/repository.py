from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.tourism.models import (
    TourismProvider, TourismExperience, TourismSchedule,
    TourismBooking, TourismReview, BookingStatus
)
from fastapi import Depends
import random
import string


def generate_booking_no():
    return "TR-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class TourismRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Provider ───────────────────────────────────────
    async def create_provider(self, data: dict):
        p = TourismProvider(**data)
        self.db.add(p); await self.db.commit(); await self.db.refresh(p)
        return p

    async def get_provider(self, provider_id: int):
        r = await self.db.execute(select(TourismProvider).where(TourismProvider.id == provider_id))
        return r.scalar_one_or_none()

    async def get_provider_by_user(self, user_id: int):
        r = await self.db.execute(select(TourismProvider).where(TourismProvider.user_id == user_id))
        return r.scalar_one_or_none()

    async def list_providers(self, is_verified: bool = None, is_active: bool = None):
        q = select(TourismProvider)
        if is_verified is not None: q = q.where(TourismProvider.is_verified == is_verified)
        if is_active is not None: q = q.where(TourismProvider.is_active == is_active)
        r = await self.db.execute(q)
        return r.scalars().all()

    # ─── Experience ─────────────────────────────────────
    async def create_experience(self, data: dict):
        e = TourismExperience(**data)
        self.db.add(e); await self.db.commit(); await self.db.refresh(e)
        return e

    async def get_experience(self, exp_id: int):
        r = await self.db.execute(select(TourismExperience).where(TourismExperience.id == exp_id))
        return r.scalar_one_or_none()

    async def list_experiences(self, category: str = None, city: str = None,
                                provider_id: int = None, is_active: bool = None):
        q = select(TourismExperience)
        if category: q = q.where(TourismExperience.category == category)
        if city: q = q.where(TourismExperience.city == city)
        if provider_id: q = q.where(TourismExperience.provider_id == provider_id)
        if is_active is not None: q = q.where(TourismExperience.is_active == is_active)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_experience(self, exp_id: int, data: dict):
        r = await self.db.execute(select(TourismExperience).where(TourismExperience.id == exp_id))
        e = r.scalar_one_or_none()
        if e:
            for k, v in data.items(): setattr(e, k, v)
            await self.db.commit(); await self.db.refresh(e)
        return e

    # ─── Schedule ───────────────────────────────────────
    async def create_schedule(self, data: dict):
        s = TourismSchedule(**data)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s)
        return s

    async def get_schedule(self, sched_id: int):
        r = await self.db.execute(select(TourismSchedule).where(TourismSchedule.id == sched_id))
        return r.scalar_one_or_none()

    async def list_schedules(self, experience_id: int = None, date: str = None):
        q = select(TourismSchedule)
        if experience_id: q = q.where(TourismSchedule.experience_id == experience_id)
        if date: q = q.where(TourismSchedule.date == date)
        r = await self.db.execute(q.order_by(TourismSchedule.date, TourismSchedule.time))
        return r.scalars().all()

    # ─── Booking ────────────────────────────────────────
    async def create_booking(self, data: dict):
        data["booking_no"] = generate_booking_no()
        b = TourismBooking(**data)
        sche = await self.get_schedule(data["schedule_id"])
        if sche and sche.available < data.get("participant_count", 1):
            raise ValueError("Yeterli kontenjan yok")
        self.db.add(b)
        if sche:
            sche.available -= data.get("participant_count", 1)
        await self.db.commit(); await self.db.refresh(b)
        return b

    async def get_booking(self, booking_id: int):
        r = await self.db.execute(select(TourismBooking).where(TourismBooking.id == booking_id))
        return r.scalar_one_or_none()

    async def get_booking_by_no(self, booking_no: str):
        r = await self.db.execute(select(TourismBooking).where(TourismBooking.booking_no == booking_no))
        return r.scalar_one_or_none()

    async def list_bookings(self, user_id: int = None, schedule_id: int = None,
                             agency_id: int = None, status: str = None):
        q = select(TourismBooking)
        if user_id: q = q.where(TourismBooking.user_id == user_id)
        if schedule_id: q = q.where(TourismBooking.schedule_id == schedule_id)
        if agency_id: q = q.where(TourismBooking.agency_id == agency_id)
        if status: q = q.where(TourismBooking.status == status)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def cancel_booking(self, booking_id: int, reason: str = None):
        r = await self.db.execute(select(TourismBooking).where(TourismBooking.id == booking_id))
        b = r.scalar_one_or_none()
        if b:
            b.status = BookingStatus.CANCELLED
            b.cancellation_reason = reason
            b.cancelled_at = func.now()
            sche = await self.get_schedule(b.schedule_id)
            if sche:
                sche.available += b.participant_count
            await self.db.commit(); await self.db.refresh(b)
        return b

    # ─── Review ─────────────────────────────────────────
    async def create_review(self, data: dict):
        r = TourismReview(**data)
        self.db.add(r); await self.db.commit(); await self.db.refresh(r)
        return r

    async def list_reviews(self, experience_id: int = None):
        q = select(TourismReview)
        if experience_id: q = q.where(TourismReview.experience_id == experience_id)
        r = await self.db.execute(q)
        return r.scalars().all()


def get_tourism_repo(db: AsyncSession = Depends(get_db)) -> TourismRepository:
    return TourismRepository(db)
