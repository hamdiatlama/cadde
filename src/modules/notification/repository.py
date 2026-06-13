from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.notification import Notification

class NotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_by_user(self, user_id: int, unread_only: bool = False):
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read == False)
        query = query.order_by(Notification.created_at.desc())
        r = await self.db.execute(query)
        return r.scalars().all()

    async def get_by_id(self, notification_id: int, user_id: int):
        r = await self.db.execute(
            select(Notification).where(Notification.id == notification_id, Notification.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def mark_read(self, notification: Notification):
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        self.db.add(notification)

    async def get_unread_by_user(self, user_id: int):
        r = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
        )
        return r.scalars().all()
