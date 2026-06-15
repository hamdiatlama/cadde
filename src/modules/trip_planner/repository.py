from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.trip_planner.models import (
    TripPlan, TripSegment, TripStay, TripActivity,
    TripFood, TripRental, TripDelivery
)
from fastapi import Depends


class TripPlannerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Plan ───────────────────────────────────────────
    async def create_plan(self, data: dict):
        p = TripPlan(**data)
        self.db.add(p); await self.db.commit(); await self.db.refresh(p)
        return p

    async def get_plan(self, plan_id: int):
        r = await self.db.execute(select(TripPlan).where(TripPlan.id == plan_id))
        return r.scalar_one_or_none()

    async def list_plans(self, user_id: int = None, status: str = None):
        q = select(TripPlan)
        if user_id: q = q.where(TripPlan.user_id == user_id)
        if status: q = q.where(TripPlan.status == status)
        r = await self.db.execute(q.order_by(TripPlan.created_at.desc()))
        return r.scalars().all()

    async def update_plan(self, plan_id: int, data: dict):
        r = await self.db.execute(select(TripPlan).where(TripPlan.id == plan_id))
        p = r.scalar_one_or_none()
        if p:
            for k, v in data.items(): setattr(p, k, v)
            await self.db.commit(); await self.db.refresh(p)
        return p

    async def delete_plan(self, plan_id: int):
        r = await self.db.execute(select(TripPlan).where(TripPlan.id == plan_id))
        p = r.scalar_one_or_none()
        if p:
            await self.db.delete(p)
            await self.db.commit()
            return True
        return False

    # ─── Segment ────────────────────────────────────────
    async def create_segment(self, data: dict):
        s = TripSegment(**data)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s)
        return s

    async def get_segment(self, seg_id: int):
        r = await self.db.execute(select(TripSegment).where(TripSegment.id == seg_id))
        return r.scalar_one_or_none()

    async def list_segments(self, trip_id: int):
        q = select(TripSegment).where(TripSegment.trip_id == trip_id).order_by(TripSegment.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_segment(self, seg_id: int, data: dict):
        r = await self.db.execute(select(TripSegment).where(TripSegment.id == seg_id))
        s = r.scalar_one_or_none()
        if s:
            for k, v in data.items(): setattr(s, k, v)
            await self.db.commit(); await self.db.refresh(s)
        return s

    async def delete_segment(self, seg_id: int):
        r = await self.db.execute(select(TripSegment).where(TripSegment.id == seg_id))
        s = r.scalar_one_or_none()
        if s:
            await self.db.delete(s)
            await self.db.commit()
            return True
        return False

    # ─── Stay ───────────────────────────────────────────
    async def create_stay(self, data: dict):
        s = TripStay(**data)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s)
        return s

    async def list_stays(self, trip_id: int):
        q = select(TripStay).where(TripStay.trip_id == trip_id).order_by(TripStay.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_stay(self, stay_id: int, data: dict):
        r = await self.db.execute(select(TripStay).where(TripStay.id == stay_id))
        s = r.scalar_one_or_none()
        if s:
            for k, v in data.items(): setattr(s, k, v)
            await self.db.commit(); await self.db.refresh(s)
        return s

    # ─── Activity ───────────────────────────────────────
    async def create_activity(self, data: dict):
        a = TripActivity(**data)
        self.db.add(a); await self.db.commit(); await self.db.refresh(a)
        return a

    async def list_activities(self, trip_id: int):
        q = select(TripActivity).where(TripActivity.trip_id == trip_id).order_by(TripActivity.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_activity(self, act_id: int, data: dict):
        r = await self.db.execute(select(TripActivity).where(TripActivity.id == act_id))
        a = r.scalar_one_or_none()
        if a:
            for k, v in data.items(): setattr(a, k, v)
            await self.db.commit(); await self.db.refresh(a)
        return a

    # ─── Food ───────────────────────────────────────────
    async def create_food(self, data: dict):
        f = TripFood(**data)
        self.db.add(f); await self.db.commit(); await self.db.refresh(f)
        return f

    async def list_foods(self, trip_id: int):
        q = select(TripFood).where(TripFood.trip_id == trip_id).order_by(TripFood.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_food(self, food_id: int, data: dict):
        r = await self.db.execute(select(TripFood).where(TripFood.id == food_id))
        f = r.scalar_one_or_none()
        if f:
            for k, v in data.items(): setattr(f, k, v)
            await self.db.commit(); await self.db.refresh(f)
        return f

    # ─── Rental ─────────────────────────────────────────
    async def create_rental(self, data: dict):
        r = TripRental(**data)
        self.db.add(r); await self.db.commit(); await self.db.refresh(r)
        return r

    async def list_rentals(self, trip_id: int):
        q = select(TripRental).where(TripRental.trip_id == trip_id).order_by(TripRental.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    # ─── Delivery ───────────────────────────────────────
    async def create_delivery(self, data: dict):
        d = TripDelivery(**data)
        self.db.add(d); await self.db.commit(); await self.db.refresh(d)
        return d

    async def list_deliveries(self, trip_id: int):
        q = select(TripDelivery).where(TripDelivery.trip_id == trip_id).order_by(TripDelivery.sequence)
        r = await self.db.execute(q)
        return r.scalars().all()

    # ─── Full trip load ─────────────────────────────────
    async def get_full_trip(self, trip_id: int):
        plan = await self.get_plan(trip_id)
        if not plan: return None
        return {
            "plan": plan,
            "segments": [s.__dict__ for s in await self.list_segments(trip_id)],
            "stays": [s.__dict__ for s in await self.list_stays(trip_id)],
            "activities": [a.__dict__ for a in await self.list_activities(trip_id)],
            "foods": [f.__dict__ for f in await self.list_foods(trip_id)],
            "rentals": [r.__dict__ for r in await self.list_rentals(trip_id)],
            "deliveries": [d.__dict__ for d in await self.list_deliveries(trip_id)],
        }


def get_trip_repo(db: AsyncSession = Depends(get_db)) -> TripPlannerRepository:
    return TripPlannerRepository(db)
