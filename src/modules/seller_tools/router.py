from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.seller_tools.repository import ListingScoreRepository, SellerAcademyRepository

router = APIRouter(prefix="/seller-tools", tags=["seller_tools"])


@router.post("/listing-score/{product_id}")
async def calculate_listing_score(
    product_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ListingScoreRepository(db)
    try:
        result = await repo.calculate_score(product_id)
    except ValueError as e:
        raise HTTPException(404, str(e))
    await db.commit()
    return result


@router.get("/listing-score/{product_id}")
async def get_listing_score(
    product_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ListingScoreRepository(db)
    result = await repo.get_score(product_id)
    if not result:
        raise HTTPException(404, "Score not found")
    return result


@router.get("/listing-score/{product_id}/suggestions")
async def get_listing_suggestions(
    product_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = ListingScoreRepository(db)
    result = await repo.get_suggestions(product_id)
    if not result:
        raise HTTPException(404, "Suggestions not found")
    return result


@router.post("/academy/courses", status_code=201)
async def create_course(
    title: str, description: str = None, content_url: str = None,
    category: str = None, duration_minutes: int = None, is_published: bool = False,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = SellerAcademyRepository(db)
    course = await repo.create_course(title, description, content_url, category, duration_minutes, is_published)
    await db.commit()
    return course


@router.get("/academy/courses")
async def list_courses(
    category: str = Query(None), published_only: bool = True,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = SellerAcademyRepository(db)
    return await repo.list_courses(category, published_only)


@router.post("/academy/courses/{course_id}/complete")
async def complete_course(
    course_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = SellerAcademyRepository(db)
    progress = await repo.track_progress(current_user.id, course_id)
    await db.commit()
    return progress


@router.get("/academy/progress")
async def get_academy_progress(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = SellerAcademyRepository(db)
    return await repo.get_progress(current_user.id)
