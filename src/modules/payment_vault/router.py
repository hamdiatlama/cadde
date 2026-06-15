from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.payment_vault.repository import PaymentVaultRepository

router = APIRouter(prefix="/payment-vault", tags=["payment_vault"])


@router.post("/cards", status_code=201)
async def save_card(
    token: str, last_four: str = None, card_holder: str = None,
    card_brand: str = None, expiry_month: int = None, expiry_year: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PaymentVaultRepository(db)
    pm = await repo.save_card(current_user.id, token, last_four, card_holder, card_brand, expiry_month, expiry_year)
    await db.commit()
    return pm


@router.get("/cards")
async def list_cards(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PaymentVaultRepository(db)
    return await repo.list_cards(current_user.id)


@router.put("/cards/{card_id}/default")
async def set_default_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PaymentVaultRepository(db)
    pm = await repo.set_default(card_id, current_user.id)
    if not pm:
        raise HTTPException(404, "Card not found")
    await db.commit()
    return pm


@router.delete("/cards/{card_id}", status_code=204)
async def delete_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PaymentVaultRepository(db)
    pm = await repo.delete_card(card_id, current_user.id)
    if not pm:
        raise HTTPException(404, "Card not found")
    await db.commit()
