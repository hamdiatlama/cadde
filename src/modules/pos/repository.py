from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.pos.models import PosTerminal, PosOrder, PosOrderItem


class PosTerminalRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_terminal(self, seller_id: int, name: str, serial_no: str, location: str = None) -> PosTerminal:
        t = PosTerminal(seller_id=seller_id, name=name, serial_no=serial_no, location=location)
        self.db.add(t)
        return t

    async def list_terminals(self, seller_id: int = None):
        stmt = select(PosTerminal)
        if seller_id:
            stmt = stmt.where(PosTerminal.seller_id == seller_id)
        r = await self.db.execute(stmt.order_by(PosTerminal.created_at.desc()))
        return r.scalars().all()


class PosOrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, terminal_id: int, seller_id: int, items: list[dict], payment_method: str, customer_id: int = None, order_id: int = None) -> PosOrder:
        total = sum(it["quantity"] * it["unit_price"] for it in items)
        order = PosOrder(
            terminal_id=terminal_id, seller_id=seller_id,
            customer_id=customer_id, order_id=order_id,
            total=total, payment_method=payment_method
        )
        self.db.add(order)
        await self.db.flush()
        for it in items:
            self.db.add(PosOrderItem(
                pos_order_id=order.id, product_id=it.get("product_id"),
                barcode=it.get("barcode"), name=it.get("name"),
                quantity=it["quantity"], unit_price=it["unit_price"],
                total=it["quantity"] * it["unit_price"]
            ))
        return order

    async def list_orders(self, seller_id: int):
        r = await self.db.execute(
            select(PosOrder).where(PosOrder.seller_id == seller_id)
            .order_by(PosOrder.created_at.desc())
        )
        return r.scalars().all()

    async def get_order(self, order_id: int):
        r = await self.db.execute(select(PosOrder).where(PosOrder.id == order_id))
        return r.scalar_one_or_none()
