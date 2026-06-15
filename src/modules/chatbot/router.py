from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.chatbot.repository import ChatbotRepository

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


@router.post("/message")
async def send_message(
    message: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ChatbotRepository(db)
    intent = await repo.match_intent(message)
    response = intent.response if intent else "Üzgünüm, bu konuda size nasıl yardımcı olabileceğimi anlamadım. Lütfen farklı bir şekilde ifade edin."
    user_id = current_user.id if current_user else None
    await repo.save_conversation(user_id, message, response)
    await db.commit()
    return {"response": response}
