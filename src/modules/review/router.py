from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.review.service import ReviewService

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_review(
    order_id: int, product_id: int, rating: int,
    comment: str = None, title: str = None, photo_urls: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReviewService(db)
    review, err = await svc.create_review(
        current_user.id, order_id, product_id, rating, comment, title, photo_urls
    )
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    await db.refresh(review)
    return {"id": review.id, "rating": review.rating, "message": "Review submitted successfully"}

@router.get("/product/{product_id}", response_model=list[dict])
async def get_product_reviews(
    product_id: int, page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    svc = ReviewService(db)
    return await svc.get_product_reviews(product_id, page, per_page)

@router.get("/my", response_model=list[dict])
async def get_my_reviews(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ReviewService(db)
    return await svc.get_my_reviews(current_user.id)
