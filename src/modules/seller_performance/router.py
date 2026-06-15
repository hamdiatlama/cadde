from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.seller_performance.repository import SellerPerformanceRepository

router = APIRouter(prefix="/seller-performance", tags=["seller_performance"])


@router.get("/{seller_id}")
async def get_seller_performance(seller_id: int, period: str = "30d", db: AsyncSession = Depends(get_db)):
    repo = SellerPerformanceRepository(db)
    avg = await repo.get_avg_rating(seller_id)
    count = await repo.get_rating_count(seller_id)
    badges = await repo.get_badges(seller_id)
    metrics = await repo.get_metrics(seller_id, period)
    return {
        "seller_id": seller_id,
        "avg_rating": avg,
        "rating_count": count,
        "badges": [{"type": b.badge_type, "awarded_at": b.awarded_at.isoformat() if b.awarded_at else None} for b in badges],
        "metrics": {
            "total_orders": metrics.total_orders if metrics else 0,
            "completed_orders": metrics.completed_orders if metrics else 0,
            "cancelled_orders": metrics.cancelled_orders if metrics else 0,
            "avg_rating": metrics.avg_rating if metrics else avg,
            "on_time_rate": metrics.on_time_rate if metrics else 100,
        } if metrics else None
    }


@router.post("/rate", status_code=201)
async def rate_seller(seller_id: int, order_id: int, rating: int, review: str = None,
                       current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if rating < 1 or rating > 5:
        raise HTTPException(400, "Rating must be 1-5")
    repo = SellerPerformanceRepository(db)
    sr = await repo.add_rating(seller_id, current_user.id, order_id, rating, review)
    await db.commit()
    return {"id": sr.id, "rating": sr.rating}


@router.post("/badge", status_code=201)
async def award_badge(seller_id: int, badge_type: str,
                       current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SellerPerformanceRepository(db)
    b = await repo.award_badge(seller_id, badge_type)
    await db.commit()
    return {"id": b.id, "badge_type": b.badge_type}


@router.post("/calculate-metrics/{seller_id}")
async def calculate_metrics(seller_id: int, period: str = "30d",
                             current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = SellerPerformanceRepository(db)
    m = await repo.calculate_metrics(seller_id, period)
    await db.commit()
    return {"id": m.id, "period": m.period, "total_orders": m.total_orders, "on_time_rate": m.on_time_rate}
