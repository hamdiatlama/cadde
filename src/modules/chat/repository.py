from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.chat.models import ChatMessage, Conversation, ChatStatus


class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_or_create_conversation(self, conv_id: str, buyer_id: int, seller_id: int, product_id: int = None, order_id: int = None) -> Conversation:
        r = await self.db.execute(select(Conversation).where(Conversation.id == conv_id))
        conv = r.scalar_one_or_none()
        if not conv:
            conv = Conversation(id=conv_id, buyer_id=buyer_id, seller_id=seller_id,
                                 product_id=product_id, order_id=order_id)
            self.db.add(conv)
        return conv

    async def list_conversations(self, user_id: int):
        r = await self.db.execute(
            select(Conversation).where(
                or_(Conversation.buyer_id == user_id, Conversation.seller_id == user_id)
            ).order_by(Conversation.last_message_at.desc().nullslast())
        )
        return r.scalars().all()

    async def get_conversation(self, conv_id: str):
        r = await self.db.execute(select(Conversation).where(Conversation.id == conv_id))
        return r.scalar_one_or_none()

    async def send_message(self, conv_id: str, sender_id: int, receiver_id: int, message: str) -> ChatMessage:
        msg = ChatMessage(conversation_id=conv_id, sender_id=sender_id, receiver_id=receiver_id, message=message)
        self.db.add(msg)
        r = await self.db.execute(select(Conversation).where(Conversation.id == conv_id))
        conv = r.scalar_one_or_none()
        if conv:
            conv.last_message_at = func.now()
        return msg

    async def get_messages(self, conv_id: str, limit: int = 100, offset: int = 0):
        r = await self.db.execute(
            select(ChatMessage).where(ChatMessage.conversation_id == conv_id)
            .order_by(ChatMessage.created_at.asc()).offset(offset).limit(limit)
        )
        return r.scalars().all()

    async def mark_as_read(self, conv_id: str, user_id: int):
        from sqlalchemy import update
        await self.db.execute(
            update(ChatMessage).where(
                ChatMessage.conversation_id == conv_id,
                ChatMessage.receiver_id == user_id,
                ChatMessage.is_read == False
            ).values(is_read=True)
        )

    async def get_unread_count(self, user_id: int):
        r = await self.db.execute(
            select(func.count(ChatMessage.id)).where(ChatMessage.receiver_id == user_id, ChatMessage.is_read == False)
        )
        return r.scalar()
