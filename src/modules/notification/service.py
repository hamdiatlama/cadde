from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.notification.repository import NotificationRepository
from src.models.notification import Notification

NOTIFICATION_TYPES = {
    "order_approved": "Siparisiniz Onaylandi",
    "order_rejected": "Siparisiniz Reddedildi",
    "order_delivered": "Siparisiniz Teslim Edildi",
    "new_order": "Yeni Siparis Var",
    "order_cancelled": "Siparis Iptal Edildi",
    "payment_received": "Odeme Alindi",
    "question_answered": "Sorunuz Cevaplandi",
    "ticket_updated": "Destek Talebi Guncellendi",
    "subscription_reminder": "Abonelik Hatirlatmasi",
    "coupon_received": "Yeni Kuponunuz Var",
    "ride_accepted": "Yolculuk Kabul Edildi",
    "ride_completed": "Yolculuk Tamamlandi",
    "ride_cancelled": "Yolculuk Iptal Edildi",
}


async def create_notification(
    db: AsyncSession,
    user_id: int,
    notification_type: str,
    message: str | None = None,
    reference_type: str | None = None,
    reference_id: int | None = None,
) -> Notification:
    title = NOTIFICATION_TYPES.get(notification_type, notification_type.replace("_", " ").title())
    n = Notification(
        user_id=user_id,
        type=notification_type,
        title=title,
        message=message,
        reference_type=reference_type,
        reference_id=reference_id,
    )
    db.add(n)
    return n


class NotificationService:
    def __init__(self, db):
        self.repo = NotificationRepository(db)

    async def list_notifications(self, user_id: int, unread_only: bool = False):
        return await self.repo.list_by_user(user_id, unread_only)

    async def mark_read(self, notification_id: int, user_id: int):
        n = await self.repo.get_by_id(notification_id, user_id)
        if not n:
            return None
        await self.repo.mark_read(n)
        return n

    async def mark_all_read(self, user_id: int):
        notifications = await self.repo.get_unread_by_user(user_id)
        now = datetime.now(timezone.utc)
        for n in notifications:
            n.is_read = True
            n.read_at = now
        return True
