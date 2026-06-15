from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.brand.models import Brand


class BrandRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_brand(self, name: str, owner_id: int, trademark_no: str = None, logo_url: str = None) -> Brand:
        b = Brand(name=name, owner_id=owner_id, trademark_no=trademark_no, logo_url=logo_url)
        self.db.add(b)
        return b

    async def get_brand(self, brand_id: int):
        r = await self.db.execute(select(Brand).where(Brand.id == brand_id))
        return r.scalar_one_or_none()

    async def list_brands(self):
        r = await self.db.execute(select(Brand).order_by(Brand.name))
        return r.scalars().all()

    async def update_brand(self, brand_id: int, **kwargs):
        b = await self.get_brand(brand_id)
        if not b:
            return None
        for k, v in kwargs.items():
            setattr(b, k, v)
        return b
