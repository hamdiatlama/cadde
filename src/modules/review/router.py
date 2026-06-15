from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.review.models import Review, ReviewMedia
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


@router.post("/{review_id}/media", status_code=201)
async def upload_review_media(
    review_id: int, media_type: str, url: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    review = await db.get(Review, review_id)
    if not review:
        raise HTTPException(404, "Review not found")
    media = ReviewMedia(review_id=review_id, media_type=media_type, url=url)
    db.add(media)
    await db.commit()
    await db.refresh(media)
    return media


@router.get("/{review_id}/media")
async def list_review_media(
    review_id: int,
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(ReviewMedia).where(ReviewMedia.review_id == review_id).order_by(ReviewMedia.created_at.desc())
    )
    media = r.scalars().all()
    return media


@router.get("/product/{product_id}/reviews-with-media")
async def get_product_reviews_with_media(
    product_id: int,
    db: AsyncSession = Depends(get_db),
):
    r = await db.execute(
        select(Review).where(Review.product_id == product_id, Review.is_approved == True).order_by(Review.created_at.desc())
    )
    reviews = r.scalars().all()
    result = []
    for review in reviews:
        mr = await db.execute(
            select(ReviewMedia).where(ReviewMedia.review_id == review.id)
        )
        media = mr.scalars().all()
        result.append({
            "id": review.id,
            "rating": review.rating,
            "title": review.title,
            "comment": review.comment,
            "created_at": review.created_at.isoformat() if review.created_at else None,
            "media": [{"id": m.id, "media_type": m.media_type, "url": m.url} for m in media],
        })
    return result
