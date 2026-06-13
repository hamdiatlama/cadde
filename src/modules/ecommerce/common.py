from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.order import Order, OrderItem
from src.models.product import Product
from src.modules.notification.service import create_notification

async def auto_cancel_expired_approvals(db: AsyncSession):
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Order).where(
            Order.status == "pending_approval",
            Order.approval_deadline.isnot(None),
            Order.approval_deadline <= now,
        )
    )
    for order in result.scalars().all():
        order.status = "cancelled"
        order.cancelled_at = now
        order.cancel_reason = "Onay süresi doldugu icin otomatik iptal edildi"
        if order.payment_status == "paid":
            order.payment_status = "refunded"
        items_r = await db.execute(select(OrderItem).where(OrderItem.order_id == order.id))
        for item in items_r.scalars().all():
            prod_r = await db.execute(select(Product).where(Product.id == item.product_id))
            prod = prod_r.scalar_one_or_none()
            if prod:
                prod.stock += item.quantity
        await create_notification(
            db, order.user_id, "order_cancelled",
            message=f"Siparis #{order.id} onay suresi doldugu icin iptal edildi",
            reference_type="order", reference_id=order.id,
        )
