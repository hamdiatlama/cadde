from datetime import datetime, timezone
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.channel_manager.models import (
    OtaChannel, OtaConnection, OtaListing, OtaRatePlan,
    OtaBooking, OtaSyncLog,
)
from src.modules.hotel.models import Booking, BookingStatus


class ChannelManagerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── OTA Channels ──────────────────────────────────────────

    async def list_ota_channels(self) -> list[OtaChannel]:
        r = await self.db.execute(select(OtaChannel).where(OtaChannel.is_active == True))
        return list(r.scalars().all())

    async def get_ota_channel(self, channel_id: int) -> OtaChannel | None:
        r = await self.db.execute(select(OtaChannel).where(OtaChannel.id == channel_id))
        return r.scalar_one_or_none()

    async def create_ota_channel(self, data: dict) -> OtaChannel:
        channel = OtaChannel(**data)
        self.db.add(channel)
        return channel

    async def update_ota_channel(self, channel_id: int, data: dict) -> OtaChannel | None:
        channel = await self.get_ota_channel(channel_id)
        if not channel:
            return None
        for field, val in data.items():
            setattr(channel, field, val)
        self.db.add(channel)
        return channel

    # ─── OTA Connections ───────────────────────────────────────

    async def list_connections(self, hotel_id: int) -> list[OtaConnection]:
        r = await self.db.execute(
            select(OtaConnection).where(OtaConnection.hotel_id == hotel_id)
        )
        return list(r.scalars().all())

    async def get_connection(self, connection_id: int) -> OtaConnection | None:
        r = await self.db.execute(select(OtaConnection).where(OtaConnection.id == connection_id))
        return r.scalar_one_or_none()

    async def create_connection(self, data: dict) -> OtaConnection:
        conn = OtaConnection(**data)
        self.db.add(conn)
        return conn

    async def update_connection(self, connection_id: int, data: dict) -> OtaConnection | None:
        conn = await self.get_connection(connection_id)
        if not conn:
            return None
        for field, val in data.items():
            setattr(conn, field, val)
        self.db.add(conn)
        return conn

    async def delete_connection(self, connection_id: int) -> bool:
        conn = await self.get_connection(connection_id)
        if not conn:
            return False
        conn.is_active = False
        self.db.add(conn)
        return True

    # ─── OTA Listings ──────────────────────────────────────────

    async def list_listings(self, hotel_id: int) -> list[OtaListing]:
        r = await self.db.execute(
            select(OtaListing).where(OtaListing.hotel_id == hotel_id)
        )
        return list(r.scalars().all())

    async def get_listing(self, listing_id: int) -> OtaListing | None:
        r = await self.db.execute(select(OtaListing).where(OtaListing.id == listing_id))
        return r.scalar_one_or_none()

    async def create_listing(self, data: dict) -> OtaListing:
        listing = OtaListing(**data)
        self.db.add(listing)
        return listing

    async def update_listing(self, listing_id: int, data: dict) -> OtaListing | None:
        listing = await self.get_listing(listing_id)
        if not listing:
            return None
        for field, val in data.items():
            setattr(listing, field, val)
        listing.updated_at = datetime.now(timezone.utc)
        self.db.add(listing)
        return listing

    # ─── OTA Rate Plans ────────────────────────────────────────

    async def list_rate_plans(self, listing_id: int) -> list[OtaRatePlan]:
        r = await self.db.execute(
            select(OtaRatePlan).where(OtaRatePlan.listing_id == listing_id)
        )
        return list(r.scalars().all())

    async def create_rate_plan(self, data: dict) -> OtaRatePlan:
        plan = OtaRatePlan(**data)
        self.db.add(plan)
        return plan

    async def update_rate_plan(self, plan_id: int, data: dict) -> OtaRatePlan | None:
        plan = await self.db.get(OtaRatePlan, plan_id)
        if not plan:
            return None
        for field, val in data.items():
            setattr(plan, field, val)
        self.db.add(plan)
        return plan

    # ─── OTA Bookings ──────────────────────────────────────────

    async def list_ota_bookings(self, hotel_id: int, status: str = None):
        query = select(OtaBooking).join(OtaListing).where(OtaListing.hotel_id == hotel_id)
        if status:
            query = query.where(OtaBooking.status == status)
        query = query.order_by(OtaBooking.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def get_ota_booking(self, booking_id: int) -> OtaBooking | None:
        r = await self.db.execute(select(OtaBooking).where(OtaBooking.id == booking_id))
        return r.scalar_one_or_none()

    async def create_ota_booking(self, data: dict) -> OtaBooking:
        booking = OtaBooking(**data)
        self.db.add(booking)
        return booking

    async def sync_ota_booking_to_pms(self, booking_id: int) -> Booking | None:
        ota_booking = await self.get_ota_booking(booking_id)
        if not ota_booking:
            return None
        listing = await self.get_listing(ota_booking.ota_listing_id)
        if not listing:
            return None
        booking = Booking(
            hotel_id=listing.hotel_id,
            guest_name=ota_booking.guest_name,
            guest_email=ota_booking.guest_email,
            check_in=ota_booking.check_in,
            check_out=ota_booking.check_out,
            adults=ota_booking.adults,
            children=ota_booking.children,
            total_price=ota_booking.total_price,
            status=BookingStatus.CONFIRMED,
        )
        self.db.add(booking)
        await self.db.flush()
        ota_booking.synced_to_pms = True
        self.db.add(ota_booking)
        return booking

    # ─── OTA Sync Logs ─────────────────────────────────────────

    async def list_sync_logs(self, connection_id: int) -> list[OtaSyncLog]:
        r = await self.db.execute(
            select(OtaSyncLog).where(OtaSyncLog.connection_id == connection_id)
            .order_by(OtaSyncLog.started_at.desc())
        )
        return list(r.scalars().all())

    async def create_sync_log(self, data: dict) -> OtaSyncLog:
        log = OtaSyncLog(**data)
        self.db.add(log)
        return log
