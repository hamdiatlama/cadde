from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.payment_vault.models import SavedPaymentMethod


class PaymentVaultRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_card(self, user_id: int, token: str, last_four: str = None, card_holder: str = None, card_brand: str = None, expiry_month: int = None, expiry_year: int = None) -> SavedPaymentMethod:
        existing = await self.list_cards(user_id)
        is_default = len(existing) == 0
        pm = SavedPaymentMethod(
            user_id=user_id, token=token, last_four=last_four,
            card_holder=card_holder, card_brand=card_brand,
            expiry_month=expiry_month, expiry_year=expiry_year,
            is_default=is_default
        )
        self.db.add(pm)
        return pm

    async def list_cards(self, user_id: int):
        r = await self.db.execute(
            select(SavedPaymentMethod).where(
                SavedPaymentMethod.user_id == user_id,
                SavedPaymentMethod.is_active == True
            ).order_by(SavedPaymentMethod.created_at.desc())
        )
        return r.scalars().all()

    async def set_default(self, card_id: int, user_id: int):
        await self.db.execute(
            update(SavedPaymentMethod).where(
                SavedPaymentMethod.user_id == user_id
            ).values(is_default=False)
        )
        r = await self.db.execute(
            select(SavedPaymentMethod).where(
                SavedPaymentMethod.id == card_id,
                SavedPaymentMethod.user_id == user_id,
                SavedPaymentMethod.is_active == True
            )
        )
        pm = r.scalar_one_or_none()
        if pm:
            pm.is_default = True
        return pm

    async def delete_card(self, card_id: int, user_id: int):
        r = await self.db.execute(
            select(SavedPaymentMethod).where(
                SavedPaymentMethod.id == card_id,
                SavedPaymentMethod.user_id == user_id
            )
        )
        pm = r.scalar_one_or_none()
        if pm:
            pm.is_active = False
        return pm

    async def get_default(self, user_id: int):
        r = await self.db.execute(
            select(SavedPaymentMethod).where(
                SavedPaymentMethod.user_id == user_id,
                SavedPaymentMethod.is_default == True,
                SavedPaymentMethod.is_active == True
            )
        )
        return r.scalar_one_or_none()
