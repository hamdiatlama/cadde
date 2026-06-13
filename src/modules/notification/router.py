from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.notification.service import NotificationService
from src.modules.notification.schemas import NotificationResponse

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=list[NotificationResponse])
async def list_notifications(
    unread_only: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = NotificationService(db)
    return await svc.list_notifications(current_user.id, unread_only)

@router.post("/{notification_id}/read", response_model=dict)
async def mark_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = NotificationService(db)
    n = await svc.mark_read(notification_id, current_user.id)
    if not n:
        raise HTTPException(status_code=404, detail="Notification not found")
    await db.commit()
    return {"status": "marked_read"}

@router.post("/read-all", response_model=dict)
async def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = NotificationService(db)
    await svc.mark_all_read(current_user.id)
    await db.commit()
    return {"status": "all_marked_read"}
