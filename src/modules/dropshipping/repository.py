from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.dropshipping.models import DropshippingSupplier, DropshippingProduct


class DropshippingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_supplier(self, name: str, api_url: str = None, api_key: str = None) -> DropshippingSupplier:
        s = DropshippingSupplier(name=name, api_url=api_url, api_key=api_key)
        self.db.add(s)
        return s

    async def list_suppliers(self):
        r = await self.db.execute(select(DropshippingSupplier).order_by(DropshippingSupplier.name))
        return r.scalars().all()

    async def link_product(self, supplier_id: int, product_id: int, supplier_sku: str = None, cost_price: float = None) -> DropshippingProduct:
        dp = DropshippingProduct(supplier_id=supplier_id, product_id=product_id, supplier_sku=supplier_sku, cost_price=cost_price)
        self.db.add(dp)
        return dp

    async def list_products(self):
        r = await self.db.execute(
            select(DropshippingProduct).where(DropshippingProduct.is_active == True).order_by(DropshippingProduct.id.desc())
        )
        return r.scalars().all()
