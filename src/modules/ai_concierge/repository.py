from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.ai_concierge.models import (
    ConciergeConfig, ConciergeIntent, ConciergeConversation,
    ConciergeMessage, ConciergeKnowledgeBase, AutomatedMessageSequence,
)


class ConciergeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_config(self, hotel_id: int) -> ConciergeConfig | None:
        r = await self.db.execute(select(ConciergeConfig).where(ConciergeConfig.hotel_id == hotel_id))
        return r.scalar_one_or_none()

    async def update_config(self, hotel_id: int, data: dict) -> ConciergeConfig:
        config = await self.get_config(hotel_id)
        if config:
            for field, val in data.items():
                setattr(config, field, val)
        else:
            config = ConciergeConfig(hotel_id=hotel_id, **data)
            self.db.add(config)
        return config

    async def list_intents(self, hotel_id: int) -> list[ConciergeIntent]:
        r = await self.db.execute(
            select(ConciergeIntent).where(
                ConciergeIntent.hotel_id == hotel_id,
                ConciergeIntent.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def create_intent(self, data: dict) -> ConciergeIntent:
        intent = ConciergeIntent(**data)
        self.db.add(intent)
        return intent

    async def update_intent(self, intent_id: int, data: dict) -> ConciergeIntent | None:
        r = await self.db.execute(select(ConciergeIntent).where(ConciergeIntent.id == intent_id))
        intent = r.scalar_one_or_none()
        if not intent:
            return None
        for field, val in data.items():
            setattr(intent, field, val)
        self.db.add(intent)
        return intent

    async def list_conversations(self, hotel_id: int, status: str = None) -> list[ConciergeConversation]:
        query = select(ConciergeConversation).where(ConciergeConversation.hotel_id == hotel_id)
        if status:
            query = query.where(ConciergeConversation.status == status)
        query = query.order_by(ConciergeConversation.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def get_conversation(self, conversation_id: int) -> ConciergeConversation | None:
        r = await self.db.execute(select(ConciergeConversation).where(ConciergeConversation.id == conversation_id))
        return r.scalar_one_or_none()

    async def create_conversation(self, data: dict) -> ConciergeConversation:
        conv = ConciergeConversation(**data)
        self.db.add(conv)
        return conv

    async def add_message(self, conversation_id: int, data: dict) -> ConciergeMessage:
        msg = ConciergeMessage(conversation_id=conversation_id, **data)
        self.db.add(msg)
        return msg

    async def get_messages(self, conversation_id: int) -> list[ConciergeMessage]:
        r = await self.db.execute(
            select(ConciergeMessage).where(
                ConciergeMessage.conversation_id == conversation_id
            ).order_by(ConciergeMessage.created_at)
        )
        return list(r.scalars().all())

    async def list_kb_entries(self, hotel_id: int, category: str = None) -> list[ConciergeKnowledgeBase]:
        query = select(ConciergeKnowledgeBase).where(
            ConciergeKnowledgeBase.hotel_id == hotel_id,
            ConciergeKnowledgeBase.is_active == True,
        )
        if category:
            query = query.where(ConciergeKnowledgeBase.category == category)
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def create_kb_entry(self, data: dict) -> ConciergeKnowledgeBase:
        entry = ConciergeKnowledgeBase(**data)
        self.db.add(entry)
        return entry

    async def update_kb_entry(self, entry_id: int, data: dict) -> ConciergeKnowledgeBase | None:
        r = await self.db.execute(select(ConciergeKnowledgeBase).where(ConciergeKnowledgeBase.id == entry_id))
        entry = r.scalar_one_or_none()
        if not entry:
            return None
        for field, val in data.items():
            setattr(entry, field, val)
        self.db.add(entry)
        return entry

    async def list_sequences(self, hotel_id: int, trigger_event: str = None) -> list[AutomatedMessageSequence]:
        query = select(AutomatedMessageSequence).where(
            AutomatedMessageSequence.hotel_id == hotel_id,
            AutomatedMessageSequence.is_active == True,
        )
        if trigger_event:
            query = query.where(AutomatedMessageSequence.trigger_event == trigger_event)
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def create_sequence(self, data: dict) -> AutomatedMessageSequence:
        seq = AutomatedMessageSequence(**data)
        self.db.add(seq)
        return seq

    async def update_sequence(self, sequence_id: int, data: dict) -> AutomatedMessageSequence | None:
        r = await self.db.execute(select(AutomatedMessageSequence).where(AutomatedMessageSequence.id == sequence_id))
        seq = r.scalar_one_or_none()
        if not seq:
            return None
        for field, val in data.items():
            setattr(seq, field, val)
        self.db.add(seq)
        return seq
