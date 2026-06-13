from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.payment import Payment, PaymentMethod, PointsTransaction
from src.models.order import Order

class PaymentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_order(self, order_id: int, user_id: int):
        r = await self.db.execute(
            select(Order).where(Order.id == order_id, Order.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def create_payment(self, payment: Payment):
        self.db.add(payment)

    async def add_points_transaction(self, txn: PointsTransaction):
        self.db.add(txn)

    async def get_points_transactions(self, user_id: int, limit: int = 50):
        r = await self.db.execute(
            select(PointsTransaction).where(PointsTransaction.user_id == user_id)
            .order_by(PointsTransaction.created_at.desc()).limit(limit)
        )
        return r.scalars().all()

    async def add_payment_method(self, method: PaymentMethod):
        self.db.add(method)

    async def list_payment_methods(self, user_id: int):
        r = await self.db.execute(
            select(PaymentMethod).where(
                PaymentMethod.user_id == user_id, PaymentMethod.is_active == True
            )
        )
        return r.scalars().all()
