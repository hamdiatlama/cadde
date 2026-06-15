from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.multiseller.repository import MultiSellerRepository

router = APIRouter(prefix="/multi-seller", tags=["multiseller"])


@router.get("/{product_id}/offers")
async def list_offers(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = MultiSellerRepository(db)
    offers = await repo.list_offers(product_id)
    return offers


@router.post("/{product_id}/offers", status_code=201)
async def create_offer(
    product_id: int, price: float, stock: int = 0,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if current_user.role != "seller":
        raise HTTPException(403, "Only sellers can create offers")
    repo = MultiSellerRepository(db)
    offer = await repo.create_offer(product_id, current_user.id, price, stock)
    await db.commit()
    return {"id": offer.id, "product_id": offer.product_id, "price": offer.price}


@router.get("/{product_id}/buybox")
async def get_buybox(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = MultiSellerRepository(db)
    offer = await repo.get_winning_offer(product_id)
    if not offer:
        raise HTTPException(404, "No winning offer found")
    return offer


@router.post("/{product_id}/buybox/recalculate")
async def recalculate_buybox(
    product_id: int,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = MultiSellerRepository(db)
    winner = await repo.recalculate_buybox(product_id)
    await db.commit()
    if not winner:
        return {"product_id": product_id, "winner": None}
    return {"product_id": product_id, "winner": {"id": winner.id, "seller_id": winner.seller_id, "price": winner.price}}
