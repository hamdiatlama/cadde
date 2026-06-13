from sqlalchemy.ext.asyncio import AsyncSession

from src.core.auth import hash_password, verify_password, create_token
from src.models.seller import Seller
from src.models.courier import Courier
from src.modules.user.repository import UserRepository
from src.modules.user.events import publish_event, UserEvent


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, email: str, password: str, full_name: str, role: str, phone: str | None = None) -> dict:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError("Email already registered")

        user = await self.repo.create(email, hash_password(password), full_name, role, phone)
        await self.repo.db.flush()

        if role == "seller":
            self.repo.db.add(Seller(user_id=user.id, store_name=full_name + "'s Store"))
        elif role == "courier":
            self.repo.db.add(Courier(user_id=user.id))

        token = create_token(user.id, user.role)
        await publish_event(UserEvent.USER_REGISTERED, {"user_id": user.id, "role": role})
        return {"access_token": token, "user": user}

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")
        token = create_token(user.id, user.role)
        await publish_event(UserEvent.USER_LOGIN, {"user_id": user.id})
        return {"access_token": token, "user": user}

    async def update_profile(self, user_id: int, data: dict) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        await self.repo.update(user, data)
        await publish_event(UserEvent.USER_UPDATED, {"user_id": user_id})
        return user

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> dict:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Old password is incorrect")
        user.password_hash = hash_password(new_password)
        self.repo.db.add(user)
        await publish_event(UserEvent.PASSWORD_CHANGED, {"user_id": user_id})
        return {"status": "password_changed"}
