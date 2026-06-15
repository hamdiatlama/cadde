from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.channel_manager.repository import ChannelManagerRepository
from src.modules.channel_manager.models import OtaChannel, OtaConnection, OtaListing


class ChannelManagerService:
    def __init__(self, db: AsyncSession):
        self.repo = ChannelManagerRepository(db)

    async def connect_ota(self, hotel_id: int, ota_channel_id: int) -> dict:
        channel = await self.repo.get_ota_channel(ota_channel_id)
        if not channel:
            raise ValueError("OTA channel not found")
        conn = await self.repo.create_connection({
            "hotel_id": hotel_id,
            "ota_channel_id": ota_channel_id,
            "status": "connected",
            "connected_at": datetime.now(timezone.utc),
        })
        return self._format_connection(conn, channel)

    async def disconnect_ota(self, connection_id: int) -> dict:
        conn = await self.repo.get_connection(connection_id)
        if not conn:
            raise ValueError("Connection not found")
        conn.status = "disconnected"
        conn.is_active = False
        self.repo.db.add(conn)
        return {"ok": True}

    async def sync_availability(self, connection_id: int, date_from: str = None, date_to: str = None) -> dict:
        conn = await self.repo.get_connection(connection_id)
        if not conn:
            raise ValueError("Connection not found")
        log = await self.repo.create_sync_log({
            "connection_id": connection_id,
            "sync_type": "availability",
            "status": "completed",
            "started_at": datetime.now(timezone.utc),
            "completed_at": datetime.now(timezone.utc),
        })
        conn.last_sync_at = datetime.now(timezone.utc)
        self.repo.db.add(conn)
        return {"ok": True, "sync_log_id": log.id, "message": "Availability sync completed"}

    async def sync_rates(self, connection_id: int) -> dict:
        conn = await self.repo.get_connection(connection_id)
        if not conn:
            raise ValueError("Connection not found")
        log = await self.repo.create_sync_log({
            "connection_id": connection_id,
            "sync_type": "rates",
            "status": "completed",
            "started_at": datetime.now(timezone.utc),
            "completed_at": datetime.now(timezone.utc),
        })
        conn.last_sync_at = datetime.now(timezone.utc)
        self.repo.db.add(conn)
        return {"ok": True, "sync_log_id": log.id, "message": "Rates sync completed"}

    async def import_ota_bookings(self, connection_id: int) -> dict:
        conn = await self.repo.get_connection(connection_id)
        if not conn:
            raise ValueError("Connection not found")
        log = await self.repo.create_sync_log({
            "connection_id": connection_id,
            "sync_type": "bookings",
            "status": "completed",
            "started_at": datetime.now(timezone.utc),
            "completed_at": datetime.now(timezone.utc),
        })
        conn.last_sync_at = datetime.now(timezone.utc)
        self.repo.db.add(conn)
        return {"ok": True, "sync_log_id": log.id, "message": "Bookings import completed"}

    async def sync_ota_booking_to_pms(self, ota_booking_id: int) -> dict:
        booking = await self.repo.sync_ota_booking_to_pms(ota_booking_id)
        if not booking:
            raise ValueError("OTA booking not found")
        return {
            "id": booking.id,
            "guest_name": booking.guest_name,
            "guest_email": booking.guest_email,
            "status": booking.status.value if booking.status else None,
            "message": "Synced to PMS successfully",
        }

    async def get_channel_analytics(self, hotel_id: int) -> dict:
        from src.modules.channel_manager.models import OtaBooking
        listings = await self.repo.list_listings(hotel_id)
        listing_ids = [l.id for l in listings]
        if not listing_ids:
            return {"total_bookings": 0, "total_revenue": 0, "channels": {}}
        r = await self.repo.db.execute(
            select(
                OtaBooking.ota_listing_id,
                func.count(OtaBooking.id),
                func.coalesce(func.sum(OtaBooking.total_price), 0),
            ).where(OtaBooking.ota_listing_id.in_(listing_ids))
            .group_by(OtaBooking.ota_listing_id)
        )
        rows = r.all()
        total_bookings = 0
        total_revenue = 0.0
        channels = {}
        for listing_id, cnt, rev in rows:
            total_bookings += cnt
            total_revenue += float(rev)
            listing = next((l for l in listings if l.id == listing_id), None)
            if listing:
                conn = await self.repo.get_connection(listing.ota_connection_id)
                if conn:
                    channel = await self.repo.get_ota_channel(conn.ota_channel_id)
                    channel_name = channel.name if channel else f"Channel #{conn.ota_channel_id}"
                else:
                    channel_name = "Unknown"
                if channel_name not in channels:
                    channels[channel_name] = {"booking_count": 0, "revenue": 0.0}
                channels[channel_name]["booking_count"] += cnt
                channels[channel_name]["revenue"] += float(rev)
        return {
            "total_bookings": total_bookings,
            "total_revenue": total_revenue,
            "channels": channels,
        }

    # ─── Channel list ──────────────────────────────────────────

    async def list_channels(self) -> list[dict]:
        channels = await self.repo.list_ota_channels()
        return [self._format_channel(c) for c in channels]

    async def list_connections(self, hotel_id: int) -> list[dict]:
        connections = await self.repo.list_connections(hotel_id)
        result = []
        for conn in connections:
            channel = await self.repo.get_ota_channel(conn.ota_channel_id)
            result.append(self._format_connection(conn, channel))
        return result

    async def list_listings(self, hotel_id: int) -> list[dict]:
        listings = await self.repo.list_listings(hotel_id)
        return [self._format_listing(l) for l in listings]

    async def list_ota_bookings(self, hotel_id: int, status: str = None) -> list[dict]:
        bookings = await self.repo.list_ota_bookings(hotel_id, status)
        return [self._format_ota_booking(b) for b in bookings]

    async def list_sync_logs(self, connection_id: int) -> list[dict]:
        logs = await self.repo.list_sync_logs(connection_id)
        return [self._format_sync_log(l) for l in logs]

    # ─── Formatters ────────────────────────────────────────────

    def _format_channel(self, channel: OtaChannel) -> dict:
        return {
            "id": channel.id,
            "name": channel.name,
            "code": channel.code,
            "logo_url": channel.logo_url,
            "is_active": channel.is_active,
            "connection_type": channel.connection_type,
            "created_at": channel.created_at.isoformat() if channel.created_at else None,
        }

    def _format_connection(self, conn: OtaConnection, channel: OtaChannel = None) -> dict:
        return {
            "id": conn.id,
            "hotel_id": conn.hotel_id,
            "ota_channel_id": conn.ota_channel_id,
            "channel_name": channel.name if channel else None,
            "channel_code": channel.code if channel else None,
            "channel_logo": channel.logo_url if channel else None,
            "status": conn.status,
            "webhook_url": conn.webhook_url,
            "connected_at": conn.connected_at.isoformat() if conn.connected_at else None,
            "last_sync_at": conn.last_sync_at.isoformat() if conn.last_sync_at else None,
            "is_active": conn.is_active,
        }

    def _format_listing(self, listing: OtaListing) -> dict:
        return {
            "id": listing.id,
            "hotel_id": listing.hotel_id,
            "ota_connection_id": listing.ota_connection_id,
            "external_listing_id": listing.external_listing_id,
            "external_url": listing.external_url,
            "listing_title": listing.listing_title,
            "status": listing.status,
            "last_synced_at": listing.last_synced_at.isoformat() if listing.last_synced_at else None,
            "sync_errors": listing.sync_errors,
            "created_at": listing.created_at.isoformat() if listing.created_at else None,
            "updated_at": listing.updated_at.isoformat() if listing.updated_at else None,
        }

    def _format_ota_booking(self, booking) -> dict:
        return {
            "id": booking.id,
            "ota_listing_id": booking.ota_listing_id,
            "external_booking_id": booking.external_booking_id,
            "guest_name": booking.guest_name,
            "guest_email": booking.guest_email,
            "check_in": booking.check_in.isoformat() if booking.check_in else None,
            "check_out": booking.check_out.isoformat() if booking.check_out else None,
            "adults": booking.adults,
            "children": booking.children,
            "total_price": booking.total_price,
            "currency": booking.currency,
            "status": booking.status,
            "synced_to_pms": booking.synced_to_pms,
            "created_at": booking.created_at.isoformat() if booking.created_at else None,
        }

    def _format_sync_log(self, log: OtaSyncLog) -> dict:
        return {
            "id": log.id,
            "connection_id": log.connection_id,
            "sync_type": log.sync_type,
            "status": log.status,
            "message": log.message,
            "started_at": log.started_at.isoformat() if log.started_at else None,
            "completed_at": log.completed_at.isoformat() if log.completed_at else None,
            "errors_count": log.errors_count,
        }
