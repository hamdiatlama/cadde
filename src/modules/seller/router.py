from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.seller.schemas import (
    SellerUpdate, SellerResponse,
    QuestionCreate, AnswerCreate, QuestionResponse,
)
from src.modules.seller.service import SellerProfileService, QuestionService

router = APIRouter(prefix="/seller-communication", tags=["seller-communication"])


# ─── Seller Profile ──────────────────────────────────

@router.get("/profile", response_model=SellerResponse)
async def get_my_seller_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = SellerProfileService(db)
    try:
        seller = await svc.get_profile(current_user.id)
        return SellerResponse.model_validate(seller)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/profile", response_model=dict)
async def update_seller_profile(
    data: SellerUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = SellerProfileService(db)
    try:
        result = await svc.update(current_user.id, data.model_dump(exclude_unset=True))
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/profile/{seller_id}", response_model=SellerResponse)
async def get_seller_profile(seller_id: int, db: AsyncSession = Depends(get_db)):
    svc = SellerProfileService(db)
    try:
        seller = await svc.get_by_id(seller_id)
        return SellerResponse.model_validate(seller)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── Questions ───────────────────────────────────────

@router.post("/questions", response_model=dict, status_code=status.HTTP_201_CREATED)
async def ask_question(
    data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = QuestionService(db)
    try:
        result = await svc.ask_question(data.product_id, current_user.id, data.question)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/questions/{question_id}/answer", response_model=dict)
async def answer_question(
    question_id: int,
    data: AnswerCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers can answer questions")
    svc = QuestionService(db)
    try:
        result = await svc.answer_question(question_id, current_user.id, data.answer)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/questions/product/{product_id}", response_model=list[QuestionResponse])
async def get_product_questions(product_id: int, db: AsyncSession = Depends(get_db)):
    svc = QuestionService(db)
    return await svc.get_product_questions(product_id)


@router.get("/questions/seller", response_model=list[dict])
async def get_seller_questions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(status_code=403, detail="Only sellers")
    svc = QuestionService(db)
    try:
        return await svc.get_seller_questions(current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/questions/mine", response_model=list[QuestionResponse])
async def get_my_questions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = QuestionService(db)
    return await svc.get_my_questions(current_user.id)
