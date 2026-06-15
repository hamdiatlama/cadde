from datetime import datetime, timezone, timedelta
from src.modules.ecommerce.order.repository import OrderRepository
from src.modules.ecommerce.common import auto_cancel_expired_approvals
from src.models.order import Order, OrderItem
from src.models.substitution import Substitution
from src.models.payment import PointsTransaction
from src.modules.ecommerce.order.schemas import OrderResponse
from src.modules.notification.service import create_notification
from src.core.events import event_bus

class OrderService:
    def __init__(self, db):
        self.repo = OrderRepository(db)

    async def create_order(self, user_id: int, data):
        await auto_cancel_expired_approvals(self.repo.db)
        subtotal = 0.0
        order_items = []

        for item in data.items:
            product = await self.repo.get_product(item.product_id)
            if not product:
                return None, f"Product {item.product_id} not found"
            if product.stock < item.quantity:
                return None, f"Insufficient stock for {product.name}"
            subtotal += product.price * item.quantity
            order_items.append({"product": product, "quantity": item.quantity})

        delivery_fee = 0 if subtotal > 200 else 29.90
        total = subtotal + delivery_fee
        now = datetime.now(timezone.utc)

        is_food = any("food" in oi["product"].category.lower() if oi["product"].category else False for oi in order_items)
        approval_deadline = None
        if is_food:
            approval_deadline = now + timedelta(minutes=15)
        elif data.scheduled_date and data.scheduled_date > now:
            delta = data.scheduled_date - now
            if delta <= timedelta(hours=1): approval_deadline = now + timedelta(minutes=15)
            elif delta <= timedelta(hours=6): approval_deadline = now + timedelta(hours=1)
            elif delta <= timedelta(hours=12): approval_deadline = now + timedelta(hours=2)
            elif delta <= timedelta(hours=24): approval_deadline = now + timedelta(hours=3)
            elif delta <= timedelta(weeks=1): approval_deadline = now + timedelta(days=1)
            elif delta <= timedelta(weeks=4): approval_deadline = now + timedelta(weeks=1)
            elif delta <= timedelta(days=365): approval_deadline = now + timedelta(days=30)
            else: approval_deadline = now + timedelta(days=30)
        elif data.scheduled_date is None:
            approval_deadline = now + timedelta(minutes=15)

        order = Order(
            user_id=user_id, seller_id=data.seller_id, status="pending_approval",
            subtotal=subtotal, delivery_fee=delivery_fee, total=total,
            payment_method=data.payment_method, delivery_address=data.delivery_address,
            delivery_latitude=data.delivery_latitude, delivery_longitude=data.delivery_longitude,
            recipient_name=data.recipient_name, recipient_phone=data.recipient_phone,
            notes=data.notes, scheduled_date=data.scheduled_date,
            approval_deadline=approval_deadline,
        )
        await self.repo.create_order(order)
        await self.repo.db.flush()

        for oi in order_items:
            oi_item = OrderItem(
                order_id=order.id, product_id=oi["product"].id,
                quantity=oi["quantity"], unit_price=oi["product"].price,
            )
            await self.repo.create_order_item(oi_item)
            oi["product"].stock -= oi["quantity"]

        seller = await self.repo.get_seller(data.seller_id)
        if seller:
            seller_user = await self.repo.get_user(seller.user_id)
            if seller_user:
                await create_notification(self.repo.db, seller_user.id, "new_order",
                    message=f"Yeni siparis #{order.id} - {subtotal:.2f} TL",
                    reference_type="order", reference_id=order.id)
        await event_bus.publish("order.created", {"order_id": order.id, "user_id": user_id, "total": total})

        return order, None

    async def list_orders(self, user_id: int, status_filter: str = None):
        await auto_cancel_expired_approvals(self.repo.db)
        orders = await self.repo.list_user_orders(user_id, status_filter)
        return [OrderResponse.model_validate(o) for o in orders]

    async def get_order(self, order_id: int, user_id: int):
        await auto_cancel_expired_approvals(self.repo.db)
        order = await self.repo.get_order(order_id, user_id)
        if not order:
            return None
        return OrderResponse.model_validate(order)

    async def seller_orders(self, user_id: int):
        await auto_cancel_expired_approvals(self.repo.db)
        seller = await self.repo.get_seller_by_user(user_id)
        if not seller:
            return []
        return [OrderResponse.model_validate(o) for o in await self.repo.list_seller_orders(seller.id)]

    async def pending_approval_orders(self, user_id: int):
        await auto_cancel_expired_approvals(self.repo.db)
        seller = await self.repo.get_seller_by_user(user_id)
        if not seller:
            return []
        items = await self.repo.db.execute(
            __import__("sqlalchemy").select(Order)
            .where(Order.seller_id == seller.id, Order.status == "pending_approval")
            .order_by(Order.created_at.asc())
        )
        return [OrderResponse.model_validate(o) for o in items.scalars().all()]

    async def approve_order(self, order_id: int, user_id: int, role: str):
        if role not in ("seller", "admin"):
            return None, "Only sellers can approve orders"
        await auto_cancel_expired_approvals(self.repo.db)
        seller = await self.repo.get_seller_by_user(user_id)
        if not seller:
            return None, "Seller profile not found"
        order = await self.repo.get_order_by_id(order_id)
        if not order or order.seller_id != seller.id:
            return None, "Order not found"
        if order.status != "pending_approval":
            return None, f"Cannot approve order in '{order.status}' status"

        # Satıcı askıda mı kontrol et
        from src.modules.cargo.service import CargoService
        cargo_svc = CargoService(self.repo.db)
        suspension = await cargo_svc.check_seller_suspension(seller.id)
        if suspension and suspension.get("is_suspended"):
            return None, f"Satışlarınız askıya alınmıştır: {suspension['message']}"

        order.status = "approved"
        order.approved_at = datetime.now(timezone.utc)

        # Kargo gönderisi oluştur
        try:
            agreements = await cargo_svc.list_seller_agreements(seller.id)
            if agreements:
                pref = next((a for a in agreements if a.get("is_preferred")), agreements[0])
                comp = await cargo_svc.get_company(pref["company_id"])
                if comp:
                    shipment_data = type("ShipmentData", (), {"model_dump": lambda self: {
                        "company_id": comp.id,
                        "sender_name": seller.company_name or seller.user_id,
                        "sender_city": comp.city,
                        "recipient_name": order.customer_name or f"User#{order.user_id}",
                        "recipient_city": order.shipping_city or order.city or "",
                        "recipient_address": order.shipping_address or order.address or "",
                        "total_price": order.shipping_fee or order.cargo_fee or 0,
                        "source_module": "ecommerce",
                        "source_order_id": order.id,
                        "piece_count": order.quantity or 1,
                    }})()
                    ship = await cargo_svc.create_shipment(shipment_data)
                    if ship:
                        order.tracking_no = ship.tracking_no
                        await self.repo.db.flush()
        except Exception:
            pass

        await create_notification(self.repo.db, order.user_id, "order_approved",
            message=f"Siparis #{order.id} onaylandi - {order.total:.2f} TL",
            reference_type="order", reference_id=order.id)
        return order, None

    async def reject_order(self, order_id: int, user_id: int, role: str, reason: str):
        if role not in ("seller", "admin"):
            return None, "Only sellers can reject orders"
        await auto_cancel_expired_approvals(self.repo.db)
        seller = await self.repo.get_seller_by_user(user_id)
        if not seller:
            return None, "Seller profile not found"
        order = await self.repo.get_order_by_id(order_id)
        if not order or order.seller_id != seller.id:
            return None, "Order not found"
        if order.status != "pending_approval":
            return None, f"Cannot reject order in '{order.status}' status"
        order.status = "rejected"
        order.rejected_at = datetime.now(timezone.utc)
        order.reject_reason = reason
        items = await self.repo.get_order_items(order.id)
        for item in items:
            prod = await self.repo.get_product(item.product_id)
            if prod:
                prod.stock += item.quantity
        await create_notification(self.repo.db, order.user_id, "order_rejected",
            message=f"Siparis #{order.id} reddedildi. Sebep: {reason}",
            reference_type="order", reference_id=order.id)
        return order, None

    async def cancel_order(self, order_id: int, user_id: int, reason: str):
        await auto_cancel_expired_approvals(self.repo.db)
        order = await self.repo.get_order(order_id, user_id)
        if not order:
            return None, "Order not found"
        if order.status not in ("pending_approval", "approved"):
            return None, f"Order cannot be cancelled in '{order.status}' status"
        order.status = "cancelled"
        order.cancelled_at = datetime.now(timezone.utc)
        order.cancel_reason = reason
        items = await self.repo.get_order_items(order.id)
        for item in items:
            prod = await self.repo.get_product(item.product_id)
            if prod:
                prod.stock += item.quantity
        await create_notification(self.repo.db, user_id, "order_cancelled",
            message=f"Siparis #{order.id} iptal edildi. Sebep: {reason}",
            reference_type="order", reference_id=order.id)
        return order, None

    async def modify_order(self, order_id: int, user_id: int, data):
        await auto_cancel_expired_approvals(self.repo.db)
        order = await self.repo.get_order(order_id, user_id)
        if not order:
            return None, "Order not found"
        if order.status not in ("pending_approval", "approved"):
            return None, "Order can only be modified while pending_approval or approved"
        if data.notes is not None: order.notes = data.notes
        if data.delivery_address is not None: order.delivery_address = data.delivery_address
        if data.recipient_name is not None: order.recipient_name = data.recipient_name
        if data.recipient_phone is not None: order.recipient_phone = data.recipient_phone
        if data.scheduled_date is not None: order.scheduled_date = data.scheduled_date
        return order, None

    async def propose_substitution(self, order_id: int, order_item_id: int,
                                    suggested_product_id: int, user_id: int, role: str):
        if role not in ("seller", "admin"):
            return None, "Only sellers can propose substitutions"
        order = await self.repo.get_order_by_id(order_id)
        if not order:
            return None, "Order not found"
        item = await self.repo.get_order_item(order_item_id, order_id)
        if not item:
            return None, "Order item not found"
        product = await self.repo.get_product(suggested_product_id)
        if not product:
            return None, "Suggested product not found"
        sub = Substitution(
            order_id=order_id, order_item_id=order_item_id,
            original_product_id=item.product_id, suggested_product_id=suggested_product_id,
            suggested_product_name=product.name, suggested_product_price=product.price,
        )
        await self.repo.create_substitution(sub)
        return {
            "id": sub.id, "status": sub.status,
            "suggested_product": product.name, "price": product.price,
            "message": "Substitution proposed, awaiting customer approval",
        }, None

    async def get_substitutions(self, order_id: int):
        subs = await self.repo.get_substitutions(order_id)
        return [{"id": s.id, "order_item_id": s.order_item_id,
                 "original_product_id": s.original_product_id,
                 "suggested_product_name": s.suggested_product_name,
                 "suggested_product_price": s.suggested_product_price,
                 "status": s.status} for s in subs]

    async def respond_substitution(self, sub_id: int, approve: bool, user_id: int):
        sub = await self.repo.get_substitution(sub_id)
        if not sub:
            return None, "Substitution not found"
        order = await self.repo.get_order(sub.order_id, user_id)
        if not order:
            return None, "Access denied"
        if sub.status != "pending":
            return None, "Substitution already responded"
        if approve:
            sub.status = "approved"
            item = await self.repo.get_order_item(sub.order_item_id, sub.order_id)
            if item:
                item.product_id = sub.suggested_product_id
                item.unit_price = sub.suggested_product_price
                new_subtotal = await self.repo.get_order_subtotal_sum(order.id)
                order.subtotal = new_subtotal
                order.total = new_subtotal + order.delivery_fee
        else:
            sub.status = "rejected"
        sub.responded_at = datetime.now(timezone.utc)
        return {"id": sub.id, "status": sub.status, "approved": approve}, None

    async def request_compensation(self, order_id: int, user_id: int):
        order = await self.repo.get_order(order_id, user_id)
        if not order:
            return None, "Order not found"
        if order.status != "delivered":
            return None, "Order must be delivered first"
        if not order.scheduled_date:
            return None, "No scheduled delivery time for this order"
        now = datetime.now(timezone.utc)
        scheduled = order.scheduled_date
        if scheduled.tzinfo is None:
            scheduled = scheduled.replace(tzinfo=timezone.utc)
        delay_minutes = (now - scheduled).total_seconds() / 60
        if delay_minutes < 60:
            return None, f"Only {int(delay_minutes)}min delay, compensation requires 60+ min"
        compensation_points = min(int(delay_minutes / 30) * 10, 200)
        user = await self.repo.get_user(user_id)
        if not user:
            return None, "User not found"
        user.points += compensation_points
        self.repo.db.add(PointsTransaction(
            user_id=user_id, amount=compensation_points, type="earn",
            description=f"Late delivery compensation for order #{order.id} ({int(delay_minutes)}min delay)",
            order_id=order.id,
        ))
        return {
            "compensation_points": compensation_points,
            "delay_minutes": int(delay_minutes),
            "new_balance": user.points,
            "message": f"{compensation_points} points awarded for {int(delay_minutes)}min delay",
        }, None
