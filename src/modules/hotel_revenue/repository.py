from datetime import datetime, timedelta, timezone, date
from sqlalchemy import select, func, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.hotel_revenue.models import HotelRevenueRule, HotelDailyRate, HotelRevenueReport
from src.modules.hotel.models import RoomType, Booking, BookingStatus


class RevenueRuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> HotelRevenueRule:
        rule = HotelRevenueRule(**data)
        self.db.add(rule)
        return rule

    async def get(self, rule_id: int) -> HotelRevenueRule | None:
        r = await self.db.execute(select(HotelRevenueRule).where(HotelRevenueRule.id == rule_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int) -> list[HotelRevenueRule]:
        r = await self.db.execute(
            select(HotelRevenueRule).where(HotelRevenueRule.hotel_id == hotel_id)
            .order_by(HotelRevenueRule.priority, HotelRevenueRule.created_at.desc())
        )
        return list(r.scalars().all())

    async def update(self, rule_id: int, data: dict) -> HotelRevenueRule | None:
        rule = await self.get(rule_id)
        if not rule:
            return None
        for field, val in data.items():
            setattr(rule, field, val)
        rule.updated_at = datetime.now(timezone.utc)
        self.db.add(rule)
        return rule

    async def delete(self, rule_id: int) -> bool:
        r = await self.db.execute(select(HotelRevenueRule).where(HotelRevenueRule.id == rule_id))
        rule = r.scalar_one_or_none()
        if not rule:
            return False
        await self.db.delete(rule)
        return True


class DailyRateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_room_type_and_date(self, room_type_id: int, dt: date) -> HotelDailyRate | None:
        r = await self.db.execute(
            select(HotelDailyRate).where(
                HotelDailyRate.room_type_id == room_type_id,
                HotelDailyRate.date == dt,
            )
        )
        return r.scalar_one_or_none()

    async def upsert(self, hotel_id: int, room_type_id: int, dt: date, data: dict) -> HotelDailyRate:
        existing = await self.get_by_room_type_and_date(room_type_id, dt)
        if existing:
            for field, val in data.items():
                setattr(existing, field, val)
            existing.updated_at = datetime.now(timezone.utc)
            self.db.add(existing)
            return existing
        data["hotel_id"] = hotel_id
        data["room_type_id"] = room_type_id
        data["date"] = dt
        rate = HotelDailyRate(**data)
        self.db.add(rate)
        return rate

    async def list_by_hotel_and_dates(self, hotel_id: int, date_from: date, date_to: date) -> list[HotelDailyRate]:
        r = await self.db.execute(
            select(HotelDailyRate).where(
                HotelDailyRate.hotel_id == hotel_id,
                HotelDailyRate.date >= date_from,
                HotelDailyRate.date <= date_to,
            ).order_by(HotelDailyRate.date)
        )
        return list(r.scalars().all())


class RevenueReportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> HotelRevenueReport:
        report = HotelRevenueReport(**data)
        self.db.add(report)
        return report

    async def list_by_hotel(self, hotel_id: int, limit: int = 30) -> list[HotelRevenueReport]:
        r = await self.db.execute(
            select(HotelRevenueReport).where(HotelRevenueReport.hotel_id == hotel_id)
            .order_by(HotelRevenueReport.report_date.desc()).limit(limit)
        )
        return list(r.scalars().all())

    async def get_by_hotel_and_date(self, hotel_id: int, report_date: date) -> HotelRevenueReport | None:
        r = await self.db.execute(
            select(HotelRevenueReport).where(
                HotelRevenueReport.hotel_id == hotel_id,
                HotelRevenueReport.report_date == report_date,
            )
        )
        return r.scalar_one_or_none()


class RevenueRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rules = RevenueRuleRepository(db)
        self.rates = DailyRateRepository(db)
        self.reports = RevenueReportRepository(db)

    async def calculate_revpar(self, hotel_id: int, date_from: date, date_to: date) -> float:
        rates = await self.rates.list_by_hotel_and_dates(hotel_id, date_from, date_to)
        if not rates:
            return 0.0
        total_revenue = sum(r.final_price or 0 for r in rates)
        total_rooms = sum(r.occupancy_rate or 0 for r in rates)
        total_available = len(rates)
        return round(total_revenue / total_available, 2) if total_available else 0.0

    async def calculate_adr(self, hotel_id: int, date_from: date, date_to: date) -> float:
        rates = await self.rates.list_by_hotel_and_dates(hotel_id, date_from, date_to)
        if not rates:
            return 0.0
        booked = [r for r in rates if (r.occupancy_rate or 0) > 0]
        if not booked:
            return 0.0
        total_revenue = sum(r.final_price or 0 for r in booked)
        return round(total_revenue / len(booked), 2)

    async def get_daily_rates(self, hotel_id: int, date_from: date, date_to: date) -> list[dict]:
        rates = await self.rates.list_by_hotel_and_dates(hotel_id, date_from, date_to)
        return [
            {
                "id": r.id, "hotel_id": r.hotel_id, "room_type_id": r.room_type_id,
                "date": r.date.isoformat() if r.date else None,
                "base_price": r.base_price, "dynamic_price": r.dynamic_price,
                "final_price": r.final_price, "occupancy_rate": r.occupancy_rate,
                "is_boosted": r.is_boosted, "is_sale": r.is_sale,
            }
            for r in rates
        ]

    async def update_daily_rate(self, room_type_id: int, dt: date, data: dict) -> HotelDailyRate:
        return await self.rates.upsert(0, room_type_id, dt, data)

    async def apply_pricing_rule(self, hotel_id: int, rule_id: int) -> dict:
        rule = await self.rules.get(rule_id)
        if not rule:
            raise ValueError("Rule not found")
        r = await self.db.execute(
            select(RoomType).where(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        )
        room_types = list(r.scalars().all())
        today = datetime.now(timezone.utc).date()
        updated = 0
        for rt in room_types:
            for i in range(90):
                dt = today + timedelta(days=i)
                rate = await self.rates.get_by_room_type_and_date(rt.id, dt)
                base = rate.base_price if rate else rt.base_price
                if rule.adjustment_type == "percentage":
                    new_price = base * (1 + (rule.adjustment_value / 100))
                else:
                    new_price = base + rule.adjustment_value
                new_price = max(new_price, 0)
                await self.rates.upsert(hotel_id, rt.id, dt, {
                    "base_price": rt.base_price, "dynamic_price": new_price,
                    "final_price": new_price,
                })
                updated += 1
        return {"rule_id": rule_id, "room_types_updated": len(room_types), "rates_updated": updated}

    async def list_revenue_rules(self, hotel_id: int) -> list[dict]:
        rules = await self.rules.list_by_hotel(hotel_id)
        return [
            {
                "id": r.id, "hotel_id": r.hotel_id, "rule_type": r.rule_type,
                "name": r.name, "is_active": r.is_active, "priority": r.priority,
                "conditions": r.conditions, "adjustment_type": r.adjustment_type,
                "adjustment_value": r.adjustment_value, "min_stay": r.min_stay,
                "max_stay": r.max_stay, "advance_days_min": r.advance_days_min,
                "advance_days_max": r.advance_days_max,
                "occupancy_threshold": r.occupancy_threshold, "day_of_week": r.day_of_week,
                "start_date": r.start_date.isoformat() if r.start_date else None,
                "end_date": r.end_date.isoformat() if r.end_date else None,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in rules
        ]

    async def generate_report(self, hotel_id: int, report_date: date) -> dict:
        existing = await self.reports.get_by_hotel_and_date(hotel_id, report_date)
        if existing:
            return {
                "id": existing.id, "hotel_id": existing.hotel_id,
                "report_date": existing.report_date.isoformat() if existing.report_date else None,
                "revpar": existing.revpar, "adr": existing.adr,
                "occupancy_rate": existing.occupancy_rate,
                "total_revenue": existing.total_revenue,
                "room_revenue": existing.room_revenue,
                "ancillary_revenue": existing.ancillary_revenue,
                "booked_rooms": existing.booked_rooms,
                "available_rooms": existing.available_rooms,
                "cancellation_rate": existing.cancellation_rate,
                "avg_length_of_stay": existing.avg_length_of_stay,
                "created_at": existing.created_at.isoformat() if existing.created_at else None,
            }

        r = await self.db.execute(
            select(func.count(Booking.id), func.sum(Booking.total_price))
            .where(
                Booking.hotel_id == hotel_id,
                func.date(Booking.check_in) == report_date,
                Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.CHECKED_IN, BookingStatus.CHECKED_OUT]),
            )
        )
        row = r.one()
        booked_rooms = row[0] or 0
        room_revenue = float(row[1] or 0)

        cancelled_r = await self.db.execute(
            select(func.count(Booking.id)).where(
                Booking.hotel_id == hotel_id,
                func.date(Booking.check_in) == report_date,
                Booking.status == BookingStatus.CANCELLED,
            )
        )
        cancelled = cancelled_r.scalar() or 0

        room_count_r = await self.db.execute(
            select(RoomType).where(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        )
        room_types = list(room_count_r.scalars().all())
        available_rooms = sum(rt.quantity or 1 for rt in room_types)

        total_booked = booked_rooms + cancelled
        cancellation_rate = round(cancelled / total_booked, 4) if total_booked else 0.0
        occupancy_rate = round(booked_rooms / available_rooms, 4) if available_rooms else 0.0
        revpar = round(room_revenue / available_rooms, 2) if available_rooms else 0.0
        adr = round(room_revenue / booked_rooms, 2) if booked_rooms else 0.0

        report_data = {
            "revpar": revpar,
            "adr": adr,
            "occupancy_rate": occupancy_rate,
            "total_revenue": room_revenue,
            "room_revenue": room_revenue,
            "ancillary_revenue": 0,
            "booked_rooms": booked_rooms,
            "available_rooms": available_rooms,
            "cancellation_rate": cancellation_rate,
            "avg_length_of_stay": 1.0,
        }

        report = await self.reports.create({
            "hotel_id": hotel_id, "report_date": report_date,
            **report_data,
        })
        return {
            "id": report.id, "hotel_id": report.hotel_id,
            "report_date": report.report_date.isoformat() if report.report_date else None,
            **report_data,
            "created_at": report.created_at.isoformat() if report.created_at else None,
        }
