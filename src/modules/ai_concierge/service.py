from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.ai_concierge.repository import ConciergeRepository
from src.modules.ai_concierge.models import ConciergeConversation, ConciergeMessage


class ConciergeService:
    def __init__(self, db: AsyncSession):
        self.repo = ConciergeRepository(db)

    async def match_intent(self, message: str, hotel_id: int):
        intents = await self.repo.list_intents(hotel_id)
        msg_lower = message.lower()
        for intent in intents:
            if intent.trigger_phrases:
                for phrase in intent.trigger_phrases:
                    if phrase.strip().lower() in msg_lower:
                        return intent
        return None

    async def generate_auto_response(self, message: str, hotel_id: int, conversation_id: int):
        config = await self.repo.get_config(hotel_id)
        if config and not config.auto_respond:
            return None
        intent = await self.match_intent(message, hotel_id)
        response = intent.response_template if intent else None
        await self.repo.add_message(conversation_id, {
            "sender_type": "ai",
            "message": response or "Üzgünüm, bu konuda size nasıl yardımcı olabileceğimi anlamadım.",
            "intent_matched": intent.intent_key if intent else None,
            "is_auto_response": True,
        })
        return response

    async def escalate_to_human(self, conversation_id: int):
        conv = await self.repo.get_conversation(conversation_id)
        if not conv:
            return None
        conv.status = "escalated"
        conv.resolved_at = datetime.now(timezone.utc)
        self.repo.db.add(conv)
        return conv

    async def send_automated_message(self, booking_id: int, sequence_id: int):
        seq = await self.repo.update_sequence(sequence_id, {})
        return seq

    async def trigger_sequence(self, hotel_id: int, booking_id: int, trigger_event: str):
        sequences = await self.repo.list_sequences(hotel_id, trigger_event)
        results = []
        for seq in sequences:
            conv = await self.repo.create_conversation({
                "booking_id": booking_id,
                "hotel_id": hotel_id,
                "channel": seq.channel or "in_app",
                "started_at": datetime.now(timezone.utc),
            })
            await self.repo.db.flush()
            msg = await self.repo.add_message(conv.id, {
                "sender_type": "ai",
                "message": seq.message_template,
                "is_auto_response": True,
            })
            results.append({"sequence_id": seq.id, "conversation_id": conv.id, "message_id": msg.id})
        return results

    async def get_concierge_analytics(self, hotel_id: int):
        convs = await self.repo.list_conversations(hotel_id)
        total = len(convs)
        resolved = sum(1 for c in convs if c.status == "resolved")
        escalated = sum(1 for c in convs if c.status == "escalated")
        resolution_rate = round((resolved / total * 100), 1) if total else 0
        intent_counts = {}
        for conv in convs:
            msgs = await self.repo.get_messages(conv.id)
            for m in msgs:
                if m.intent_matched:
                    intent_counts[m.intent_matched] = intent_counts.get(m.intent_matched, 0) + 1
        common_intents = sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        return {
            "total_conversations": total,
            "resolved": resolved,
            "escalated": escalated,
            "resolution_rate": resolution_rate,
            "active": sum(1 for c in convs if c.status == "active"),
            "common_intents": [{"intent": k, "count": v} for k, v in common_intents],
        }
