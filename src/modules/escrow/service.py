from datetime import datetime, timezone, timedelta
from src.modules.escrow.repository import EscrowRepository
from src.modules.campaign.service import CampaignService


class EscrowService:
    def __init__(self, db):
        self.repo = EscrowRepository(db)

    async def hold_payment(self, order_id: int, buyer_id: int, seller_id: int, amount: float,
                            platform_fee_percent: float = 5.0, release_days: int = 3):
        existing = await self.repo.get_by_order(order_id)
        if existing:
            return existing, "Already held"
        platform_fee = round(amount * platform_fee_percent / 100, 2)
        seller_amount = round(amount - platform_fee, 2)
        release_at = datetime.now(timezone.utc) + timedelta(days=release_days)
        e = await self.repo.create_escrow(
            order_id=order_id, buyer_id=buyer_id, seller_id=seller_id,
            amount=amount, platform_fee=platform_fee, seller_amount=seller_amount,
            status="held", release_trigger=f"auto_{release_days}d", release_at=release_at,
        )
        return {"id": e.id, "order_id": e.order_id, "amount": e.amount,
                "platform_fee": e.platform_fee, "seller_amount": e.seller_amount,
                "status": "held", "release_at": e.release_at.isoformat() if e.release_at else None,
                "message": f"Payment held in escrow. Will auto-release after {release_days} days."}, None

    async def release_payment(self, escrow_id: int, released_by: str = "admin"):
        e = await self.repo.get_escrow(escrow_id)
        if not e or e.status != "held":
            return None
        await self.repo.release_escrow(escrow_id, released_by)
        return {"id": e.id, "status": "released", "seller_amount": e.seller_amount,
                "message": f"Payment released. {e.seller_amount} TL transferred to seller."}

    async def release_by_order(self, order_id: int, released_by: str = "system"):
        e = await self.repo.get_by_order(order_id)
        if not e:
            return None
        return await self.release_payment(e.id, released_by)

    async def get_escrow_status(self, order_id: int):
        e = await self.repo.get_by_order(order_id)
        if not e:
            return None
        return {"id": e.id, "order_id": e.order_id, "amount": e.amount,
                "platform_fee": e.platform_fee, "seller_amount": e.seller_amount,
                "status": e.status, "release_at": e.release_at.isoformat() if e.release_at else None,
                "released_at": e.released_at.isoformat() if e.released_at else None}

    async def seller_balance(self, seller_id: int):
        holds = await self.repo.list_seller_holds(seller_id)
        total = sum(h.seller_amount for h in holds)
        return {"seller_id": seller_id, "held_count": len(holds), "total_held": round(total, 2)}

    async def raise_dispute(self, order_id: int, raised_by: int, reason: str, description: str = None,
                             evidence: str = None, raised_against: str = "seller"):
        d = await self.repo.create_dispute(
            order_id=order_id, raised_by=raised_by, raised_against=raised_against,
            reason=reason, description=description, evidence=evidence, status="open",
        )
        return {"id": d.id, "order_id": d.order_id, "reason": d.reason, "status": "open",
                "message": "Dispute raised. Admin will review within 24 hours."}

    async def resolve_dispute(self, dispute_id: int, resolution: str, resolved_by: int,
                               refund_buyer: bool = False):
        d = await self.repo.get_dispute(dispute_id)
        if not d:
            return None
        await self.repo.resolve_dispute(dispute_id, resolution, resolved_by)
        if refund_buyer:
            e = await self.repo.get_by_order(d.order_id)
            if e and e.status == "held":
                await self.repo.refund_escrow(e.id)
        return {"id": d.id, "resolution": resolution, "status": "resolved"}

    async def get_disputes(self, order_id: int = None):
        if order_id:
            disputes = await self.repo.list_order_disputes(order_id)
        else:
            return []
        return [{"id": d.id, "order_id": d.order_id, "reason": d.reason,
                 "status": d.status, "raised_by": d.raised_by,
                 "created_at": d.created_at.isoformat() if d.created_at else None}
                for d in disputes]
