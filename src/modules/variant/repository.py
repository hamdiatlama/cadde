from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.variant.models import ProductVariantGroup, ProductVariantOption, ProductVariantSku, ProductVariantMapping
from src.models.product import Product


class VariantRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_group(self, product_id: int, name: str, sort_order: int = 0) -> ProductVariantGroup:
        g = ProductVariantGroup(product_id=product_id, name=name, sort_order=sort_order)
        self.db.add(g); return g

    async def list_groups(self, product_id: int):
        r = await self.db.execute(
            select(ProductVariantGroup).where(ProductVariantGroup.product_id == product_id).order_by(ProductVariantGroup.sort_order)
        )
        return r.scalars().all()

    async def create_option(self, group_id: int, value: str, sort_order: int = 0) -> ProductVariantOption:
        o = ProductVariantOption(group_id=group_id, value=value, sort_order=sort_order)
        self.db.add(o); return o

    async def list_options(self, group_id: int):
        r = await self.db.execute(
            select(ProductVariantOption).where(ProductVariantOption.group_id == group_id).order_by(ProductVariantOption.sort_order)
        )
        return r.scalars().all()

    async def create_sku(self, product_id: int, sku: str, barcode: str = None, price_override: float = None,
                          compare_price_override: float = None, stock: int = 0, image_url: str = None) -> ProductVariantSku:
        s = ProductVariantSku(product_id=product_id, sku=sku, barcode=barcode, price_override=price_override,
                               compare_price_override=compare_price_override, stock=stock, image_url=image_url)
        self.db.add(s); return s

    async def list_skus(self, product_id: int):
        r = await self.db.execute(
            select(ProductVariantSku).where(ProductVariantSku.product_id == product_id, ProductVariantSku.is_active == True)
        )
        return r.scalars().all()

    async def get_sku(self, sku_id: int):
        r = await self.db.execute(select(ProductVariantSku).where(ProductVariantSku.id == sku_id))
        return r.scalar_one_or_none()

    async def get_sku_by_code(self, sku: str):
        r = await self.db.execute(select(ProductVariantSku).where(ProductVariantSku.sku == sku))
        return r.scalar_one_or_none()

    async def update_sku_stock(self, sku_id: int, delta: int):
        s = await self.get_sku(sku_id)
        if s: s.stock = max(0, (s.stock or 0) + delta)

    async def add_mapping(self, sku_id: int, option_id: int):
        m = ProductVariantMapping(sku_id=sku_id, option_id=option_id)
        self.db.add(m)

    async def get_sku_by_options(self, product_id: int, option_ids: list[int]):
        from sqlalchemy import func
        r = await self.db.execute(
            select(ProductVariantSku).join(ProductVariantMapping, ProductVariantMapping.sku_id == ProductVariantSku.id)
            .where(ProductVariantSku.product_id == product_id, ProductVariantSku.is_active == True,
                   ProductVariantMapping.option_id.in_(option_ids))
            .group_by(ProductVariantSku.id)
            .having(func.count(ProductVariantMapping.id) == len(option_ids))
        )
        return r.scalar_one_or_none()

    async def get_full_variants(self, product_id: int) -> list[dict]:
        groups = await self.list_groups(product_id)
        skus = await self.list_skus(product_id)
        result = []
        for g in groups:
            opts = await self.list_options(g.id)
            result.append({"id": g.id, "name": g.name, "options": [{"id": o.id, "value": o.value} for o in opts]})
        sku_list = []
        for s in skus:
            r2 = await self.db.execute(
                select(ProductVariantOption.value).join(ProductVariantMapping, ProductVariantMapping.option_id == ProductVariantOption.id)
                .where(ProductVariantMapping.sku_id == s.id)
            )
            vals = [row[0] for row in r2.all()]
            sku_list.append({"id": s.id, "sku": s.sku, "barcode": s.barcode, "price_override": s.price_override,
                             "stock": s.stock, "image_url": s.image_url, "variant_values": vals})
        return {"groups": result, "skus": sku_list}
