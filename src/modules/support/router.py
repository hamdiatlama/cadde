from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.support.service import SupportService

router = APIRouter(prefix="/support", tags=["support"])

@router.post("/tickets", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_ticket(
    subject: str, message: str, category: str = "other", order_id: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    try:
        result = await svc.create_ticket(current_user.id, subject, message, category, order_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return result

@router.get("/tickets", response_model=list[dict])
async def list_my_tickets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    return await svc.list_my_tickets(current_user.id)

@router.get("/tickets/{ticket_id}", response_model=dict)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    result = await svc.get_ticket(ticket_id, current_user.id, current_user.role)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result

@router.post("/tickets/{ticket_id}/messages", response_model=dict)
async def add_message(
    ticket_id: int, message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    result = await svc.add_message(ticket_id, current_user.id, current_user.role, message)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    await db.commit()
    return result

@router.get("/admin/tickets", response_model=list[dict])
async def list_all_tickets(
    limit: int = 50, offset: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    result = await svc.list_all_tickets(current_user.role, limit, offset)
    if result is None:
        raise HTTPException(status_code=403, detail="Admin only")
    return result

@router.put("/tickets/{ticket_id}/status", response_model=dict)
async def update_ticket_status(
    ticket_id: int, status: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = SupportService(db)
    result = await svc.update_status(ticket_id, status, current_user.role)
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found or access denied")
    await db.commit()
    return result
