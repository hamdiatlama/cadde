from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.digital_compendium.repository import DigitalCompendiumRepository
from src.modules.hotel.models import Booking


class DigitalCompendiumService:
    def __init__(self, db: AsyncSession):
        self.repo = DigitalCompendiumRepository(db)

    async def create_compendium(self, hotel_id: int, data: dict) -> dict:
        existing = await self.repo.get_hotel_compendium(hotel_id)
        if existing:
            raise ValueError("Compendium already exists for this hotel")
        c = await self.repo.create_compendium({"hotel_id": hotel_id, **data})
        return self._format_compendium(c)

    async def update_compendium(self, compendium_id: int, data: dict) -> dict:
        c = await self.repo.update_compendium(compendium_id, data)
        if not c:
            raise ValueError("Compendium not found")
        return self._format_compendium(c)

    async def get_compendium(self, hotel_id: int) -> dict | None:
        c = await self.repo.get_hotel_compendium(hotel_id)
        if not c:
            return None
        return self._format_compendium(c)

    async def get_guest_compendium(self, booking_id: int) -> dict | None:
        r = await self.repo.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")
        c = await self.repo.get_hotel_compendium(booking.hotel_id)
        if not c or not c.is_published:
            return None
        pages = await self.repo.list_pages(c.id)
        return {
            **self._format_compendium(c),
            "pages": [self._format_page(p) for p in pages],
        }

    async def send_welcome_notification(self, booking_id: int) -> dict:
        r = await self.repo.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")
        c = await self.repo.get_hotel_compendium(booking.hotel_id)
        welcome_msg = c.welcome_message if c and c.welcome_message else "Welcome to our hotel!"
        n = await self.repo.create_notification({
            "booking_id": booking_id,
            "hotel_id": booking.hotel_id,
            "notification_type": "welcome",
            "title": "Welcome!",
            "message": welcome_msg,
        })
        return self._format_notification(n)

    async def send_checkout_reminder(self, booking_id: int) -> dict:
        r = await self.repo.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")
        n = await self.repo.create_notification({
            "booking_id": booking_id,
            "hotel_id": booking.hotel_id,
            "notification_type": "checkout_reminder",
            "title": "Check-out Reminder",
            "message": f"Your check-out time is {booking.check_out.strftime('%H:%M') if booking.check_out else '12:00'}. Thank you for staying with us!",
        })
        return self._format_notification(n)

    async def list_notifications(self, booking_id: int, is_read: bool = None) -> list[dict]:
        ns = await self.repo.list_notifications(booking_id, is_read)
        return [self._format_notification(n) for n in ns]

    async def request_room_service(self, booking_id: int, category: str, item_name: str, quantity: int = 1, notes: str = None) -> dict:
        r = await self.repo.db.execute(select(Booking).where(Booking.id == booking_id))
        booking = r.scalar_one_or_none()
        if not booking:
            raise ValueError("Booking not found")
        req = await self.repo.create_room_service_request({
            "booking_id": booking_id,
            "hotel_id": booking.hotel_id,
            "category": category,
            "item_name": item_name,
            "quantity": quantity,
            "notes": notes,
            "status": "pending",
        })
        return self._format_room_service(req)

    async def list_room_service_requests(self, hotel_id: int, status: str = None) -> list[dict]:
        reqs = await self.repo.list_room_service_requests(hotel_id, status)
        return [self._format_room_service(r) for r in reqs]

    async def update_room_service_status(self, request_id: int, status: str) -> dict:
        req = await self.repo.update_room_service_status(request_id, status)
        if not req:
            raise ValueError("Room service request not found")
        return self._format_room_service(req)

    async def create_page(self, compendium_id: int, data: dict) -> dict:
        p = await self.repo.create_page({"compendium_id": compendium_id, **data})
        return self._format_page(p)

    async def update_page(self, page_id: int, data: dict) -> dict:
        p = await self.repo.update_page(page_id, data)
        if not p:
            raise ValueError("Page not found")
        return self._format_page(p)

    async def list_pages(self, compendium_id: int) -> list[dict]:
        pages = await self.repo.list_pages(compendium_id)
        return [self._format_page(p) for p in pages]

    def _format_compendium(self, c) -> dict:
        return {
            "id": c.id,
            "hotel_id": c.hotel_id,
            "welcome_message": c.welcome_message,
            "wifi_ssid": c.wifi_ssid,
            "wifi_password": c.wifi_password,
            "breakfast_info": c.breakfast_info,
            "restaurant_info": c.restaurant_info,
            "room_service_info": c.room_service_info,
            "spa_info": c.spa_info,
            "gym_info": c.gym_info,
            "parking_info": c.parking_info,
            "house_rules": c.house_rules,
            "emergency_info": c.emergency_info,
            "checkout_info": c.checkout_info,
            "local_attractions": c.local_attractions,
            "hotel_services": c.hotel_services,
            "contact_info": c.contact_info,
            "is_published": c.is_published,
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None,
        }

    def _format_page(self, p) -> dict:
        return {
            "id": p.id,
            "compendium_id": p.compendium_id,
            "title": p.title,
            "content": p.content,
            "icon": p.icon,
            "sort_order": p.sort_order,
            "is_active": p.is_active,
            "created_at": p.created_at.isoformat() if p.created_at else None,
        }

    def _format_notification(self, n) -> dict:
        return {
            "id": n.id,
            "booking_id": n.booking_id,
            "hotel_id": n.hotel_id,
            "room_number": n.room_number,
            "notification_type": n.notification_type,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "sent_at": n.sent_at.isoformat() if n.sent_at else None,
        }

    def _format_room_service(self, r) -> dict:
        return {
            "id": r.id,
            "booking_id": r.booking_id,
            "hotel_id": r.hotel_id,
            "room_number": r.room_number,
            "category": r.category,
            "item_name": r.item_name,
            "quantity": r.quantity,
            "notes": r.notes,
            "status": r.status,
            "requested_at": r.requested_at.isoformat() if r.requested_at else None,
            "completed_at": r.completed_at.isoformat() if r.completed_at else None,
        }
