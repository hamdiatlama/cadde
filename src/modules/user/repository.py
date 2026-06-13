from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_email(self, email: str) -> User | None:
        r = await self.db.execute(select(User).where(User.email == email))
        return r.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        r = await self.db.execute(select(User).where(User.id == user_id))
        return r.scalar_one_or_none()

    async def create(self, email: str, password_hash: str, full_name: str, role: str, phone: str | None = None) -> User:
        user = User(
            email=email, phone=phone,
            password_hash=password_hash, full_name=full_name, role=role,
        )
        self.db.add(user)
        return user

    async def update(self, user: User, data: dict) -> User:
        for field, val in data.items():
            setattr(user, field, val)
        self.db.add(user)
        return user
