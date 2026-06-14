from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.support import SupportTicket, TicketMessage

class SupportRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_ticket(self, ticket: SupportTicket):
        self.db.add(ticket)

    async def create_message(self, msg: TicketMessage):
        self.db.add(msg)

    async def get_ticket(self, ticket_id: int):
        r = await self.db.execute(select(SupportTicket).where(SupportTicket.id == ticket_id))
        return r.scalar_one_or_none()

    async def list_user_tickets(self, user_id: int):
        r = await self.db.execute(
            select(SupportTicket).where(SupportTicket.user_id == user_id)
            .order_by(SupportTicket.updated_at.desc().nulls_last(), SupportTicket.created_at.desc())
        )
        return r.scalars().all()

    async def count_open_tickets(self, user_id: int) -> int:
        r = await self.db.execute(
            select(func.count(SupportTicket.id))
            .where(SupportTicket.user_id == user_id, SupportTicket.status.in_(["open", "in_progress"]))
        )
        return r.scalar() or 0

    async def get_last_message(self, ticket_id: int):
        r = await self.db.execute(
            select(TicketMessage).where(TicketMessage.ticket_id == ticket_id)
            .order_by(TicketMessage.created_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def get_messages(self, ticket_id: int):
        r = await self.db.execute(
            select(TicketMessage).where(TicketMessage.ticket_id == ticket_id)
            .order_by(TicketMessage.created_at.asc())
        )
        return r.scalars().all()

    async def update_status(self, ticket_id: int, status: str):
        await self.db.execute(
            SupportTicket.__table__.update()
            .where(SupportTicket.id == ticket_id)
            .values(status=status, updated_at=func.now())
        )

    async def update_resolved_at(self, ticket_id: int):
        await self.db.execute(
            SupportTicket.__table__.update()
            .where(SupportTicket.id == ticket_id)
            .values(resolved_at=func.now(), updated_at=func.now())
        )

    async def list_all_tickets(self, limit: int = 50, offset: int = 0):
        r = await self.db.execute(
            select(SupportTicket)
            .order_by(SupportTicket.updated_at.desc().nulls_last(), SupportTicket.created_at.desc())
            .limit(limit).offset(offset)
        )
        return r.scalars().all()
