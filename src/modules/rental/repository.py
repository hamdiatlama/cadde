from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.rental.models import (
    RentalCompany, RentalBranch, RentalVehicle,
    RentalBooking, RentalInsurance, RentalReview,
    RentalStatus, BookingStatus
)
from fastapi import Depends
import random, string


def generate_booking_no():
    return "RNT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


class RentalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_company(self, data: dict):
        c = RentalCompany(**data); self.db.add(c)
        await self.db.commit(); await self.db.refresh(c); return c

    async def get_company(self, company_id: int):
        r = await self.db.execute(select(RentalCompany).where(RentalCompany.id == company_id))
        return r.scalar_one_or_none()

    async def list_companies(self, category: str = None, city: str = None):
        q = select(RentalCompany).where(RentalCompany.is_active == True)
        if category: q = q.where(RentalCompany.categories.contains(category))
        r = await self.db.execute(q); return r.scalars().all()

    async def create_branch(self, data: dict):
        b = RentalBranch(**data); self.db.add(b)
        await self.db.commit(); await self.db.refresh(b); return b

    async def list_branches(self, company_id: int = None, city: str = None):
        q = select(RentalBranch)
        if company_id: q = q.where(RentalBranch.company_id == company_id)
        if city: q = q.where(RentalBranch.city == city)
        r = await self.db.execute(q); return r.scalars().all()

    async def create_vehicle(self, data: dict):
        v = RentalVehicle(**data); self.db.add(v)
        await self.db.commit(); await self.db.refresh(v); return v

    async def get_vehicle(self, vehicle_id: int):
        r = await self.db.execute(select(RentalVehicle).where(RentalVehicle.id == vehicle_id))
        return r.scalar_one_or_none()

    async def list_vehicles(self, category: str = None, company_id: int = None,
                             branch_id: int = None, city: str = None,
                             min_price: float = None, max_price: float = None):
        q = select(RentalVehicle).where(RentalVehicle.is_active == True)
        if category: q = q.where(RentalVehicle.category == category)
        if company_id: q = q.where(RentalVehicle.company_id == company_id)
        if branch_id: q = q.where(RentalVehicle.branch_id == branch_id)
        if min_price: q = q.where(RentalVehicle.daily_price >= min_price)
        if max_price: q = q.where(RentalVehicle.daily_price <= max_price)
        r = await self.db.execute(q); return r.scalars().all()

    async def create_booking(self, data: dict):
        data["booking_no"] = generate_booking_no()
        b = RentalBooking(**data); self.db.add(b)
        v = await self.get_vehicle(data["vehicle_id"])
        if v: v.status = RentalStatus.RENTED
        await self.db.commit(); await self.db.refresh(b); return b

    async def get_booking(self, booking_id: int):
        r = await self.db.execute(select(RentalBooking).where(RentalBooking.id == booking_id))
        return r.scalar_one_or_none()

    async def list_bookings(self, user_id: int = None, company_id: int = None,
                             vehicle_id: int = None, status: str = None):
        q = select(RentalBooking)
        if user_id: q = q.where(RentalBooking.user_id == user_id)
        if company_id: q = q.where(RentalBooking.vehicle_id.in_(
            select(RentalVehicle.id).where(RentalVehicle.company_id == company_id)))
        if vehicle_id: q = q.where(RentalBooking.vehicle_id == vehicle_id)
        if status: q = q.where(RentalBooking.status == status)
        r = await self.db.execute(q); return r.scalars().all()

    async def return_vehicle(self, booking_id: int):
        r = await self.db.execute(select(RentalBooking).where(RentalBooking.id == booking_id))
        b = r.scalar_one_or_none()
        if b:
            b.status = BookingStatus.RETURNED
            b.returned_at = func.now()
            v = await self.get_vehicle(b.vehicle_id)
            if v: v.status = RentalStatus.AVAILABLE
            await self.db.commit(); await self.db.refresh(b)
        return b

    async def cancel_booking(self, booking_id: int, reason: str = None):
        r = await self.db.execute(select(RentalBooking).where(RentalBooking.id == booking_id))
        b = r.scalar_one_or_none()
        if b:
            b.status = BookingStatus.CANCELLED
            b.cancellation_reason = reason
            v = await self.get_vehicle(b.vehicle_id)
            if v: v.status = RentalStatus.AVAILABLE
            await self.db.commit(); await self.db.refresh(b)
        return b

    async def create_insurance(self, data: dict):
        ins = RentalInsurance(**data); self.db.add(ins)
        await self.db.commit(); await self.db.refresh(ins); return ins

    async def list_insurances(self, company_id: int = None):
        q = select(RentalInsurance)
        if company_id: q = q.where(RentalInsurance.company_id == company_id)
        r = await self.db.execute(q); return r.scalars().all()

    async def create_review(self, data: dict):
        rev = RentalReview(**data); self.db.add(rev)
        await self.db.commit(); await self.db.refresh(rev); return rev

    async def list_reviews(self, vehicle_id: int = None):
        q = select(RentalReview)
        if vehicle_id: q = q.where(RentalReview.vehicle_id == vehicle_id)
        r = await self.db.execute(q); return r.scalars().all()


def get_rental_repo(db: AsyncSession = Depends(get_db)) -> RentalRepository:
    return RentalRepository(db)
