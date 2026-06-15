from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.digital_compendium.models import (
    DigitalCompendium, CompendiumPage, GuestNotification, RoomServiceRequest,
)


class DigitalCompendiumRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── DigitalCompendium ──────────────────────────────────────────

    async def create_compendium(self, data: dict) -> DigitalCompendium:
        c = DigitalCompendium(**data)
        self.db.add(c)
        await self.db.flush()
        await self.db.refresh(c)
        return c

    async def get_compendium(self, compendium_id: int) -> DigitalCompendium | None:
        r = await self.db.execute(select(DigitalCompendium).where(DigitalCompendium.id == compendium_id))
        return r.scalar_one_or_none()

    async def get_hotel_compendium(self, hotel_id: int) -> DigitalCompendium | None:
        r = await self.db.execute(select(DigitalCompendium).where(DigitalCompendium.hotel_id == hotel_id))
        return r.scalar_one_or_none()

    async def update_compendium(self, compendium_id: int, data: dict) -> DigitalCompendium | None:
        c = await self.get_compendium(compendium_id)
        if not c:
            return None
        for field, val in data.items():
            setattr(c, field, val)
        c.updated_at = datetime.now(timezone.utc)
        self.db.add(c)
        return c

    # ─── CompendiumPage ─────────────────────────────────────────────

    async def create_page(self, data: dict) -> CompendiumPage:
        p = CompendiumPage(**data)
        self.db.add(p)
        await self.db.flush()
        await self.db.refresh(p)
        return p

    async def get_page(self, page_id: int) -> CompendiumPage | None:
        r = await self.db.execute(select(CompendiumPage).where(CompendiumPage.id == page_id))
        return r.scalar_one_or_none()

    async def list_pages(self, compendium_id: int) -> list[CompendiumPage]:
        r = await self.db.execute(
            select(CompendiumPage)
            .where(CompendiumPage.compendium_id == compendium_id, CompendiumPage.is_active == True)
            .order_by(CompendiumPage.sort_order)
        )
        return list(r.scalars().all())

    async def update_page(self, page_id: int, data: dict) -> CompendiumPage | None:
        p = await self.get_page(page_id)
        if not p:
            return None
        for field, val in data.items():
            setattr(p, field, val)
        self.db.add(p)
        return p

    async def delete_page(self, page_id: int) -> bool:
        p = await self.get_page(page_id)
        if not p:
            return False
        p.is_active = False
        self.db.add(p)
        return True

    # ─── GuestNotification ──────────────────────────────────────────

    async def create_notification(self, data: dict) -> GuestNotification:
        n = GuestNotification(**data)
        self.db.add(n)
        await self.db.flush()
        await self.db.refresh(n)
        return n

    async def list_notifications(self, booking_id: int, is_read: bool = None) -> list[GuestNotification]:
        q = select(GuestNotification).where(GuestNotification.booking_id == booking_id)
        if is_read is not None:
            q = q.where(GuestNotification.is_read == is_read)
        q = q.order_by(GuestNotification.sent_at.desc())
        r = await self.db.execute(q)
        return list(r.scalars().all())

    async def mark_notification_read(self, notification_id: int) -> GuestNotification | None:
        r = await self.db.execute(select(GuestNotification).where(GuestNotification.id == notification_id))
        n = r.scalar_one_or_none()
        if n:
            n.is_read = True
            self.db.add(n)
        return n

    # ─── RoomServiceRequest ─────────────────────────────────────────

    async def create_room_service_request(self, data: dict) -> RoomServiceRequest:
        req = RoomServiceRequest(**data)
        self.db.add(req)
        await self.db.flush()
        await self.db.refresh(req)
        return req

    async def get_room_service_request(self, request_id: int) -> RoomServiceRequest | None:
        r = await self.db.execute(select(RoomServiceRequest).where(RoomServiceRequest.id == request_id))
        return r.scalar_one_or_none()

    async def list_room_service_requests(self, hotel_id: int, status: str = None) -> list[RoomServiceRequest]:
        q = select(RoomServiceRequest).where(RoomServiceRequest.hotel_id == hotel_id)
        if status:
            q = q.where(RoomServiceRequest.status == status)
        q = q.order_by(RoomServiceRequest.requested_at.desc())
        r = await self.db.execute(q)
        return list(r.scalars().all())

    async def update_room_service_status(self, request_id: int, status: str) -> RoomServiceRequest | None:
        req = await self.get_room_service_request(request_id)
        if not req:
            return None
        req.status = status
        if status == "completed":
            req.completed_at = datetime.now(timezone.utc)
        self.db.add(req)
        return req
