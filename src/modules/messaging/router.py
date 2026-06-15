from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.messaging.repository import (
    EmailTemplateRepository, EmailLogRepository,
    SmsTemplateRepository, SmsLogRepository,
    PushSubscriptionRepository, PushNotificationRepository,
)

router = APIRouter(prefix="/messaging", tags=["messaging"])


@router.post("/email/templates", status_code=201)
async def create_email_template(
    name: str, subject: str, body_html: str, event_type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailTemplateRepository(db)
    t = await repo.create(name, subject, body_html, event_type)
    await db.commit()
    return t


@router.get("/email/templates")
async def list_email_templates(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailTemplateRepository(db)
    return await repo.list()


@router.post("/email/send", status_code=201)
async def send_transactional_email(
    to_email: str, subject: str, body: str,
    reference_type: str = None, reference_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailLogRepository(db)
    log = await repo.log_sent(to_email, subject, reference_type=reference_type, reference_id=reference_id)
    await db.commit()
    return log


@router.get("/email/logs")
async def list_email_logs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailLogRepository(db)
    return await repo.list()


@router.post("/sms/templates", status_code=201)
async def create_sms_template(
    name: str, body: str, event_type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SmsTemplateRepository(db)
    t = await repo.create(name, body, event_type)
    await db.commit()
    return t


@router.get("/sms/templates")
async def list_sms_templates(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SmsTemplateRepository(db)
    return await repo.list()


@router.post("/sms/send", status_code=201)
async def send_sms(
    to_phone: str, body: str,
    reference_type: str = None, reference_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SmsLogRepository(db)
    log = await repo.log_sent(to_phone, body, reference_type=reference_type, reference_id=reference_id)
    await db.commit()
    return log


@router.post("/push/subscribe", status_code=201)
async def subscribe_push(
    platform: str, token: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PushSubscriptionRepository(db)
    sub = await repo.subscribe(current_user.id, platform, token)
    await db.commit()
    return sub


@router.delete("/push/unsubscribe", status_code=204)
async def unsubscribe_push(
    token: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PushSubscriptionRepository(db)
    await repo.unsubscribe(current_user.id, token)
    await db.commit()


@router.post("/push/send", status_code=201)
async def send_push_notification(
    user_id: int, title: str, body: str, data: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PushNotificationRepository(db)
    n = await repo.send(user_id, title, body, data)
    await db.commit()
    return n


@router.get("/push/my")
async def my_push_notifications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PushNotificationRepository(db)
    return await repo.list_by_user(current_user.id)


@router.put("/push/{notification_id}/read")
async def mark_push_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = PushNotificationRepository(db)
    n = await repo.mark_read(notification_id, current_user.id)
    if not n:
        raise HTTPException(404, "Notification not found")
    await db.commit()
    return n
