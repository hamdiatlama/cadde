import secrets
import string
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.gift_card.models import GiftCard, GiftCardTransaction


class GiftCardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _generate_code(self) -> str:
        alphabet = string.ascii_uppercase + string.digits
        return "GC-" + "".join(secrets.choice(alphabet) for _ in range(12))

    async def create_card(
        self, buyer_id: int, balance: float, currency: str = "TRY",
        recipient_email: str = None, expires_at: datetime = None
    ) -> GiftCard:
        code = await self._generate_code()
        card = GiftCard(
            code=code, balance=balance, currency=currency,
            buyer_id=buyer_id, recipient_email=recipient_email,
            expires_at=expires_at
        )
        self.db.add(card)
        return card

    async def get_by_code(self, code: str):
        r = await self.db.execute(select(GiftCard).where(GiftCard.code == code))
        return r.scalar_one_or_none()

    async def redeem(self, code: str, amount: float) -> GiftCard:
        r = await self.db.execute(select(GiftCard).where(GiftCard.code == code))
        card = r.scalar_one_or_none()
        if not card:
            raise ValueError("Gift card not found")
        if not card.is_active:
            raise ValueError("Gift card is not active")
        if card.expires_at and card.expires_at < datetime.now(card.expires_at.tzinfo):
            raise ValueError("Gift card has expired")
        if card.balance < amount:
            raise ValueError("Insufficient balance")
        card.balance -= amount
        if card.balance == 0:
            card.is_active = False
        return card

    async def list_user_cards(self, user_id: int):
        r = await self.db.execute(
            select(GiftCard).where(GiftCard.buyer_id == user_id).order_by(GiftCard.created_at.desc())
        )
        return r.scalars().all()
