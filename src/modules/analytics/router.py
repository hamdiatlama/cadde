from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.analytics.repository import AnalyticsReportRepository, SavedDashboardRepository, RfmSegmentRepository
from datetime import datetime, timezone

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/reports", status_code=201)
async def create_report(data: dict, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    repo = AnalyticsReportRepository(db)
    data["seller_id"] = current_user.id
    data["last_generated_at"] = datetime.now(timezone.utc)
    report = await repo.create(data)
    result = await repo.generate(report)
    await db.commit()
    return {"id": report.id, "name": report.name, "data": result}


@router.get("/reports")
async def list_reports(current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    repo = AnalyticsReportRepository(db)
    return await repo.list_reports(current_user.id)


@router.get("/reports/{id}/data")
async def get_report_data(id: int, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    repo = AnalyticsReportRepository(db)
    r = await db.execute(
        select(AnalyticsReport).where(AnalyticsReport.id == id, AnalyticsReport.seller_id == current_user.id)
    )
    from src.modules.analytics.models import AnalyticsReport
    report = r.scalar_one_or_none()
    if not report:
        raise HTTPException(404, "Report not found")
    data = await repo.generate(report)
    return data


@router.post("/dashboards", status_code=201)
async def create_dashboard(data: dict, current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    repo = SavedDashboardRepository(db)
    data["seller_id"] = current_user.id
    d = await repo.create(data)
    await db.commit()
    return {"id": d.id, "name": d.name}


@router.get("/dashboards")
async def list_dashboards(current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    repo = SavedDashboardRepository(db)
    return await repo.list_all(current_user.id)


@router.put("/dashboards/{id}/default")
async def set_default_dashboard(id: int, current_user: User = Depends(get_current_user),
                                db: AsyncSession = Depends(get_db)):
    repo = SavedDashboardRepository(db)
    d = await repo.set_default(id, current_user.id)
    if not d:
        raise HTTPException(404, "Dashboard not found")
    await db.commit()
    return {"id": d.id, "is_default": d.is_default}


@router.post("/rfm/calculate")
async def calculate_rfm(current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    repo = RfmSegmentRepository(db)
    segments = await repo.calculate(current_user.id)
    await db.commit()
    return [{"name": s.name, "customer_count": s.customer_count} for s in segments]


@router.get("/rfm/segments")
async def get_rfm_segments(current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    repo = RfmSegmentRepository(db)
    segments = await repo.get_segments(current_user.id)
    return [{"id": s.id, "name": s.name, "customer_count": s.customer_count} for s in segments]
