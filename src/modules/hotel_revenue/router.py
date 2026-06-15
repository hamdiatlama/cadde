from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.hotel_revenue.service import HotelRevenueService
from src.modules.hotel_revenue.repository import RevenueRepository
from datetime import datetime, date

router = APIRouter(prefix="/hotel-revenue", tags=["hotel_revenue"])


def get_service(db: AsyncSession = Depends(get_db)) -> HotelRevenueService:
    return HotelRevenueService(db)


@router.get("/rules/{hotel_id}")
async def list_rules(hotel_id: int, db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    return await repo.list_revenue_rules(hotel_id)


@router.post("/rules", status_code=201)
async def create_rule(rule_data: dict, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    rule = await repo.rules.create(rule_data)
    await db.commit()
    return {"id": rule.id, "name": rule.name, "rule_type": rule.rule_type}


@router.put("/rules/{rule_id}")
async def update_rule(rule_id: int, rule_data: dict, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    rule = await repo.rules.update(rule_id, rule_data)
    if not rule:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return {"id": rule.id, "name": rule.name, "rule_type": rule.rule_type}


@router.delete("/rules/{rule_id}")
async def delete_rule(rule_id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    ok = await repo.rules.delete(rule_id)
    if not ok:
        raise HTTPException(404, "Rule not found")
    await db.commit()
    return {"ok": True}


@router.get("/daily-rates/{hotel_id}")
async def get_daily_rates(hotel_id: int, date_from: str = Query(...), date_to: str = Query(...),
                          db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    try:
        df = date.fromisoformat(date_from)
        dt = date.fromisoformat(date_to)
    except ValueError:
        raise HTTPException(400, "Invalid date format")
    return await repo.get_daily_rates(hotel_id, df, dt)


@router.post("/apply-rules/{hotel_id}")
async def apply_rules(hotel_id: int, current_user: User = Depends(get_current_user),
                      db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    result = await service.apply_all_rules(hotel_id)
    await db.commit()
    return result


@router.get("/analytics/{hotel_id}")
async def get_analytics(hotel_id: int, period: str = Query("daily"),
                        db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    return await service.get_revenue_analytics(hotel_id, period)


@router.get("/reports/{hotel_id}")
async def list_reports(hotel_id: int, db: AsyncSession = Depends(get_db)):
    repo = RevenueRepository(db)
    reports = await repo.reports.list_by_hotel(hotel_id)
    return [
        {
            "id": r.id, "report_date": r.report_date.isoformat() if r.report_date else None,
            "revpar": r.revpar, "adr": r.adr, "occupancy_rate": r.occupancy_rate,
            "total_revenue": r.total_revenue, "booked_rooms": r.booked_rooms,
            "available_rooms": r.available_rooms, "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in reports
    ]


@router.post("/generate-report/{hotel_id}")
async def generate_report(hotel_id: int, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    result = await service.generate_daily_report(hotel_id)
    await db.commit()
    return result
