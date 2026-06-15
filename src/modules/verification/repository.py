from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.verification.models import ProductVerification


class VerificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def request_verification(self, product_id: int, verifier_id: int) -> ProductVerification:
        v = ProductVerification(product_id=product_id, verifier_id=verifier_id)
        self.db.add(v)
        return v

    async def update_verification(self, id: int, status: str, notes: str = None):
        v = await self.get_verification(id)
        if not v:
            return None
        v.status = status
        v.verified_at = datetime.now(timezone.utc)
        if notes:
            v.notes = notes
        return v

    async def get_verification(self, id: int):
        r = await self.db.execute(select(ProductVerification).where(ProductVerification.id == id))
        return r.scalar_one_or_none()

    async def get_status(self, product_id: int):
        r = await self.db.execute(
            select(ProductVerification).where(ProductVerification.product_id == product_id).order_by(ProductVerification.created_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()
