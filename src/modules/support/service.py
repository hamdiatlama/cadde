from datetime import datetime, timezone
from src.modules.support.repository import SupportRepository
from src.models.support import SupportTicket, TicketMessage

MAX_OPEN_TICKETS = 2

class SupportService:
    def __init__(self, db):
        self.repo = SupportRepository(db)

    async def create_ticket(self, user_id: int, subject: str, message: str,
                            category: str = "other", order_id: int = None):
        open_count = await self.repo.count_open_tickets(user_id)
        if open_count >= MAX_OPEN_TICKETS:
            raise ValueError(f"En fazla {MAX_OPEN_TICKETS} acik destek talebiniz olabilir")
        ticket = SupportTicket(
            user_id=user_id, order_id=order_id, subject=subject, category=category,
        )
        await self.repo.create_ticket(ticket)
        await self.repo.db.flush()
        msg = TicketMessage(ticket_id=ticket.id, sender_id=user_id, message=message)
        await self.repo.create_message(msg)
        return {
            "id": ticket.id, "status": ticket.status, "subject": ticket.subject,
            "category": ticket.category,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
        }

    async def list_my_tickets(self, user_id: int):
        tickets = await self.repo.list_user_tickets(user_id)
        result = []
        for t in tickets:
            last_msg = await self.repo.get_last_message(t.id)
            result.append({
                "id": t.id, "subject": t.subject, "category": t.category,
                "status": t.status, "priority": t.priority, "order_id": t.order_id,
                "last_message": last_msg.message[:100] if last_msg else None,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            })
        return result

    async def get_ticket(self, ticket_id: int, user_id: int, role: str):
        ticket = await self.repo.get_ticket(ticket_id)
        if not ticket:
            return None
        if ticket.user_id != user_id and role != "admin":
            return None
        messages = await self.repo.get_messages(ticket_id)
        return {
            "id": ticket.id, "subject": ticket.subject, "category": ticket.category,
            "status": ticket.status, "priority": ticket.priority,
            "order_id": ticket.order_id,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "messages": [
                {"id": m.id, "sender_id": m.sender_id, "message": m.message,
                 "is_staff": m.is_staff,
                 "created_at": m.created_at.isoformat() if m.created_at else None}
                for m in messages
            ],
        }

    async def add_message(self, ticket_id: int, user_id: int, role: str, message: str):
        ticket = await self.repo.get_ticket(ticket_id)
        if not ticket:
            return None
        if ticket.user_id != user_id and role != "admin":
            return None
        msg = TicketMessage(
            ticket_id=ticket.id, sender_id=user_id, message=message,
            is_staff=(role == "admin"),
        )
        await self.repo.create_message(msg)
        if ticket.status == "open":
            ticket.status = "in_progress"
        return {
            "id": msg.id, "message": msg.message,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }

    async def list_all_tickets(self, role: str, limit: int = 50, offset: int = 0):
        if role != "admin":
            return None
        tickets = await self.repo.list_all_tickets(limit, offset)
        result = []
        for t in tickets:
            last_msg = await self.repo.get_last_message(t.id)
            result.append({
                "id": t.id, "user_id": t.user_id, "subject": t.subject,
                "category": t.category, "status": t.status, "priority": t.priority,
                "order_id": t.order_id,
                "last_message": last_msg.message[:100] if last_msg else None,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            })
        return result

    async def update_status(self, ticket_id: int, status: str, role: str):
        if role != "admin":
            return None
        ticket = await self.repo.get_ticket(ticket_id)
        if not ticket:
            return None
        await self.repo.update_status(ticket_id, status)
        if status == "resolved":
            await self.repo.update_resolved_at(ticket_id)
        return {"id": ticket.id, "status": status}
