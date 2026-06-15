from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.address import Address

class AddressRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: int):
        r = await self.db.execute(
            select(Address).where(Address.user_id == user_id)
            .order_by(Address.is_default.desc(), Address.created_at.desc())
        )
        return r.scalars().all()

    async def get_by_id(self, addr_id: int, user_id: int):
        r = await self.db.execute(
            select(Address).where(Address.id == addr_id, Address.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def create(self, address: Address):
        self.db.add(address)

    async def delete(self, address: Address):
        await self.db.delete(address)

    async def unset_defaults(self, user_id: int):
        r = await self.db.execute(
            select(Address).where(Address.user_id == user_id, Address.is_default == True)
        )
        for a in r.scalars().all():
            a.is_default = False

    async def set_default(self, user_id: int, address_id: int) -> Address | None:
        r = await self.db.execute(
            select(Address).where(Address.user_id == user_id, Address.id == address_id)
        )
        addr = r.scalar_one_or_none()
        if not addr:
            return None
        await self.unset_defaults(user_id)
        addr.is_default = True
        return addr

    async def get_default(self, user_id: int) -> Address | None:
        r = await self.db.execute(
            select(Address).where(Address.user_id == user_id, Address.is_default == True)
        )
        return r.scalar_one_or_none()

    async def list_addresses(self, user_id: int):
        return await self.list_by_user(user_id)
