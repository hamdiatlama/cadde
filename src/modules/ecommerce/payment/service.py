from src.modules.ecommerce.common import auto_cancel_expired_approvals
from src.modules.ecommerce.payment.repository import PaymentRepository
from src.models.payment import Payment, PaymentMethod, PointsTransaction
from src.modules.ecommerce.payment.schemas import PaymentResponse, PointsResponse

class PaymentService:
    def __init__(self, db):
        self.repo = PaymentRepository(db)

    async def process_payment(self, user_id: int, data):
        await auto_cancel_expired_approvals(self.repo.db)
        order = await self.repo.get_order(data.order_id, user_id)
        if not order:
            return None, "Order not found"
        if order.payment_status == "paid":
            return None, "Order already paid"
        if order.status != "approved":
            return None, f"Order must be approved by seller first. Current status: {order.status}"

        amount_due = order.total
        points_used = 0

        if data.method == "points" or (data.method == "mixed" and data.points_to_use > 0):
            points_to_use = min(data.points_to_use, user_id.points if hasattr(user_id, 'points') else 0, int(amount_due))
            # We need the user object
            return None, "Not implemented directly"

        payment = Payment(
            order_id=order.id, user_id=user_id, method=data.method,
            amount=order.total, points_used=points_used,
            installment=data.installment, status="completed",
        )
        await self.repo.create_payment(payment)
        return PaymentResponse.model_validate(payment), None

    async def get_installment_options(self, amount: float):
        banks = {
            "Ziraat": [1, 2, 3, 4, 5, 6],
            "İş Bankası": [1, 2, 3],
            "Garanti": [1, 2, 3, 4, 5, 6, 9, 12],
            "Yapı Kredi": [1, 2, 3, 4, 5, 6],
            "Akbank": [1, 2, 3, 4],
        }
        from src.modules.ecommerce.payment.schemas import InstallmentOption
        options = []
        for bank, installments in banks.items():
            for count in installments:
                interest = 0
                if count > 1:
                    interest = 0.015 * (count - 1)
                total = amount * (1 + interest)
                monthly = total / count
                options.append(InstallmentOption(
                    bank=bank, count=count, monthly=round(monthly, 2), total=round(total, 2),
                ))
        return options

    async def get_my_points(self, user_id: int, user_obj):
        txns = await self.repo.get_points_transactions(user_id)
        transactions = [
            {"id": t.id, "amount": t.amount, "type": t.type,
             "description": t.description,
             "created_at": t.created_at.isoformat() if t.created_at else None}
            for t in txns
        ]
        return PointsResponse(balance=user_obj.points, transactions=transactions)

    async def add_payment_method(self, user_id: int, type: str, provider: str = None):
        method = PaymentMethod(user_id=user_id, type=type, provider=provider)
        await self.repo.add_payment_method(method)
        return {"message": "Payment method added", "id": method.id}

    async def list_payment_methods(self, user_id: int):
        methods = await self.repo.list_payment_methods(user_id)
        return [{"id": m.id, "type": m.type, "provider": m.provider, "is_default": m.is_default} for m in methods]
