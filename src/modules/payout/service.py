from datetime import datetime, timezone, timedelta
import uuid
from src.modules.payout.repository import PayoutRepository
from src.modules.escrow.repository import EscrowRepository


class PayoutService:
    def __init__(self, db):
        self.repo = PayoutRepository(db)
        self.escrow_repo = EscrowRepository(db)

    async def seller_earnings(self, seller_id: int):
        return await self.repo.get_seller_earnings(seller_id)

    async def process_payout(self, seller_id: int, admin_id: int):
        earnings = await self.repo.get_seller_earnings(seller_id, 365)
        pending = earnings["pending_escrow"]
        if pending < 10:
            return None, "Minimum payout amount is 10 TL"
        batch = await self.repo.create_batch(
            batch_no=f"PO-{uuid.uuid4().hex[:8].upper()}",
            total_amount=pending, total_sellers=1, status="processing",
        )
        p = await self.repo.create_payout(
            seller_id=seller_id, batch_id=batch.id, amount=pending,
            platform_fee=round(pending * 0.05, 2),
            net_amount=round(pending * 0.95, 2),
            status="processing", period_start=datetime.now(timezone.utc) - timedelta(days=30),
            period_end=datetime.now(timezone.utc),
        )
        batch.total_amount = p.net_amount
        return {"id": p.id, "batch_no": batch.batch_no, "amount": p.amount,
                "platform_fee": p.platform_fee, "net_amount": p.net_amount,
                "status": p.status, "message": "Payout is being processed"}, None

    async def mark_paid(self, payout_id: int, payment_ref: str = None):
        await self.repo.mark_paid(payout_id, payment_ref)
        return {"id": payout_id, "status": "paid", "message": "Payout completed"}

    async def my_payouts(self, seller_id: int):
        payouts = await self.repo.list_payouts(seller_id)
        return [
            {"id": p.id, "amount": p.amount, "platform_fee": p.platform_fee,
             "net_amount": p.net_amount, "status": p.status,
             "paid_at": p.paid_at.isoformat() if p.paid_at else None,
             "created_at": p.created_at.isoformat() if p.created_at else None}
            for p in payouts
        ]
