from src.modules.chat.repository import ChatRepository
import uuid


class ChatService:
    def __init__(self, db):
        self.repo = ChatRepository(db)

    def _conv_id(self, buyer_id: int, seller_id: int, product_id: int = None):
        parts = sorted([buyer_id, seller_id])
        if product_id:
            return f"p{product_id}_u{parts[0]}_u{parts[1]}"
        return f"u{parts[0]}_u{parts[1]}"

    async def start_conversation(self, buyer_id: int, seller_id: int, product_id: int = None, order_id: int = None):
        cid = self._conv_id(buyer_id, seller_id, product_id)
        conv = await self.repo.get_or_create_conversation(cid, buyer_id, seller_id, product_id, order_id)
        return conv

    async def list_conversations(self, user_id: int):
        convs = await self.repo.list_conversations(user_id)
        result = []
        for c in convs:
            result.append({
                "id": c.id, "buyer_id": c.buyer_id, "seller_id": c.seller_id,
                "product_id": c.product_id, "order_id": c.order_id, "status": c.status.value,
                "last_message_at": c.last_message_at.isoformat() if c.last_message_at else None
            })
        return result

    async def send_message(self, conv_id: str, sender_id: int, receiver_id: int, message: str):
        msg = await self.repo.send_message(conv_id, sender_id, receiver_id, message)
        return {"id": msg.id, "conversation_id": msg.conversation_id, "sender_id": msg.sender_id,
                "message": msg.message, "created_at": msg.created_at.isoformat() if msg.created_at else None}

    async def get_messages(self, conv_id: str, limit: int = 100, offset: int = 0):
        msgs = await self.repo.get_messages(conv_id, limit, offset)
        return [{"id": m.id, "sender_id": m.sender_id, "receiver_id": m.receiver_id, "message": m.message,
                  "is_read": m.is_read, "created_at": m.created_at.isoformat() if m.created_at else None} for m in msgs]

    async def mark_as_read(self, conv_id: str, user_id: int):
        await self.repo.mark_as_read(conv_id, user_id)
