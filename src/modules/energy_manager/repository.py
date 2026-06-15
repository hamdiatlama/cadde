import json
from datetime import datetime, timezone, date
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.energy_manager.models import (
    EnergyMeter, EnergyReading, EnergyConsumptionReport,
    EnergySavingRule, SustainabilityCertification,
)


class EnergyMeterRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> EnergyMeter:
        obj = EnergyMeter(**data)
        self.db.add(obj)
        return obj

    async def get(self, meter_id: int) -> EnergyMeter | None:
        r = await self.db.execute(select(EnergyMeter).where(EnergyMeter.id == meter_id))
        return r.scalar_one_or_none()

    async def update(self, meter_id: int, data: dict) -> EnergyMeter | None:
        obj = await self.get(meter_id)
        if not obj:
            return None
        for field, val in data.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def delete(self, meter_id: int) -> bool:
        obj = await self.get(meter_id)
        if not obj:
            return False
        await self.db.delete(obj)
        return True

    async def list_meters(self, hotel_id: int, meter_type: str = None) -> list[EnergyMeter]:
        query = select(EnergyMeter).where(EnergyMeter.hotel_id == hotel_id)
        if meter_type:
            query = query.where(EnergyMeter.meter_type == meter_type)
        query = query.order_by(EnergyMeter.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def log_reading(self, meter_id: int, reading_value: float, source: str = "manual") -> EnergyReading:
        meter = await self.get(meter_id)
        if not meter:
            raise ValueError("Meter not found")
        reading = EnergyReading(
            meter_id=meter_id,
            reading_value=reading_value,
            unit=meter.unit,
            reading_date=datetime.now(timezone.utc),
            source=source,
        )
        self.db.add(reading)
        return reading

    async def get_readings(self, meter_id: int, date_from=None, date_to=None) -> list[EnergyReading]:
        query = select(EnergyReading).where(EnergyReading.meter_id == meter_id)
        if date_from:
            query = query.where(EnergyReading.reading_date >= date_from)
        if date_to:
            query = query.where(EnergyReading.reading_date <= date_to)
        query = query.order_by(EnergyReading.reading_date.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def get_consumption_summary(self, hotel_id: int, date_from=None, date_to=None) -> dict:
        meter_ids_q = await self.db.execute(
            select(EnergyMeter.id).where(EnergyMeter.hotel_id == hotel_id)
        )
        meter_ids = [row[0] for row in meter_ids_q.all()]
        if not meter_ids:
            return {"electricity": 0, "water": 0, "gas": 0}

        query = select(
            EnergyReading.meter_id,
            func.sum(EnergyReading.reading_value),
        ).where(EnergyReading.meter_id.in_(meter_ids))

        if date_from:
            query = query.where(EnergyReading.reading_date >= date_from)
        if date_to:
            query = query.where(EnergyReading.reading_date <= date_to)
        query = query.group_by(EnergyReading.meter_id)

        r = await self.db.execute(query)
        rows = dict(r.all())

        meters_q = await self.db.execute(
            select(EnergyMeter).where(EnergyMeter.id.in_(meter_ids))
        )
        meters = list(meters_q.scalars().all())

        result = {"electricity": 0.0, "water": 0.0, "gas": 0.0}
        for m in meters:
            total = rows.get(m.id, 0) or 0
            key = m.meter_type
            if key in result:
                result[key] += float(total)
        return result

    async def generate_consumption_report(self, hotel_id: int, report_date: date) -> EnergyConsumptionReport:
        date_from = datetime.combine(report_date, datetime.min.time())
        date_to = datetime.combine(report_date, datetime.max.time())
        summary = await self.get_consumption_summary(hotel_id, date_from, date_to)

        electricity_price_per_kwh = 1.5
        water_price_per_m3 = 10.0
        gas_price_per_m3 = 5.0

        electricity_cost = summary["electricity"] * electricity_price_per_kwh
        water_cost = summary["water"] * water_price_per_m3
        gas_cost = summary["gas"] * gas_price_per_m3
        total_cost = electricity_cost + water_cost + gas_cost

        r = await self.db.execute(
            select(func.count()).select_from(EnergyMeter).where(
                EnergyMeter.hotel_id == hotel_id, EnergyMeter.is_active == True,
            )
        )
        # occupancy is placeholder; real impl would query bookings
        occupancy_rate = 0.65
        total_rooms = r.scalar() or 1
        cost_per_occupied_room = total_cost / (total_rooms * occupancy_rate) if occupancy_rate > 0 else 0

        report = EnergyConsumptionReport(
            hotel_id=hotel_id,
            report_date=report_date,
            total_electricity_kwh=summary["electricity"],
            total_water_m3=summary["water"],
            total_gas_m3=summary["gas"],
            total_cost=total_cost,
            electricity_cost=electricity_cost,
            water_cost=water_cost,
            gas_cost=gas_cost,
            occupancy_rate=occupancy_rate,
            cost_per_occupied_room=cost_per_occupied_room,
            report_data=json.dumps(summary),
        )
        self.db.add(report)
        return report

    async def list_reports(self, hotel_id: int) -> list[EnergyConsumptionReport]:
        r = await self.db.execute(
            select(EnergyConsumptionReport)
            .where(EnergyConsumptionReport.hotel_id == hotel_id)
            .order_by(EnergyConsumptionReport.report_date.desc())
        )
        return list(r.scalars().all())

    async def get_report(self, report_id: int) -> EnergyConsumptionReport | None:
        r = await self.db.execute(
            select(EnergyConsumptionReport).where(EnergyConsumptionReport.id == report_id)
        )
        return r.scalar_one_or_none()


class EnergySavingRuleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> EnergySavingRule:
        obj = EnergySavingRule(**data)
        self.db.add(obj)
        return obj

    async def get(self, rule_id: int) -> EnergySavingRule | None:
        r = await self.db.execute(select(EnergySavingRule).where(EnergySavingRule.id == rule_id))
        return r.scalar_one_or_none()

    async def update(self, rule_id: int, data: dict) -> EnergySavingRule | None:
        obj = await self.get(rule_id)
        if not obj:
            return None
        for field, val in data.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def delete(self, rule_id: int) -> bool:
        obj = await self.get(rule_id)
        if not obj:
            return False
        await self.db.delete(obj)
        return True

    async def list_rules(self, hotel_id: int) -> list[EnergySavingRule]:
        r = await self.db.execute(
            select(EnergySavingRule)
            .where(EnergySavingRule.hotel_id == hotel_id)
            .order_by(EnergySavingRule.created_at.desc())
        )
        return list(r.scalars().all())


class SustainabilityCertificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SustainabilityCertification:
        obj = SustainabilityCertification(**data)
        self.db.add(obj)
        return obj

    async def get(self, cert_id: int) -> SustainabilityCertification | None:
        r = await self.db.execute(
            select(SustainabilityCertification).where(SustainabilityCertification.id == cert_id)
        )
        return r.scalar_one_or_none()

    async def update(self, cert_id: int, data: dict) -> SustainabilityCertification | None:
        obj = await self.get(cert_id)
        if not obj:
            return None
        for field, val in data.items():
            setattr(obj, field, val)
        self.db.add(obj)
        return obj

    async def delete(self, cert_id: int) -> bool:
        obj = await self.get(cert_id)
        if not obj:
            return False
        await self.db.delete(obj)
        return True

    async def list_certifications(self, hotel_id: int) -> list[SustainabilityCertification]:
        r = await self.db.execute(
            select(SustainabilityCertification)
            .where(SustainabilityCertification.hotel_id == hotel_id)
            .order_by(SustainabilityCertification.created_at.desc())
        )
        return list(r.scalars().all())
