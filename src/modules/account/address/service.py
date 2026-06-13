from src.modules.account.address.repository import AddressRepository
from src.models.address import Address

class AddressService:
    def __init__(self, db):
        self.repo = AddressRepository(db)

    async def list_addresses(self, user_id: int):
        return await self.repo.list_by_user(user_id)

    async def create_address(self, user_id: int, data):
        if data.is_default:
            await self.repo.unset_defaults(user_id)
        addr = Address(user_id=user_id, **data.model_dump())
        await self.repo.create(addr)
        return addr

    async def update_address(self, addr_id: int, user_id: int, data):
        addr = await self.repo.get_by_id(addr_id, user_id)
        if not addr:
            return None
        if data.is_default:
            await self.repo.unset_defaults(user_id)
        for field, val in data.model_dump(exclude_unset=True).items():
            setattr(addr, field, val)
        return addr

    async def delete_address(self, addr_id: int, user_id: int):
        addr = await self.repo.get_by_id(addr_id, user_id)
        if not addr:
            return None
        await self.repo.delete(addr)
        return addr

    async def set_default(self, addr_id: int, user_id: int):
        addr = await self.repo.get_by_id(addr_id, user_id)
        if not addr:
            return None
        await self.repo.unset_defaults(user_id)
        addr.is_default = True
        return addr
