from datetime import datetime, timezone
import uuid
from sqlalchemy import select, and_
from src.modules.event.repository import EventRepository
from src.modules.event.models import Venue, VenueSection, Event, EventSession, SessionPricing, Seat, TicketBooking, Ticket


class EventService:
    def __init__(self, db):
        self.repo = EventRepository(db)

    async def create_venue(self, name: str, city: str, district: str = None, address: str = None,
                           latitude=None, longitude=None, capacity: int = 0, phone: str = None):
        venue = Venue(name=name, city=city, district=district, address=address,
                      latitude=latitude, longitude=longitude, capacity=capacity, phone=phone)
        await self.repo.create_venue(venue)
        await self.repo.db.flush()
        return {"id": venue.id, "name": venue.name, "city": venue.city}

    async def list_venues(self):
        venues = await self.repo.list_venues()
        return [{"id": v.id, "name": v.name, "city": v.city, "district": v.district,
                 "capacity": v.capacity} for v in venues]

    async def get_venue(self, venue_id: int):
        venue = await self.repo.get_venue(venue_id)
        if not venue:
            return None
        sections = await self.repo.list_sections_by_venue(venue_id)
        return {
            "id": venue.id, "name": venue.name, "city": venue.city, "district": venue.district,
            "address": venue.address, "latitude": str(venue.latitude) if venue.latitude else None,
            "longitude": str(venue.longitude) if venue.longitude else None,
            "capacity": venue.capacity, "phone": venue.phone,
            "created_at": venue.created_at.isoformat() if venue.created_at else None,
            "sections": [{"id": s.id, "name": s.name, "capacity": s.capacity,
                          "price_multiplier": str(s.price_multiplier)} for s in sections]
        }

    async def create_section(self, venue_id: int, name: str, capacity: int = 0, price_multiplier: float = 1.0):
        section = VenueSection(venue_id=venue_id, name=name, capacity=capacity,
                               price_multiplier=price_multiplier)
        await self.repo.create_venue_section(section)
        await self.repo.db.flush()
        return {"id": section.id, "name": section.name, "capacity": section.capacity}

    async def list_sections(self, venue_id: int):
        sections = await self.repo.list_sections_by_venue(venue_id)
        return [{"id": s.id, "venue_id": s.venue_id, "name": s.name, "capacity": s.capacity,
                 "price_multiplier": str(s.price_multiplier)} for s in sections]

    async def delete_section(self, section_id: int):
        await self.repo.delete_venue_section(section_id)

    async def create_event(self, title: str, category: str, venue_id: int, description: str = None,
                           poster_url: str = None, min_age: int = 0, organizer: str = None):
        event = Event(title=title, category=category, venue_id=venue_id, description=description,
                      poster_url=poster_url, min_age=min_age, organizer=organizer)
        await self.repo.create_event(event)
        await self.repo.db.flush()
        return {"id": event.id, "title": event.title, "category": event.category, "status": event.status}

    async def list_events(self, category: str = None, venue_id: int = None, venue_type: str = None):
        events = await self.repo.list_events(category, venue_id, venue_type)
        return [{"id": e.id, "title": e.title, "category": e.category, "venue_id": e.venue_id,
                 "status": e.status, "min_age": e.min_age,
                 "created_at": e.created_at.isoformat() if e.created_at else None}
                for e in events]

    async def get_event(self, event_id: int):
        event = await self.repo.get_event(event_id)
        if not event:
            return None
        sessions = await self.repo.list_sessions_by_event(event_id)
        return {
            "id": event.id, "title": event.title, "category": event.category,
            "venue_id": event.venue_id, "description": event.description,
            "poster_url": event.poster_url, "min_age": event.min_age,
            "organizer": event.organizer, "status": event.status,
            "created_at": event.created_at.isoformat() if event.created_at else None,
            "updated_at": event.updated_at.isoformat() if event.updated_at else None,
            "sessions": [{"id": s.id, "start_time": s.start_time.isoformat() if s.start_time else None,
                          "end_time": s.end_time.isoformat() if s.end_time else None,
                          "is_active": s.is_active} for s in sessions]
        }

    async def update_event_status(self, event_id: int, status: str):
        event = await self.repo.get_event(event_id)
        if not event:
            return None
        await self.repo.update_event_status(event_id, status)
        return {"id": event.id, "status": status}

    async def delete_event(self, event_id: int):
        await self.repo.delete_event(event_id)

    async def create_session(self, event_id: int, start_time, end_time=None, is_active: bool = True):
        session = EventSession(event_id=event_id, start_time=start_time, end_time=end_time,
                               is_active=is_active)
        await self.repo.create_event_session(session)
        await self.repo.db.flush()
        return {"id": session.id, "event_id": session.event_id,
                "start_time": session.start_time.isoformat() if session.start_time else None}

    async def list_sessions(self, event_id: int):
        sessions = await self.repo.list_sessions_by_event(event_id)
        return [{"id": s.id, "event_id": s.event_id,
                 "start_time": s.start_time.isoformat() if s.start_time else None,
                 "end_time": s.end_time.isoformat() if s.end_time else None,
                 "is_active": s.is_active} for s in sessions]

    async def create_session_pricing(self, session_id: int, section_id: int, price, currency: str = "TRY"):
        pricing = SessionPricing(session_id=session_id, section_id=section_id, price=price, currency=currency)
        await self.repo.create_session_pricing(pricing)
        await self.repo.db.flush()
        return {"id": pricing.id, "session_id": pricing.session_id, "section_id": pricing.section_id,
                "price": str(pricing.price), "currency": pricing.currency}

    async def get_session_pricing(self, session_id: int):
        pricing_list = await self.repo.list_pricing_by_session(session_id)
        return [{"id": p.id, "session_id": p.session_id, "section_id": p.section_id,
                 "price": str(p.price), "currency": p.currency} for p in pricing_list]

    async def create_seats_bulk(self, section_id: int, seats_data: list[dict]):
        seats = [Seat(section_id=section_id, row_label=s.get("row_label"),
                      seat_number=s.get("seat_number")) for s in seats_data]
        await self.repo.bulk_create_seats(seats)
        await self.repo.db.flush()
        return [{"id": s.id, "section_id": s.section_id, "row_label": s.row_label,
                 "seat_number": s.seat_number} for s in seats]

    async def reserve_tickets(self, user_id: int, session_id: int, section_id: int,
                              seat_ids: list[int] = None, qty: int = None):
        session = await self.repo.get_event_session(session_id)
        if not session or not session.is_active:
            raise ValueError("Session not found or inactive")

        pricing_list = await self.repo.list_pricing_by_session(session_id)
        pricing = next((p for p in pricing_list if p.section_id == section_id), None)
        if not pricing:
            raise ValueError("No pricing found for this session and section")

        if seat_ids:
            taken = await self.repo.list_tickets_by_session(session_id)
            taken_seat_ids = {t.seat_id for t in taken if t.status in ("active", "pending") and t.seat_id}
            available_seats = await self.repo.list_seats_by_section(section_id)
            requested = [s for s in available_seats if s.id in seat_ids]
            for s in requested:
                if s.id in taken_seat_ids:
                    raise ValueError(f"Seat {s.id} already taken")
            count = len(requested)
        elif qty:
            taken = await self.repo.list_tickets_by_session(session_id)
            taken_seat_ids = {t.seat_id for t in taken if t.status in ("active", "pending") and t.seat_id}
            available_seats = await self.repo.list_seats_by_section(section_id)
            requested = [s for s in available_seats if s.id not in taken_seat_ids][:qty]
            count = len(requested)
            if count < qty:
                raise ValueError(f"Only {count} seats available, requested {qty}")
        else:
            raise ValueError("Provide seat_ids or qty")

        total = float(pricing.price) * count
        booking = TicketBooking(user_id=user_id, session_id=session_id,
                                total_amount=total, currency=pricing.currency)
        await self.repo.create_ticket_booking(booking)
        await self.repo.db.flush()

        tickets = []
        for i, seat in enumerate(requested):
            seat_label = f"{seat.row_label}{seat.seat_number}" if seat.row_label else str(seat.seat_number)
            barcode = f"TK-{booking.id}-{i + 1}-{uuid.uuid4().hex[:8].upper()}"
            ticket = Ticket(
                booking_id=booking.id, session_id=session_id, section_id=section_id,
                seat_id=seat.id, seat_label=seat_label, price=pricing.price,
                barcode=barcode, status="active"
            )
            await self.repo.create_ticket(ticket)
            tickets.append(ticket)
        await self.repo.db.flush()

        return {
            "booking_id": booking.id,
            "status": booking.status,
            "total_amount": str(booking.total_amount),
            "currency": booking.currency,
            "tickets": [{"id": t.id, "seat_label": t.seat_label, "barcode": t.barcode, "status": t.status}
                        for t in tickets]
        }

    async def confirm_booking(self, booking_id: int, user_id: int):
        booking = await self.repo.get_ticket_booking(booking_id)
        if not booking:
            return None
        if booking.user_id != user_id:
            return None
        if booking.status != "pending":
            raise ValueError("Booking is not in pending status")
        now = datetime.now(timezone.utc)
        await self.repo.update_booking_status(booking_id, "paid", paid_at=now)
        return {"id": booking.id, "status": "paid"}

    async def cancel_booking(self, booking_id: int, user_id: int):
        booking = await self.repo.get_ticket_booking(booking_id)
        if not booking:
            return None
        if booking.user_id != user_id:
            return None
        if booking.status not in ("pending", "paid"):
            raise ValueError("Booking cannot be cancelled")
        now = datetime.now(timezone.utc)
        await self.repo.update_booking_status(booking_id, "cancelled", cancelled_at=now)
        tickets = await self.repo.list_tickets_by_booking(booking_id)
        for t in tickets:
            await self.repo.update_ticket_status(t.id, "cancelled")
        return {"id": booking.id, "status": "cancelled"}

    async def get_booking_detail(self, booking_id: int, user_id: int):
        booking = await self.repo.get_ticket_booking(booking_id)
        if not booking:
            return None
        if booking.user_id != user_id:
            return None
        tickets = await self.repo.list_tickets_by_booking(booking_id)
        return {
            "id": booking.id, "user_id": booking.user_id, "session_id": booking.session_id,
            "status": booking.status, "total_amount": str(booking.total_amount),
            "currency": booking.currency,
            "paid_at": booking.paid_at.isoformat() if booking.paid_at else None,
            "cancelled_at": booking.cancelled_at.isoformat() if booking.cancelled_at else None,
            "created_at": booking.created_at.isoformat() if booking.created_at else None,
            "tickets": [{"id": t.id, "seat_label": t.seat_label, "barcode": t.barcode, "status": t.status,
                         "price": str(t.price)} for t in tickets]
        }

    async def get_available_seats(self, session_id: int, section_id: int):
        all_seats = await self.repo.list_seats_by_section(section_id)
        taken = await self.repo.list_tickets_by_session(session_id)
        taken_seat_ids = {t.seat_id for t in taken if t.status in ("active", "pending") and t.seat_id}
        available = [s for s in all_seats if s.id not in taken_seat_ids]
        return [{"id": s.id, "row_label": s.row_label, "seat_number": s.seat_number,
                 "section_id": s.section_id} for s in available]

    async def list_bookings_by_user(self, user_id: int):
        bookings = await self.repo.list_bookings_by_user(user_id)
        return [{"id": b.id, "session_id": b.session_id, "status": b.status,
                 "total_amount": str(b.total_amount), "currency": b.currency,
                 "created_at": b.created_at.isoformat() if b.created_at else None}
                for b in bookings]
