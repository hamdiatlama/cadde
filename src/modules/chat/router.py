from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/conversations")
async def list_conversations(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ChatService(db)
    return await svc.list_conversations(current_user.id)


@router.post("/conversations", status_code=201)
async def start_conversation(seller_id: int, product_id: int = None, order_id: int = None,
                              current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ChatService(db)
    conv = await svc.start_conversation(current_user.id, seller_id, product_id, order_id)
    await db.commit()
    return {"id": conv.id, "status": "created"}


@router.get("/conversations/{conv_id}/messages")
async def get_messages(conv_id: str, limit: int = 100, offset: int = 0,
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ChatService(db)
    conv = await svc.repo.get_conversation(conv_id)
    if not conv or (conv.buyer_id != current_user.id and conv.seller_id != current_user.id):
        raise HTTPException(404, "Conversation not found")
    await svc.mark_as_read(conv_id, current_user.id)
    await db.commit()
    return await svc.get_messages(conv_id, limit, offset)


@router.post("/conversations/{conv_id}/messages", status_code=201)
async def send_message(conv_id: str, message: str,
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ChatService(db)
    conv = await svc.repo.get_conversation(conv_id)
    if not conv or (conv.buyer_id != current_user.id and conv.seller_id != current_user.id):
        raise HTTPException(404, "Conversation not found")
    receiver_id = conv.seller_id if current_user.id == conv.buyer_id else conv.buyer_id
    result = await svc.send_message(conv_id, current_user.id, receiver_id, message)
    await db.commit()
    return result


@router.get("/unread")
async def unread_count(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = ChatService(db)
    count = await svc.repo.get_unread_count(current_user.id)
    return {"unread_count": count}
