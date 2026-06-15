from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.energy_manager.service import EnergyManagerService
from src.modules.energy_manager.repository import EnergyMeterRepository

router = APIRouter(prefix="/energy-manager", tags=["energy_manager"])


def get_service(db: AsyncSession = Depends(get_db)) -> EnergyManagerService:
    return EnergyManagerService(db)


# ─── Meters ────────────────────────────────────────────────────────

@router.get("/meters/{hotel_id}")
async def list_meters(
    hotel_id: int,
    meter_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    repo = EnergyMeterRepository(db)
    meters = await repo.list_meters(hotel_id, meter_type)
    return meters


@router.post("/meters", status_code=201)
async def create_meter(
    hotel_id: int = Query(...),
    meter_type: str = Query(...),
    meter_name: str = Query(...),
    location: str = Query(None),
    unit: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EnergyMeterRepository(db)
    data = {
        "hotel_id": hotel_id,
        "meter_type": meter_type,
        "meter_name": meter_name,
        "location": location,
        "unit": unit,
    }
    meter = await repo.create(data)
    await db.commit()
    return {
        "id": meter.id,
        "hotel_id": meter.hotel_id,
        "meter_type": meter.meter_type,
        "meter_name": meter.meter_name,
        "location": meter.location,
        "unit": meter.unit,
        "is_active": meter.is_active,
    }


# ─── Readings ──────────────────────────────────────────────────────

@router.post("/readings", status_code=201)
async def log_reading(
    meter_id: int = Query(...),
    value: float = Query(...),
    source: str = Query("manual"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.log_meter_reading(meter_id, value, source)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/readings/{meter_id}")
async def get_readings(
    meter_id: int,
    date_from: str = Query(None),
    date_to: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    repo = EnergyMeterRepository(db)
    readings = await repo.get_readings(meter_id, date_from, date_to)
    return readings


# ─── Summary & Reports ─────────────────────────────────────────────

@router.get("/summary/{hotel_id}")
async def consumption_summary(
    hotel_id: int,
    date_from: str = Query(None),
    date_to: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    repo = EnergyMeterRepository(db)
    return await repo.get_consumption_summary(hotel_id, date_from, date_to)


@router.get("/reports/{hotel_id}")
async def list_reports(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.get_reports(hotel_id)


@router.post("/generate-report/{hotel_id}", status_code=201)
async def generate_report(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    result = await service.generate_daily_report(hotel_id)
    await db.commit()
    return result


@router.get("/dashboard/{hotel_id}")
async def energy_dashboard(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.get_energy_dashboard(hotel_id)


# ─── Saving Rules ──────────────────────────────────────────────────

@router.get("/rules/{hotel_id}")
async def list_saving_rules(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_saving_rules(hotel_id)


@router.post("/rules", status_code=201)
async def create_rule(
    hotel_id: int = Query(...),
    rule_name: str = Query(...),
    trigger_type: str = Query(...),
    conditions: str = Query("{}"),
    actions: str = Query("{}"),
    estimated_savings_percent: float = Query(0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    data = {
        "rule_name": rule_name,
        "trigger_type": trigger_type,
        "conditions": conditions,
        "actions": actions,
        "estimated_savings_percent": estimated_savings_percent,
    }
    result = await service.create_saving_rule(hotel_id, data)
    await db.commit()
    return result


@router.put("/rules/{rule_id}")
async def update_rule(
    rule_id: int,
    rule_name: str = Query(None),
    trigger_type: str = Query(None),
    conditions: str = Query(None),
    actions: str = Query(None),
    estimated_savings_percent: float = Query(None),
    is_active: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    data = {k: v for k, v in {
        "rule_name": rule_name,
        "trigger_type": trigger_type,
        "conditions": conditions,
        "actions": actions,
        "estimated_savings_percent": estimated_savings_percent,
        "is_active": is_active,
    }.items() if v is not None}
    result = await service.update_saving_rule(rule_id, data)
    if not result:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return result


@router.delete("/rules/{rule_id}")
async def delete_rule(
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    ok = await service.delete_saving_rule(rule_id)
    if not ok:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return {"ok": True}


# ─── Certifications ────────────────────────────────────────────────

@router.get("/certifications/{hotel_id}")
async def list_certifications(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_certifications(hotel_id)


@router.post("/certifications", status_code=201)
async def add_certification(
    hotel_id: int = Query(...),
    certification_name: str = Query(...),
    issuing_body: str = Query(None),
    certificate_number: str = Query(None),
    awarded_date: str = Query(None),
    expiry_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    from datetime import date
    data = {
        "certification_name": certification_name,
        "issuing_body": issuing_body,
        "certificate_number": certificate_number,
        "awarded_date": date.fromisoformat(awarded_date) if awarded_date else None,
        "expiry_date": date.fromisoformat(expiry_date) if expiry_date else None,
    }
    result = await service.register_certification(hotel_id, data)
    await db.commit()
    return result
