from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.gift_card.repository import GiftCardRepository

router = APIRouter(prefix="/gift-cards", tags=["gift_cards"])


@router.post("/", status_code=201)
async def create_gift_card(
    balance: float, currency: str = "TRY", recipient_email: str = None, expires_at: datetime = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = GiftCardRepository(db)
    card = await repo.create_card(current_user.id, balance, currency, recipient_email, expires_at)
    await db.commit()
    return {"id": card.id, "code": card.code, "balance": card.balance, "currency": card.currency}


@router.get("/my")
async def my_gift_cards(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = GiftCardRepository(db)
    cards = await repo.list_user_cards(current_user.id)
    return cards


@router.post("/redeem")
async def redeem_gift_card(
    code: str, amount: float,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = GiftCardRepository(db)
    try:
        card = await repo.redeem(code, amount)
    except ValueError as e:
        raise HTTPException(400, str(e))
    await db.commit()
    return {"code": card.code, "remaining_balance": card.balance}


@router.get("/balance/{code}")
async def get_balance(code: str, db: AsyncSession = Depends(get_db)):
    repo = GiftCardRepository(db)
    card = await repo.get_by_code(code)
    if not card:
        raise HTTPException(404, "Gift card not found")
    return {"code": card.code, "balance": card.balance, "currency": card.currency, "is_active": card.is_active}
