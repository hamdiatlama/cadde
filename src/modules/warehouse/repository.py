from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.warehouse.models import Warehouse, WarehouseStock, WarehouseTransfer


class WarehouseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_warehouse(self, seller_id: int, name: str, address: str = None, city: str = None) -> Warehouse:
        w = Warehouse(seller_id=seller_id, name=name, address=address, city=city)
        self.db.add(w); return w

    async def list_warehouses(self, seller_id: int):
        r = await self.db.execute(
            select(Warehouse).where(Warehouse.seller_id == seller_id, Warehouse.is_active == True)
        )
        return r.scalars().all()

    async def get_warehouse(self, wid: int):
        r = await self.db.execute(select(Warehouse).where(Warehouse.id == wid))
        return r.scalar_one_or_none()

    async def set_stock(self, warehouse_id: int, product_id: int, quantity: int, sku_id: int = None):
        r = await self.db.execute(
            select(WarehouseStock).where(WarehouseStock.warehouse_id == warehouse_id,
                                          WarehouseStock.product_id == product_id,
                                          WarehouseStock.sku_id == sku_id)
        )
        ws = r.scalar_one_or_none()
        if ws:
            ws.quantity = quantity
        else:
            ws = WarehouseStock(warehouse_id=warehouse_id, product_id=product_id, sku_id=sku_id, quantity=quantity)
            self.db.add(ws)
        return ws

    async def get_stock(self, warehouse_id: int = None, product_id: int = None, sku_id: int = None):
        q = select(WarehouseStock)
        if warehouse_id: q = q.where(WarehouseStock.warehouse_id == warehouse_id)
        if product_id: q = q.where(WarehouseStock.product_id == product_id)
        if sku_id: q = q.where(WarehouseStock.sku_id == sku_id)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def total_stock(self, product_id: int, sku_id: int = None):
        from sqlalchemy import func
        q = select(func.sum(WarehouseStock.quantity)).where(WarehouseStock.product_id == product_id)
        if sku_id: q = q.where(WarehouseStock.sku_id == sku_id)
        r = await self.db.execute(q)
        return r.scalar() or 0

    async def create_transfer(self, from_wh: int, to_wh: int, product_id: int, quantity: int) -> WarehouseTransfer:
        t = WarehouseTransfer(from_warehouse_id=from_wh, to_warehouse_id=to_wh, product_id=product_id, quantity=quantity)
        self.db.add(t); return t

    async def create_low_stock_alert(self, seller_id: int):
        r = await self.db.execute(
            select(WarehouseStock).join(Warehouse, Warehouse.id == WarehouseStock.warehouse_id)
            .where(Warehouse.seller_id == seller_id, WarehouseStock.quantity <= WarehouseStock.min_threshold)
        )
        return r.scalars().all()
