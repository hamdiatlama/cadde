from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.multiseller.models import SellerOffer


class MultiSellerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_offers(self, product_id: int):
        r = await self.db.execute(
            select(SellerOffer).where(
                SellerOffer.product_id == product_id,
                SellerOffer.is_active == True
            ).order_by(SellerOffer.price.asc())
        )
        return r.scalars().all()

    async def create_offer(self, product_id: int, seller_id: int, price: float, stock: int = 0) -> SellerOffer:
        offer = SellerOffer(product_id=product_id, seller_id=seller_id, price=price, stock=stock)
        self.db.add(offer)
        return offer

    async def update_stock(self, offer_id: int, delta: int):
        r = await self.db.execute(
            select(SellerOffer).where(SellerOffer.id == offer_id)
        )
        offer = r.scalar_one_or_none()
        if not offer:
            return None
        offer.stock = max(0, offer.stock + delta)
        return offer

    async def get_winning_offer(self, product_id: int):
        r = await self.db.execute(
            select(SellerOffer).where(
                SellerOffer.product_id == product_id,
                SellerOffer.is_active == True,
                SellerOffer.stock > 0
            ).order_by(SellerOffer.price.asc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def recalculate_buybox(self, product_id: int):
        await self.db.execute(
            update(SellerOffer).where(
                SellerOffer.product_id == product_id
            ).values(is_winning=False)
        )
        winner = await self.get_winning_offer(product_id)
        if winner:
            winner.is_winning = True
        return winner
