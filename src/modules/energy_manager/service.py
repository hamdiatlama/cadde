from datetime import datetime, timezone, date
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.energy_manager.repository import (
    EnergyMeterRepository, EnergySavingRuleRepository,
    SustainabilityCertificationRepository,
)


class EnergyManagerService:
    def __init__(self, db: AsyncSession):
        self.meter_repo = EnergyMeterRepository(db)
        self.rule_repo = EnergySavingRuleRepository(db)
        self.cert_repo = SustainabilityCertificationRepository(db)
        self.db = db

    # ─── Meter Readings ─────────────────────────────────────────

    async def log_meter_reading(self, meter_id: int, value: float, source: str = "manual") -> dict:
        reading = await self.meter_repo.log_reading(meter_id, value, source)
        await self.db.flush()
        return self._format_reading(reading)

    async def generate_daily_report(self, hotel_id: int) -> dict:
        today = date.today()
        report = await self.meter_repo.generate_consumption_report(hotel_id, today)
        await self.db.flush()
        return self._format_report(report)

    async def get_energy_dashboard(self, hotel_id: int) -> dict:
        today = date.today()
        year_start = date(today.year, 1, 1)
        year_summary = await self.meter_repo.get_consumption_summary(
            hotel_id,
            datetime.combine(year_start, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )
        month_start = date(today.year, today.month, 1)
        month_summary = await self.meter_repo.get_consumption_summary(
            hotel_id,
            datetime.combine(month_start, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )
        today_summary = await self.meter_repo.get_consumption_summary(
            hotel_id,
            datetime.combine(today, datetime.min.time()),
            datetime.combine(today, datetime.max.time()),
        )

        meters = await self.meter_repo.list_meters(hotel_id)
        reports_raw = await self.meter_repo.list_reports(hotel_id)
        report = reports_raw[0] if reports_raw else None

        certs = await self.cert_repo.list_certifications(hotel_id)
        rules = await self.rule_repo.list_rules(hotel_id)

        return {
            "today": today_summary,
            "this_month": month_summary,
            "this_year": year_summary,
            "total_cost": report.total_cost if report else 0,
            "occupancy_rate": report.occupancy_rate if report else 0,
            "cost_per_occupied_room": report.cost_per_occupied_room if report else 0,
            "meter_count": len(meters),
            "active_rules": len([r for r in rules if r.is_active]),
            "verified_certifications": len([c for c in certs if c.is_verified]),
            "certs": [self._format_cert(c) for c in certs],
        }

    async def get_reports(self, hotel_id: int) -> list[dict]:
        reports = await self.meter_repo.list_reports(hotel_id)
        return [self._format_report(r) for r in reports]

    # ─── Saving Rules ───────────────────────────────────────────

    async def create_saving_rule(self, hotel_id: int, data: dict) -> dict:
        data["hotel_id"] = hotel_id
        if isinstance(data.get("conditions"), str):
            import json
            data["conditions"] = json.loads(data["conditions"])
        if isinstance(data.get("actions"), str):
            import json
            data["actions"] = json.loads(data["actions"])
        rule = await self.rule_repo.create(data)
        await self.db.flush()
        return self._format_rule(rule)

    async def update_saving_rule(self, rule_id: int, data: dict) -> dict | None:
        rule = await self.rule_repo.update(rule_id, data)
        if not rule:
            return None
        await self.db.flush()
        return self._format_rule(rule)

    async def delete_saving_rule(self, rule_id: int) -> bool:
        return await self.rule_repo.delete(rule_id)

    async def list_saving_rules(self, hotel_id: int) -> list[dict]:
        rules = await self.rule_repo.list_rules(hotel_id)
        return [self._format_rule(r) for r in rules]

    async def estimate_savings(self, rule_id: int) -> dict:
        rule = await self.rule_repo.get(rule_id)
        if not rule:
            raise ValueError("Rule not found")
        savings_percent = rule.estimated_savings_percent or 0
        reports = await self.meter_repo.list_reports(rule.hotel_id)
        latest = reports[0] if reports else None
        current_cost = latest.total_cost if latest else 10000
        estimated_saving = current_cost * (savings_percent / 100)
        return {
            "rule_id": rule.id,
            "rule_name": rule.rule_name,
            "current_monthly_cost": current_cost,
            "estimated_savings_percent": savings_percent,
            "estimated_monthly_saving": round(estimated_saving, 2),
            "estimated_yearly_saving": round(estimated_saving * 12, 2),
        }

    async def apply_saving_rule(self, rule_id: int) -> dict:
        rule = await self.rule_repo.get(rule_id)
        if not rule:
            raise ValueError("Rule not found")
        actions = rule.actions or {}
        executed = []
        if rule.trigger_type == "occupancy" and actions.get("set_temperature"):
            executed.append(f"Temperature set to {actions['set_temperature']}°C")
        if actions.get("turn_off_lights"):
            executed.append("Lights turned off in unoccupied areas")
        if actions.get("reduce_hvac"):
            executed.append(f"HVAC reduced to {actions['reduce_hvac']}%")
        if actions.get("schedule_equipment"):
            executed.append(f"Equipment scheduled: {actions['schedule_equipment']}")
        return {
            "rule_id": rule.id,
            "rule_name": rule.rule_name,
            "trigger_type": rule.trigger_type,
            "actions_executed": executed,
            "status": "applied",
        }

    # ─── Certifications ─────────────────────────────────────────

    async def register_certification(self, hotel_id: int, data: dict) -> dict:
        data["hotel_id"] = hotel_id
        cert = await self.cert_repo.create(data)
        await self.db.flush()
        return self._format_cert(cert)

    async def list_certifications(self, hotel_id: int) -> list[dict]:
        certs = await self.cert_repo.list_certifications(hotel_id)
        return [self._format_cert(c) for c in certs]

    # ─── Helpers ────────────────────────────────────────────────

    def _format_reading(self, r) -> dict:
        return {
            "id": r.id,
            "meter_id": r.meter_id,
            "reading_value": r.reading_value,
            "unit": r.unit,
            "reading_date": r.reading_date.isoformat() if r.reading_date else None,
            "source": r.source,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }

    def _format_report(self, r) -> dict:
        return {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "report_date": r.report_date.isoformat() if r.report_date else None,
            "total_electricity_kwh": r.total_electricity_kwh,
            "total_water_m3": r.total_water_m3,
            "total_gas_m3": r.total_gas_m3,
            "total_cost": r.total_cost,
            "electricity_cost": r.electricity_cost,
            "water_cost": r.water_cost,
            "gas_cost": r.gas_cost,
            "occupancy_rate": r.occupancy_rate,
            "cost_per_occupied_room": r.cost_per_occupied_room,
            "report_data": r.report_data,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }

    def _format_rule(self, r) -> dict:
        return {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "rule_name": r.rule_name,
            "trigger_type": r.trigger_type,
            "conditions": r.conditions,
            "actions": r.actions,
            "estimated_savings_percent": r.estimated_savings_percent,
            "is_active": r.is_active,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }

    def _format_cert(self, c) -> dict:
        return {
            "id": c.id,
            "hotel_id": c.hotel_id,
            "certification_name": c.certification_name,
            "issuing_body": c.issuing_body,
            "certificate_number": c.certificate_number,
            "awarded_date": c.awarded_date.isoformat() if c.awarded_date else None,
            "expiry_date": c.expiry_date.isoformat() if c.expiry_date else None,
            "is_verified": c.is_verified,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
