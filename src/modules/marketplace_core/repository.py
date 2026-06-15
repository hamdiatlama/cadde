from datetime import datetime, timezone
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.marketplace_core.models import MultiVendorCart, MultiVendorCartItem, SellerApplication, PreOrder, GuestCheckout
from src.modules.ecommerce.order.models import Order, OrderItem
from src.modules.store.models import Product


class MultiVendorCartRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_cart(self, user_id: int) -> MultiVendorCart:
        cart = MultiVendorCart(user_id=user_id)
        self.db.add(cart)
        return cart

    async def add_item(self, cart_id: int, seller_id: int, product_id: int, qty: int, price: float) -> MultiVendorCartItem:
        item = MultiVendorCartItem(cart_id=cart_id, seller_id=seller_id, product_id=product_id, quantity=qty, price=price)
        self.db.add(item)
        return item

    async def get_cart(self, user_id: int) -> MultiVendorCart | None:
        r = await self.db.execute(
            select(MultiVendorCart).where(MultiVendorCart.user_id == user_id).order_by(MultiVendorCart.created_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def get_cart_items(self, cart_id: int) -> list[MultiVendorCartItem]:
        r = await self.db.execute(
            select(MultiVendorCartItem).where(MultiVendorCartItem.cart_id == cart_id)
        )
        return r.scalars().all()

    async def checkout(self, cart_id: int, user_id: int) -> list[Order]:
        cart = await self.db.get(MultiVendorCart, cart_id)
        if not cart:
            return []
        items = await self.get_cart_items(cart_id)
        seller_groups = {}
        for item in items:
            seller_groups.setdefault(item.seller_id, []).append(item)
        orders = []
        for seller_id, seller_items in seller_groups.items():
            subtotal = sum(i.price * i.quantity for i in seller_items)
            order = Order(user_id=user_id, seller_id=seller_id, subtotal=subtotal, total=subtotal)
            self.db.add(order)
            orders.append(order)
            for si in seller_items:
                oi = OrderItem(order_id=order.id, product_id=si.product_id, quantity=si.quantity, unit_price=si.price)
                self.db.add(oi)
        return orders

    async def split_payment(self, cart_id: int) -> list[dict]:
        items = await self.get_cart_items(cart_id)
        shares = {}
        for item in items:
            total = item.price * item.quantity
            shares[item.seller_id] = shares.get(item.seller_id, 0) + total
        return [{"seller_id": sid, "amount": amt} for sid, amt in shares.items()]


class SellerApplicationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def apply(self, user_id: int, company_name: str, tax_number: str, phone: str, business_type: str) -> SellerApplication:
        app = SellerApplication(user_id=user_id, company_name=company_name, tax_number=tax_number, phone=phone, business_type=business_type)
        self.db.add(app)
        return app

    async def approve(self, application_id: int, admin_id: int) -> SellerApplication | None:
        app = await self.db.get(SellerApplication, application_id)
        if not app:
            return None
        app.status = "approved"
        app.reviewed_by = admin_id
        app.reviewed_at = datetime.now(timezone.utc)
        return app

    async def reject(self, application_id: int, admin_id: int, notes: str = None) -> SellerApplication | None:
        app = await self.db.get(SellerApplication, application_id)
        if not app:
            return None
        app.status = "rejected"
        app.reviewed_by = admin_id
        app.reviewed_at = datetime.now(timezone.utc)
        if notes:
            app.notes = notes
        return app

    async def list_pending(self) -> list[SellerApplication]:
        r = await self.db.execute(
            select(SellerApplication).where(SellerApplication.status == "pending").order_by(SellerApplication.created_at.desc())
        )
        return r.scalars().all()

    async def get_status(self, user_id: int) -> SellerApplication | None:
        r = await self.db.execute(
            select(SellerApplication).where(SellerApplication.user_id == user_id).order_by(SellerApplication.created_at.desc()).limit(1)
        )
        return r.scalar_one_or_none()


class PreOrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_pre_order(self, user_id: int, product_id: int, quantity: int, expected_stock_date) -> PreOrder:
        po = PreOrder(user_id=user_id, product_id=product_id, quantity=quantity, expected_stock_date=expected_stock_date)
        self.db.add(po)
        return po

    async def fulfill(self, pre_order_id: int, order_id: int) -> PreOrder | None:
        po = await self.db.get(PreOrder, pre_order_id)
        if not po:
            return None
        po.status = "fulfilled"
        po.order_id = order_id
        return po

    async def list_by_user(self, user_id: int) -> list[PreOrder]:
        r = await self.db.execute(
            select(PreOrder).where(PreOrder.user_id == user_id).order_by(PreOrder.created_at.desc())
        )
        return r.scalars().all()

    async def list_by_seller(self, seller_id: int) -> list[PreOrder]:
        r = await self.db.execute(
            select(PreOrder).join(Product, PreOrder.product_id == Product.id).where(Product.seller_id == seller_id).order_by(PreOrder.created_at.desc())
        )
        return r.scalars().all()


class GuestCheckoutRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_guest(self, email: str, session_id: str, order_id: int) -> GuestCheckout:
        g = GuestCheckout(email=email, session_id=session_id, order_id=order_id)
        self.db.add(g)
        return g

    async def convert_to_account(self, guest_id: int, user_id: int) -> GuestCheckout | None:
        g = await self.db.get(GuestCheckout, guest_id)
        if not g:
            return None
        g.converted_to_user_id = user_id
        return g

    async def get_by_session(self, session_id: str) -> list[GuestCheckout]:
        r = await self.db.execute(
            select(GuestCheckout).where(GuestCheckout.session_id == session_id)
        )
        return r.scalars().all()
