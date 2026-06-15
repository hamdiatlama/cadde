from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order
from src.models.review import Review
from src.modules.cargo.models import CargoReturnRequest, CargoShipment
from src.modules.escrow.models import Dispute


class ProtectionService:
    def __init__(self, db):
        self.db = db

    async def buyer_protection_status(self, user_id: int):
        r = await self.db.execute(
            select(func.count()).where(Order.user_id == user_id, Order.status == "delivered")
        )
        total_orders = r.scalar()
        r = await self.db.execute(
            select(func.count()).where(Order.user_id == user_id, Order.status == "cancelled")
        )
        cancelled = r.scalar()
        r = await self.db.execute(
            select(func.count())
            .select_from(CargoReturnRequest).join(CargoShipment, CargoShipment.id == CargoReturnRequest.shipment_id)
            .where(CargoReturnRequest.user_id == user_id)
        )
        returns = r.scalar()
        r = await self.db.execute(
            select(func.count()).where(Dispute.raised_by == user_id, Dispute.status == "open")
        )
        open_disputes = r.scalar()
        return {
            "total_orders": total_orders, "cancelled_orders": cancelled,
            "return_requests": returns, "open_disputes": open_disputes,
            "protection_level": "standard",
            "coverage": "A-to-Z Buyer Protection covers: late delivery, damaged items, wrong items, defective products",
            "claim_window_days": 30,
            "max_claim_amount": 50000,
        }

    async def file_claim(self, user_id: int, order_id: int, reason: str, description: str, evidence: str = None):
        order = await self.db.execute(select(Order).where(Order.id == order_id, Order.user_id == user_id))
        order = order.scalar_one_or_none()
        if not order:
            return None, "Order not found"
        now = datetime.now(timezone.utc)
        deadline = order.created_at + timedelta(days=30)
        if now > deadline:
            return None, "Claim window has expired (30 days from order date)"
        from src.modules.escrow.models import Dispute
        d = Dispute(
            order_id=order_id, raised_by=user_id, raised_against="seller",
            reason=reason, description=description, evidence=evidence,
            status="open",
        )
        self.db.add(d)
        return {"id": d.id, "order_id": order_id, "reason": reason, "status": "open",
                "message": "Claim filed. We'll review within 48 hours."}, None

    async def my_claims(self, user_id: int):
        r = await self.db.execute(
            select(Dispute).where(Dispute.raised_by == user_id).order_by(Dispute.created_at.desc())
        )
        disputes = r.scalars().all()
        return [
            {"id": d.id, "order_id": d.order_id, "reason": d.reason,
             "status": d.status, "resolution": d.resolution,
             "created_at": d.created_at.isoformat() if d.created_at else None}
            for d in disputes
        ]
