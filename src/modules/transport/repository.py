from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import joinedload
from src.database import async_session
from src.modules.transport.models import (
    TransportCompany, TransportVehicle, TransportDriver,
    TransportStation, TransportRoute, TransportRouteStop,
    TransportSchedule, ScheduleStopTime, TransportSeat,
    TransportTicket, TransportPickupBooking, TransportRating,
    TransportDocument, TransportAgencyAuthorization,
)


class TransportRepository:
    def __init__(self, db: async_session):
        self.db = db

    # ─── Firms ──────────────────────────────────────────
    async def list_companies(self, vehicle_type: str = None, is_reseller: bool = None):
        q = select(TransportCompany).where(TransportCompany.is_active == True)
        if vehicle_type:
            q = q.where(TransportCompany.vehicle_type == vehicle_type)
        if is_reseller is not None:
            q = q.where(TransportCompany.is_reseller == is_reseller)
        q = q.order_by(TransportCompany.rating.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_company(self, company_id: int):
        r = await self.db.execute(select(TransportCompany).where(TransportCompany.id == company_id))
        return r.scalar_one_or_none()

    async def create_company(self, data: dict):
        c = TransportCompany(**data)
        self.db.add(c); await self.db.commit(); await self.db.refresh(c)
        return c

    async def update_company(self, company_id: int, data: dict):
        r = await self.db.execute(select(TransportCompany).where(TransportCompany.id == company_id))
        c = r.scalar_one_or_none()
        if c:
            for k, v in data.items(): setattr(c, k, v)
            await self.db.commit(); await self.db.refresh(c)
        return c

    # ─── Vehicles ───────────────────────────────────────
    async def list_vehicles(self, company_id: int = None):
        q = select(TransportVehicle)
        if company_id: q = q.where(TransportVehicle.company_id == company_id)
        q = q.order_by(TransportVehicle.plate_number)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_vehicle(self, vehicle_id: int):
        r = await self.db.execute(select(TransportVehicle).where(TransportVehicle.id == vehicle_id))
        return r.scalar_one_or_none()

    async def create_vehicle(self, data: dict):
        v = TransportVehicle(**data)
        self.db.add(v); await self.db.commit(); await self.db.refresh(v)
        return v

    async def update_vehicle(self, vehicle_id: int, data: dict):
        r = await self.db.execute(select(TransportVehicle).where(TransportVehicle.id == vehicle_id))
        v = r.scalar_one_or_none()
        if v:
            for k, val in data.items(): setattr(v, k, val)
            await self.db.commit(); await self.db.refresh(v)
        return v

    # ─── Drivers ────────────────────────────────────────
    async def list_drivers(self, company_id: int = None):
        q = select(TransportDriver)
        if company_id: q = q.where(TransportDriver.company_id == company_id)
        q = q.order_by(TransportDriver.name)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_driver(self, driver_id: int):
        r = await self.db.execute(select(TransportDriver).where(TransportDriver.id == driver_id))
        return r.scalar_one_or_none()

    async def create_driver(self, data: dict):
        d = TransportDriver(**data)
        self.db.add(d); await self.db.commit(); await self.db.refresh(d)
        return d

    async def update_driver(self, driver_id: int, data: dict):
        r = await self.db.execute(select(TransportDriver).where(TransportDriver.id == driver_id))
        d = r.scalar_one_or_none()
        if d:
            for k, val in data.items(): setattr(d, k, val)
            await self.db.commit(); await self.db.refresh(d)
        return d

    # ─── Stations ───────────────────────────────────────
    async def list_stations(self, city: str = None):
        q = select(TransportStation).where(TransportStation.is_active == True)
        if city: q = q.where(TransportStation.city.ilike(f"%{city}%"))
        q = q.order_by(TransportStation.city, TransportStation.name)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def search_stations(self, query: str):
        q = select(TransportStation).where(and_(
            TransportStation.is_active == True,
            or_(TransportStation.name.ilike(f"%{query}%"),
                TransportStation.city.ilike(f"%{query}%"),
                TransportStation.district.ilike(f"%{query}%"))
        )).limit(20)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_station(self, station_id: int):
        r = await self.db.execute(select(TransportStation).where(TransportStation.id == station_id))
        return r.scalar_one_or_none()

    # ─── Routes ─────────────────────────────────────────
    async def list_routes(self, company_id: int = None, vehicle_type: str = None):
        q = select(TransportRoute).where(TransportRoute.is_active == True)
        if company_id: q = q.where(TransportRoute.company_id == company_id)
        if vehicle_type:
            q = q.join(TransportCompany).where(TransportCompany.vehicle_type == vehicle_type)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_route(self, route_id: int):
        r = await self.db.execute(select(TransportRoute).where(TransportRoute.id == route_id))
        return r.scalar_one_or_none()

    # ─── Route Stops ────────────────────────────────────
    async def list_route_stops(self, route_id: int, can_pickup: bool = None):
        q = select(TransportRouteStop).where(
            TransportRouteStop.route_id == route_id,
            TransportRouteStop.is_active == True,
        )
        if can_pickup is not None:
            q = q.where(TransportRouteStop.can_pickup == can_pickup)
        q = q.order_by(TransportRouteStop.sort_order)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_route_stop(self, stop_id: int):
        r = await self.db.execute(select(TransportRouteStop).where(TransportRouteStop.id == stop_id))
        return r.scalar_one_or_none()

    async def create_route_stop(self, data: dict):
        s = TransportRouteStop(**data)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s)
        return s

    # ─── Schedules ──────────────────────────────────────
    async def search_schedules(self, origin_id: int, destination_id: int, date: str,
                                vehicle_type: str = None, seat_class: str = None,
                                min_price: float = None, max_price: float = None,
                                is_pickup_route: bool = None, company_id: int = None,
                                sort_by: str = "departure_time"):
        q = select(TransportSchedule).join(TransportRoute)
        if vehicle_type or company_id:
            q = q.join(TransportCompany, TransportRoute.company_id == TransportCompany.id)
        q = q.where(
            TransportRoute.origin_station_id == origin_id,
            TransportRoute.destination_station_id == destination_id,
            TransportSchedule.departure_date == date,
            TransportSchedule.status == "active",
            TransportSchedule.available_seats > 0,
        )
        if vehicle_type:
            q = q.where(TransportCompany.vehicle_type == vehicle_type)
        if company_id:
            q = q.where(TransportRoute.company_id == company_id)
        if is_pickup_route is not None:
            q = q.where(TransportSchedule.is_pickup_route == is_pickup_route)
        if min_price is not None:
            q = q.where(TransportSchedule.base_price >= min_price)
        if max_price is not None:
            q = q.where(TransportSchedule.base_price <= max_price)
        if sort_by == "price":
            q = q.order_by(TransportSchedule.base_price)
        elif sort_by == "duration":
            q = q.order_by(TransportRoute.duration_minutes)
        else:
            q = q.order_by(TransportSchedule.departure_time)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_schedule(self, schedule_id: int):
        r = await self.db.execute(
            select(TransportSchedule)
            .options(joinedload(TransportSchedule.route))
            .where(TransportSchedule.id == schedule_id)
        )
        return r.scalar_one_or_none()

    async def get_schedule_with_details(self, schedule_id: int):
        r = await self.db.execute(
            select(TransportSchedule, TransportRoute, TransportCompany,
                   TransportVehicle, TransportDriver)
            .join(TransportRoute, TransportSchedule.route_id == TransportRoute.id)
            .join(TransportCompany, TransportRoute.company_id == TransportCompany.id)
            .outerjoin(TransportVehicle, TransportSchedule.vehicle_id == TransportVehicle.id)
            .outerjoin(TransportDriver, TransportSchedule.driver_id == TransportDriver.id)
            .where(TransportSchedule.id == schedule_id)
        )
        row = r.one_or_none()
        if not row:
            return None
        return {
            "schedule": row[0], "route": row[1], "company": row[2],
            "vehicle": row[3], "driver": row[4],
        }

    async def create_schedule(self, data: dict):
        s = TransportSchedule(**data)
        self.db.add(s); await self.db.commit(); await self.db.refresh(s)
        return s

    # ─── Schedule Stop Times ────────────────────────────
    async def list_schedule_stops(self, schedule_id: int):
        q = select(ScheduleStopTime).join(TransportRouteStop).where(
            ScheduleStopTime.schedule_id == schedule_id,
            TransportRouteStop.is_active == True,
        ).order_by(TransportRouteStop.sort_order)
        r = await self.db.execute(q)
        return r.scalars().all()

    # ─── Seats ──────────────────────────────────────────
    async def list_seats(self, schedule_id: int, seat_class: str = None):
        q = select(TransportSeat).where(TransportSeat.schedule_id == schedule_id)
        if seat_class: q = q.where(TransportSeat.seat_class == seat_class)
        q = q.order_by(TransportSeat.seat_number)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_seat(self, seat_id: int):
        r = await self.db.execute(select(TransportSeat).where(TransportSeat.id == seat_id))
        return r.scalar_one_or_none()

    async def generate_seats(self, schedule_id: int, seat_count: int, base_price: float):
        existing = await self.list_seats(schedule_id)
        if existing:
            return existing
        seats = []
        for i in range(1, seat_count + 1):
            sn = str(i).zfill(2)
            is_window = i % 3 == 1
            is_aisle = i % 3 == 0
            seat = TransportSeat(
                schedule_id=schedule_id, seat_number=sn,
                price=base_price, is_window=is_window, is_aisle=is_aisle,
            )
            self.db.add(seat)
            seats.append(seat)
        await self.db.commit()
        for s in seats:
            await self.db.refresh(s)
        return seats

    # ─── Tickets ────────────────────────────────────────
    async def create_ticket(self, data: dict):
        t = TransportTicket(**data)
        self.db.add(t); await self.db.commit(); await self.db.refresh(t)
        return t

    async def get_ticket(self, ticket_no: str):
        r = await self.db.execute(select(TransportTicket).where(TransportTicket.ticket_no == ticket_no))
        return r.scalar_one_or_none()

    async def list_user_tickets(self, user_id: int, status: str = None):
        q = select(TransportTicket).where(TransportTicket.user_id == user_id)
        if status: q = q.where(TransportTicket.status == status)
        q = q.order_by(TransportTicket.bought_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_ticket_status(self, ticket_id: int, status: str, reason: str = None):
        r = await self.db.execute(select(TransportTicket).where(TransportTicket.id == ticket_id))
        t = r.scalar_one_or_none()
        if not t: return None
        t.status = status
        if reason: t.cancellation_reason = reason
        if status == "cancelled": t.cancelled_at = func.now()
        await self.db.commit(); await self.db.refresh(t)
        return t

    async def update_seat_availability(self, seat_id: int, is_available: bool):
        r = await self.db.execute(select(TransportSeat).where(TransportSeat.id == seat_id))
        s = r.scalar_one_or_none()
        if s: s.is_available = is_available; await self.db.commit()

    async def update_schedule_seats(self, schedule_id: int, delta: int):
        r = await self.db.execute(select(TransportSchedule).where(TransportSchedule.id == schedule_id))
        s = r.scalar_one_or_none()
        if s: s.available_seats = TransportSchedule.available_seats + delta; await self.db.commit()

    # ─── Pickup Bookings ────────────────────────────────
    async def create_pickup_booking(self, data: dict):
        pb = TransportPickupBooking(**data)
        self.db.add(pb); await self.db.commit(); await self.db.refresh(pb)
        return pb

    async def list_pickup_bookings(self, schedule_id: int, status: str = None):
        q = select(TransportPickupBooking).where(
            TransportPickupBooking.schedule_id == schedule_id)
        if status: q = q.where(TransportPickupBooking.status == status)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_driver_pickups(self, driver_id: int, date: str = None):
        q = select(TransportPickupBooking)\
            .join(TransportSchedule, TransportPickupBooking.schedule_id == TransportSchedule.id)\
            .where(TransportSchedule.driver_id == driver_id)
        if date: q = q.where(TransportSchedule.departure_date == date)
        r = await self.db.execute(q)
        return r.scalars().all()

    # ─── Ratings ────────────────────────────────────────
    async def create_rating(self, data: dict):
        rt = TransportRating(**data)
        self.db.add(rt); await self.db.commit(); await self.db.refresh(rt)
        return rt

    async def get_company_ratings(self, company_id: int):
        r = await self.db.execute(
            select(TransportRating).where(TransportRating.company_id == company_id)
            .order_by(TransportRating.created_at.desc())
        )
        return r.scalars().all()

    async def get_driver_ratings(self, driver_id: int):
        r = await self.db.execute(
            select(TransportRating).where(TransportRating.driver_id == driver_id)
            .order_by(TransportRating.created_at.desc())
        )
        return r.scalars().all()

    # ─── Documents ──────────────────────────────────────
    async def list_documents(self, company_id: int = None, vehicle_id: int = None, driver_id: int = None):
        q = select(TransportDocument)
        if company_id: q = q.where(TransportDocument.company_id == company_id)
        if vehicle_id: q = q.where(TransportDocument.vehicle_id == vehicle_id)
        if driver_id: q = q.where(TransportDocument.driver_id == driver_id)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def create_document(self, data: dict):
        d = TransportDocument(**data)
        self.db.add(d); await self.db.commit(); await self.db.refresh(d)
        return d
