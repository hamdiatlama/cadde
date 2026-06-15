from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.chatbot.models import ChatbotIntent, ChatbotConversation


class ChatbotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_intents(self):
        r = await self.db.execute(select(ChatbotIntent))
        return r.scalars().all()

    async def save_conversation(self, user_id: int, message: str, response: str):
        c = ChatbotConversation(user_id=user_id, message=message, response=response)
        self.db.add(c)
        return c

    async def match_intent(self, message: str):
        intents = await self.get_all_intents()
        msg_lower = message.lower()
        for intent in intents:
            if intent.keywords:
                for kw in intent.keywords.split(","):
                    if kw.strip().lower() in msg_lower:
                        return intent
        return None
