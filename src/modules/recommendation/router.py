from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.recommendation.repository import RecommendationRepository

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/popular")
async def popular(limit: int = 10, db: AsyncSession = Depends(get_db)):
    repo = RecommendationRepository(db)
    return await repo.get_popular_products(limit)


@router.get("/similar/{product_id}")
async def similar(product_id: int, limit: int = 6, db: AsyncSession = Depends(get_db)):
    repo = RecommendationRepository(db)
    results = await repo.get_similar_products(product_id, limit)
    return results


@router.get("/for-you")
async def for_you(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RecommendationRepository(db)
    return await repo.get_recommendations(current_user.id)


@router.post("/track/view")
async def track_view(
    product_id: int, session_id: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RecommendationRepository(db)
    v = await repo.record_view(current_user.id, product_id, session_id)
    await db.commit()
    return {"id": v.id}


@router.post("/track/search")
async def track_search(
    query: str, session_id: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RecommendationRepository(db)
    s = await repo.record_search(current_user.id, query, session_id)
    await db.commit()
    return {"id": s.id}
