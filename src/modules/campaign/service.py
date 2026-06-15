from datetime import datetime, timezone
from src.modules.campaign.repository import CampaignRepository


class CampaignService:
    def __init__(self, db):
        self.repo = CampaignRepository(db)

    async def create_campaign(self, data: dict, user_id: int):
        data["created_by"] = user_id
        c = await self.repo.create_campaign(**data)
        return {"id": c.id, "name": c.name, "type": c.type, "message": "Campaign created"}

    async def update_campaign(self, campaign_id: int, data: dict):
        c = await self.repo.get_campaign(campaign_id)
        if not c:
            return None
        await self.repo.update_campaign(c, **data)
        return {"id": c.id, "name": c.name, "message": "Campaign updated"}

    async def active_campaigns(self):
        campaigns = await self.repo.list_active_campaigns()
        return [
            {"id": c.id, "name": c.name, "description": c.description, "type": c.type,
             "discount_type": c.discount_type, "discount_value": c.discount_value,
             "min_order_amount": c.min_order_amount, "max_discount_amount": c.max_discount_amount,
             "applicable_categories": c.applicable_categories.split(",") if c.applicable_categories else [],
             "banner_url": c.banner_url, "end_date": c.end_date.isoformat() if c.end_date else None}
            for c in campaigns
        ]

    async def validate_and_apply(self, campaign_id: int, user_id: int, order_total: float,
                                  category: str = None, seller_id: int = None) -> dict | None:
        c = await self.repo.get_campaign(campaign_id)
        if not c or not c.is_active:
            return None
        now = datetime.now(timezone.utc)
        if c.start_date > now or c.end_date < now:
            return None
        if c.min_order_amount and order_total < c.min_order_amount:
            return None
        if c.max_uses and c.current_uses >= c.max_uses:
            return None
        if c.per_user_limit:
            used = await self.repo.check_usage(campaign_id, user_id)
            if used >= c.per_user_limit:
                return None
        if c.applicable_categories:
            cats = [x.strip() for x in c.applicable_categories.split(",")]
            if category and category not in cats:
                return None
        discount = 0
        if c.discount_type == "percentage":
            discount = order_total * c.discount_value / 100
            if c.max_discount_amount:
                discount = min(discount, c.max_discount_amount)
        elif c.discount_type == "fixed":
            discount = min(c.discount_value, order_total)
        elif c.discount_type == "free_shipping":
            discount = 0
        return {"campaign_id": c.id, "campaign_name": c.name, "discount": round(discount, 2),
                "discount_type": c.discount_type, "discount_value": c.discount_value}

    async def apply_campaign(self, campaign_id: int, user_id: int, order_id: int, order_total: float) -> dict | None:
        result = await self.validate_and_apply(campaign_id, user_id, order_total)
        if not result:
            return None
        await self.repo.record_usage(campaign_id, user_id, order_id, result["discount"])
        return result

    async def list_flash_sales(self):
        rows = await self.repo.list_active_flash_sales()
        return [
            {"id": fs.id, "product_id": fs.product_id, "product_name": p.name,
             "product_image": p.image_url, "original_price": p.price,
             "sale_price": fs.sale_price, "sold_count": fs.sold_count,
             "quantity_limit": fs.quantity_limit,
             "end_date": fs.end_date.isoformat() if fs.end_date else None}
            for fs, p in rows
        ]

    async def create_flash_sale(self, data: dict):
        fs = await self.repo.create_flash_sale(**data)
        return {"id": fs.id, "product_id": fs.product_id, "sale_price": fs.sale_price}
