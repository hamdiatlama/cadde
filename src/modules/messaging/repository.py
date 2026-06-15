from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.messaging.models import EmailTemplate, EmailLog, SmsTemplate, SmsLog, PushSubscription, PushNotification


class EmailTemplateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, subject: str, body_html: str, event_type: str = None) -> EmailTemplate:
        t = EmailTemplate(name=name, subject=subject, body_html=body_html, event_type=event_type)
        self.db.add(t)
        return t

    async def list(self):
        r = await self.db.execute(select(EmailTemplate).order_by(EmailTemplate.created_at.desc()))
        return r.scalars().all()

    async def get_by_name(self, name: str):
        r = await self.db.execute(select(EmailTemplate).where(EmailTemplate.name == name))
        return r.scalar_one_or_none()


class EmailLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_sent(self, to_email: str, subject: str, template: str = None, reference_type: str = None, reference_id: int = None, status: str = "sent", error: str = None) -> EmailLog:
        log = EmailLog(to_email=to_email, subject=subject, template=template, reference_type=reference_type, reference_id=reference_id, status=status, error=error)
        self.db.add(log)
        return log

    async def list(self):
        r = await self.db.execute(select(EmailLog).order_by(EmailLog.sent_at.desc()))
        return r.scalars().all()


class SmsTemplateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, name: str, body: str, event_type: str = None) -> SmsTemplate:
        t = SmsTemplate(name=name, body=body, event_type=event_type)
        self.db.add(t)
        return t

    async def list(self):
        r = await self.db.execute(select(SmsTemplate).order_by(SmsTemplate.name))
        return r.scalars().all()

    async def get_by_name(self, name: str):
        r = await self.db.execute(select(SmsTemplate).where(SmsTemplate.name == name))
        return r.scalar_one_or_none()


class SmsLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def log_sent(self, to_phone: str, body: str, reference_type: str = None, reference_id: int = None, status: str = "sent", error: str = None) -> SmsLog:
        log = SmsLog(to_phone=to_phone, body=body, reference_type=reference_type, reference_id=reference_id, status=status, error=error)
        self.db.add(log)
        return log

    async def list(self):
        r = await self.db.execute(select(SmsLog).order_by(SmsLog.sent_at.desc()))
        return r.scalars().all()


class PushSubscriptionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def subscribe(self, user_id: int, platform: str, token: str) -> PushSubscription:
        sub = PushSubscription(user_id=user_id, platform=platform, token=token)
        self.db.add(sub)
        return sub

    async def unsubscribe(self, user_id: int, token: str):
        await self.db.execute(
            delete(PushSubscription).where(
                PushSubscription.user_id == user_id,
                PushSubscription.token == token
            )
        )

    async def get_tokens(self, user_id: int):
        r = await self.db.execute(
            select(PushSubscription.token).where(
                PushSubscription.user_id == user_id,
                PushSubscription.is_active == True
            )
        )
        return r.scalars().all()


class PushNotificationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def send(self, user_id: int, title: str, body: str, data: str = None) -> PushNotification:
        n = PushNotification(user_id=user_id, title=title, body=body, data=data)
        self.db.add(n)
        return n

    async def list_by_user(self, user_id: int):
        r = await self.db.execute(
            select(PushNotification).where(PushNotification.user_id == user_id)
            .order_by(PushNotification.sent_at.desc())
        )
        return r.scalars().all()

    async def mark_read(self, notification_id: int, user_id: int):
        r = await self.db.execute(
            select(PushNotification).where(
                PushNotification.id == notification_id,
                PushNotification.user_id == user_id
            )
        )
        n = r.scalar_one_or_none()
        if n:
            n.is_read = True
        return n
