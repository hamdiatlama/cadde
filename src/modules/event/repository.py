from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.event.models import Venue, VenueSection, Event, EventSession, SessionPricing, Seat, TicketBooking, Ticket


class EventRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_venue(self, obj: Venue):
        self.db.add(obj)

    async def list_venues(self):
        r = await self.db.execute(select(Venue).order_by(Venue.id))
        return r.scalars().all()

    async def get_venue(self, venue_id: int):
        r = await self.db.execute(select(Venue).where(Venue.id == venue_id))
        return r.scalar_one_or_none()

    async def delete_venue(self, venue_id: int):
        await self.db.execute(Venue.__table__.delete().where(Venue.id == venue_id))

    async def create_venue_section(self, obj: VenueSection):
        self.db.add(obj)

    async def list_sections_by_venue(self, venue_id: int):
        r = await self.db.execute(
            select(VenueSection).where(VenueSection.venue_id == venue_id).order_by(VenueSection.id)
        )
        return r.scalars().all()

    async def delete_venue_section(self, section_id: int):
        await self.db.execute(VenueSection.__table__.delete().where(VenueSection.id == section_id))

    async def create_event(self, obj: Event):
        self.db.add(obj)

    async def list_events(self, category: str = None, venue_id: int = None, venue_type: str = None):
        q = select(Event)
        filters = []
        if category:
            filters.append(Event.category == category)
        if venue_id:
            filters.append(Event.venue_id == venue_id)
        if venue_type:
            q = q.join(Venue, Event.venue_id == Venue.id)
            filters.append(Venue.venue_type == venue_type)
        if filters:
            q = q.where(and_(*filters))
        q = q.order_by(Event.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_event(self, event_id: int):
        r = await self.db.execute(select(Event).where(Event.id == event_id))
        return r.scalar_one_or_none()

    async def update_event_status(self, event_id: int, status: str):
        await self.db.execute(
            Event.__table__.update().where(Event.id == event_id).values(status=status, updated_at=func.now())
        )

    async def delete_event(self, event_id: int):
        await self.db.execute(Event.__table__.delete().where(Event.id == event_id))

    async def create_event_session(self, obj: EventSession):
        self.db.add(obj)

    async def list_sessions_by_event(self, event_id: int):
        r = await self.db.execute(
            select(EventSession).where(EventSession.event_id == event_id).order_by(EventSession.start_time)
        )
        return r.scalars().all()

    async def get_event_session(self, session_id: int):
        r = await self.db.execute(select(EventSession).where(EventSession.id == session_id))
        return r.scalar_one_or_none()

    async def create_session_pricing(self, obj: SessionPricing):
        self.db.add(obj)

    async def list_pricing_by_session(self, session_id: int):
        r = await self.db.execute(
            select(SessionPricing).where(SessionPricing.session_id == session_id)
        )
        return r.scalars().all()

    async def bulk_create_seats(self, seats: list[Seat]):
        self.db.add_all(seats)

    async def list_seats_by_section(self, section_id: int):
        r = await self.db.execute(
            select(Seat).where(Seat.section_id == section_id).order_by(Seat.row_label, Seat.seat_number)
        )
        return r.scalars().all()

    async def create_ticket_booking(self, obj: TicketBooking):
        self.db.add(obj)

    async def get_ticket_booking(self, booking_id: int):
        r = await self.db.execute(select(TicketBooking).where(TicketBooking.id == booking_id))
        return r.scalar_one_or_none()

    async def list_bookings_by_user(self, user_id: int):
        r = await self.db.execute(
            select(TicketBooking).where(TicketBooking.user_id == user_id)
            .order_by(TicketBooking.created_at.desc())
        )
        return r.scalars().all()

    async def update_booking_status(self, booking_id: int, status: str, paid_at=None, cancelled_at=None):
        values = {"status": status}
        if paid_at is not None:
            values["paid_at"] = paid_at
        if cancelled_at is not None:
            values["cancelled_at"] = cancelled_at
        await self.db.execute(
            TicketBooking.__table__.update().where(TicketBooking.id == booking_id).values(**values)
        )

    async def create_ticket(self, obj: Ticket):
        self.db.add(obj)

    async def list_tickets_by_booking(self, booking_id: int):
        r = await self.db.execute(
            select(Ticket).where(Ticket.booking_id == booking_id).order_by(Ticket.id)
        )
        return r.scalars().all()

    async def list_tickets_by_session(self, session_id: int):
        r = await self.db.execute(
            select(Ticket).where(Ticket.session_id == session_id)
        )
        return r.scalars().all()

    async def get_ticket_by_barcode(self, barcode: str):
        r = await self.db.execute(select(Ticket).where(Ticket.barcode == barcode))
        return r.scalar_one_or_none()

    async def update_ticket_status(self, ticket_id: int, status: str):
        await self.db.execute(
            Ticket.__table__.update().where(Ticket.id == ticket_id).values(status=status)
        )
