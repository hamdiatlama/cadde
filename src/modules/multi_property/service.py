import uuid
from datetime import datetime, timezone, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.multi_property.repository import PropertyGroupRepository
from src.modules.multi_property.models import PropertyGroup, PropertyGroupMember, PropertyGroupInvite
from src.modules.hotel.models import Booking, Hotel


class PropertyGroupService:
    def __init__(self, db: AsyncSession):
        self.repo = PropertyGroupRepository(db)
        self.db = db

    async def create_group(self, owner_id: int, name: str, description: str = None, logo_url: str = None):
        group = await self.repo.create_group({
            "owner_id": owner_id,
            "name": name,
            "description": description,
            "logo_url": logo_url,
        })
        return group

    async def invite_member(self, group_id: int, email: str, role: str, invited_by: int):
        data = {
            "group_id": group_id,
            "email": email,
            "role": role,
            "invited_by": invited_by,
        }
        invite = await self.repo.create_invite(data)
        return invite

    async def accept_group_invite(self, token: str, user_id: int):
        inv = await self.repo.accept_invite(token)
        if not inv:
            return None
        if inv.status != "accepted":
            inv.status = "accepted"
        return inv

    async def get_group_dashboard(self, group_id: int):
        members = await self.repo.list_group_hotels(group_id)
        hotel_ids = [m.hotel_id for m in members]
        hotel_data = []
        total_revenue = 0
        total_bookings = 0
        for hid in hotel_ids:
            h_r = await self.db.execute(select(Hotel).where(Hotel.id == hid))
            hotel = h_r.scalar_one_or_none()
            if not hotel:
                continue
            b_r = await self.db.execute(
                select(func.count(), func.coalesce(func.sum(Booking.total_price), 0))
                .where(Booking.hotel_id == hid, Booking.status.in_(["confirmed", "checked_in", "checked_out"]))
            )
            count, revenue = b_r.one()
            total_bookings += count
            total_revenue += revenue
            hotel_data.append({
                "hotel_id": hid,
                "hotel_name": hotel.name,
                "city": hotel.city,
                "rating": hotel.rating,
                "booking_count": count,
                "revenue": revenue,
            })
        avg_occupancy = 0
        avg_revpar = 0
        if hotel_data:
            avg_occupancy = sum(h.get("booking_count", 0) for h in hotel_data) / len(hotel_data)
            avg_revpar = total_revenue / len(hotel_data) if total_revenue else 0
        return {
            "group_id": group_id,
            "total_hotels": len(hotel_data),
            "total_revenue": total_revenue,
            "total_bookings": total_bookings,
            "avg_occupancy": round(avg_occupancy, 2),
            "avg_revpar": round(avg_revpar, 2),
            "hotels": hotel_data,
        }

    async def generate_consolidated_report(self, group_id: int):
        dashboard = await self.get_group_dashboard(group_id)
        today = date.today()
        existing = await self.repo.get_consolidated_report(group_id, today)
        data = {
            "group_id": group_id,
            "report_date": today,
            "total_revenue": dashboard["total_revenue"],
            "total_bookings": dashboard["total_bookings"],
            "avg_occupancy": dashboard["avg_occupancy"],
            "avg_revpar": dashboard["avg_revpar"],
            "total_hotels": dashboard["total_hotels"],
            "report_data": {"hotels": dashboard["hotels"]},
        }
        if existing:
            for k, v in data.items():
                if hasattr(existing, k):
                    setattr(existing, k, v)
            return existing
        return await self.repo.save_report(data)
