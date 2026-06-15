from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.reputation.models import ReputationAlert
from src.modules.reputation.service import ReputationService

router = APIRouter(prefix="/reputation", tags=["reputation"])


@router.get("/{hotel_id}")
async def get_reputation_dashboard(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    return await svc.get_reputation_dashboard(hotel_id)


@router.get("/{hotel_id}/reviews")
async def list_external_reviews(
    hotel_id: int,
    platform: str | None = Query(None),
    sentiment: str | None = Query(None),
    date_from: str | None = Query(None),
    date_to: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    df = datetime.fromisoformat(date_from) if date_from else None
    dt = datetime.fromisoformat(date_to) if date_to else None
    return await svc.repo.list_external_reviews(hotel_id, platform, sentiment, df, dt)


@router.post("/{hotel_id}/reviews", status_code=status.HTTP_201_CREATED)
async def import_external_review(
    hotel_id: int,
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    platform = body.get("platform")
    if platform not in ("booking_com", "google", "tripadvisor", "expedia"):
        raise HTTPException(400, "Invalid platform")
    result = await svc.import_external_review(hotel_id, platform, body)
    await db.commit()
    return result


@router.post("/reviews/{review_id}/respond")
async def respond_to_review(
    review_id: int,
    body: dict,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    try:
        result = await svc.respond_to_review(review_id, body.get("response_text", ""), current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/{hotel_id}/alerts")
async def list_alerts(
    hotel_id: int,
    is_resolved: bool | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    return await svc.repo.list_alerts(hotel_id, is_resolved)


@router.put("/alerts/{alert_id}/resolve")
async def resolve_alert(
    alert_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    alert = await svc.repo.alerts.resolve(alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    await db.commit()
    return {"id": alert.id, "is_resolved": True, "message": "Alert resolved"}


@router.post("/{hotel_id}/recalculate")
async def recalculate_score(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    result = await svc.update_reputation_score(hotel_id)
    await db.commit()
    return result


@router.get("/{hotel_id}/sentiment")
async def get_sentiment_breakdown(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = ReputationService(db)
    return await svc.get_sentiment_breakdown(hotel_id)
