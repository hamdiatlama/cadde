from datetime import datetime, timedelta, timezone, date
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.hotel_revenue.repository import RevenueRepository
from src.modules.hotel_revenue.models import HotelDailyRate
from src.modules.hotel.models import RoomType, Booking, BookingStatus


class HotelRevenueService:
    def __init__(self, db: AsyncSession):
        self.repo = RevenueRepository(db)

    async def calculate_dynamic_price(self, hotel_id: int, room_type_id: int, dt: date) -> float:
        r = await self.repo.db.execute(select(RoomType).where(RoomType.id == room_type_id))
        room = r.scalar_one_or_none()
        if not room:
            raise ValueError("Room type not found")
        base_price = room.base_price
        rules = await self.repo.rules.list_by_hotel(hotel_id)
        active_rules = [rule for rule in rules if rule.is_active and
                        (not rule.start_date or rule.start_date.date() <= dt) and
                        (not rule.end_date or rule.end_date.date() >= dt)]
        if not active_rules:
            return base_price
        price = base_price
        for rule in sorted(active_rules, key=lambda x: x.priority or 0):
            if rule.adjustment_type == "percentage":
                price *= 1 + (rule.adjustment_value / 100)
            else:
                price += rule.adjustment_value
        return round(max(price, 0), 2)

    async def apply_all_rules(self, hotel_id: int) -> dict:
        r = await self.repo.db.execute(
            select(RoomType).where(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        )
        room_types = list(r.scalars().all())
        today = datetime.now(timezone.utc).date()
        total_updated = 0
        for rt in room_types:
            for i in range(90):
                dt = today + timedelta(days=i)
                dynamic = await self.calculate_dynamic_price(hotel_id, rt.id, dt)
                existing = await self.repo.rates.get_by_room_type_and_date(rt.id, dt)
                if existing:
                    existing.dynamic_price = dynamic
                    existing.final_price = dynamic
                    existing.updated_at = datetime.now(timezone.utc)
                    self.repo.db.add(existing)
                else:
                    await self.repo.rates.upsert(hotel_id, rt.id, dt, {
                        "base_price": rt.base_price, "dynamic_price": dynamic,
                        "final_price": dynamic,
                    })
                total_updated += 1
        return {"hotel_id": hotel_id, "room_types": len(room_types), "rates_updated": total_updated}

    async def get_revenue_analytics(self, hotel_id: int, period: str = "daily") -> dict:
        today = datetime.now(timezone.utc).date()
        if period == "weekly":
            date_from = today - timedelta(days=7)
        elif period == "monthly":
            date_from = today - timedelta(days=30)
        else:
            date_from = today - timedelta(days=1)
        rates = await self.repo.rates.list_by_hotel_and_dates(hotel_id, date_from, today)
        total_revenue = sum(r.final_price or 0 for r in rates)
        total_rooms = len(rates)
        booked_count = sum(1 for r in rates if (r.occupancy_rate or 0) > 0)
        revpar = round(total_revenue / total_rooms, 2) if total_rooms else 0.0
        adr = round(total_revenue / booked_count, 2) if booked_count else 0.0
        occupancy = round(booked_count / total_rooms, 4) if total_rooms else 0.0
        daily_data = {}
        for r in rates:
            day_key = r.date.isoformat() if r.date else "unknown"
            if day_key not in daily_data:
                daily_data[day_key] = {"revenue": 0, "booked": 0, "available": 0}
            daily_data[day_key]["revenue"] += r.final_price or 0
            daily_data[day_key]["booked"] += 1 if (r.occupancy_rate or 0) > 0 else 0
            daily_data[day_key]["available"] += 1
        return {
            "revpar": revpar, "adr": adr, "occupancy_rate": occupancy,
            "total_revenue": total_revenue, "period": period,
            "daily_breakdown": daily_data,
        }

    async def generate_daily_report(self, hotel_id: int) -> dict:
        return await self.repo.generate_report(hotel_id, datetime.now(timezone.utc).date())

    async def suggest_optimal_price(self, hotel_id: int, room_type_id: int) -> dict:
        r = await self.repo.db.execute(select(RoomType).where(RoomType.id == room_type_id))
        room = r.scalar_one_or_none()
        if not room:
            raise ValueError("Room type not found")
        today = datetime.now(timezone.utc).date()
        rates = await self.repo.rates.list_by_hotel_and_dates(hotel_id, today, today + timedelta(days=30))
        avg_occupancy = sum(r.occupancy_rate or 0 for r in rates) / len(rates) if rates else 0
        base = room.base_price
        if avg_occupancy > 0.8:
            suggested = base * 1.2
            reason = "Yüksek doluluk (>%80), fiyat artırılmalı"
        elif avg_occupancy > 0.6:
            suggested = base * 1.05
            reason = "Orta doluluk (%60-%80), hafif artış"
        elif avg_occupancy > 0.3:
            suggested = base * 0.95
            reason = "Düşük doluluk (%30-%60), hafif düşüş"
        else:
            suggested = base * 0.85
            reason = "Çok düşük doluluk (<%30), fiyat düşürülmeli"
        current_price = rates[0].final_price if rates else base
        return {
            "room_type_id": room_type_id, "base_price": base,
            "current_price": current_price,
            "suggested_price": round(suggested, 2),
            "avg_occupancy_30d": round(avg_occupancy, 4),
            "reason": reason,
        }
