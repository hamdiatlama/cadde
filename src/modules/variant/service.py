from src.modules.variant.repository import VariantRepository


class VariantService:
    def __init__(self, db):
        self.repo = VariantRepository(db)

    async def add_group(self, product_id: int, name: str, sort_order: int = 0):
        g = await self.repo.create_group(product_id, name, sort_order)
        return {"id": g.id, "name": g.name}

    async def add_option(self, group_id: int, value: str, sort_order: int = 0):
        o = await self.repo.create_option(group_id, value, sort_order)
        return {"id": o.id, "value": o.value}

    async def add_sku(self, product_id: int, sku: str, option_ids: list[int], **kwargs):
        s = await self.repo.create_sku(product_id, sku, **kwargs)
        for oid in option_ids:
            await self.repo.add_mapping(s.id, oid)
        return {"id": s.id, "sku": s.sku}

    async def get_variants(self, product_id: int):
        return await self.repo.get_full_variants(product_id)

    async def get_sku_by_selection(self, product_id: int, option_ids: list[int]):
        sku = await self.repo.get_sku_by_options(product_id, option_ids)
        if not sku:
            return None
        return {"id": sku.id, "sku": sku.sku, "stock": sku.stock, "price_override": sku.price_override,
                "barcode": sku.barcode, "image_url": sku.image_url}
