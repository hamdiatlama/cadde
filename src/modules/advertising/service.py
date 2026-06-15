from datetime import datetime, timezone
from src.modules.advertising.repository import AdRepository


class AdService:
    def __init__(self, db):
        self.repo = AdRepository(db)

    async def create_campaign(self, seller_id: int, data: dict):
        data["seller_id"] = seller_id
        c = await self.repo.create_campaign(**data)
        return {"id": c.id, "name": c.name, "type": c.type, "daily_budget": c.daily_budget,
                "total_budget": c.total_budget, "message": "Campaign created"}

    async def update_campaign(self, campaign_id: int, seller_id: int, data: dict):
        c = await self.repo.get_campaign(campaign_id)
        if not c or c.seller_id != seller_id:
            return None
        await self.repo.update_campaign(c, **data)
        return {"id": c.id, "message": "Campaign updated"}

    async def list_my_campaigns(self, seller_id: int):
        campaigns = await self.repo.list_seller_campaigns(seller_id)
        return [
            {"id": c.id, "name": c.name, "type": c.type,
             "daily_budget": c.daily_budget, "total_budget": c.total_budget,
             "spent": c.spent, "impressions": c.impressions, "clicks": c.clicks,
             "conversions": c.conversions, "is_active": c.is_active,
             "start_date": c.start_date.isoformat() if c.start_date else None,
             "end_date": c.end_date.isoformat() if c.end_date else None}
            for c in campaigns
        ]

    async def add_product(self, campaign_id: int, seller_id: int, product_id: int, bid_amount: float):
        c = await self.repo.get_campaign(campaign_id)
        if not c or c.seller_id != seller_id:
            return None, "Campaign not found or access denied"
        ap = await self.repo.add_product(campaign_id=campaign_id, product_id=product_id, bid_amount=bid_amount)
        return {"id": ap.id, "product_id": product_id, "bid_amount": bid_amount}, None

    async def get_campaign_analytics(self, campaign_id: int, seller_id: int):
        c = await self.repo.get_campaign(campaign_id)
        if not c or c.seller_id != seller_id:
            return None
        products = await self.repo.get_campaign_products(campaign_id)
        ctr = round(c.clicks / c.impressions * 100, 2) if c.impressions else 0
        return {
            "campaign": {"id": c.id, "name": c.name, "spent": c.spent,
                         "impressions": c.impressions, "clicks": c.clicks,
                         "conversions": c.conversions, "ctr": ctr,
                         "budget_remaining": max(0, (c.total_budget or 0) - (c.spent or 0))},
            "products": [{"id": ap.id, "product_id": p.id, "product_name": p.name,
                          "bid_amount": ap.bid_amount, "impressions": ap.impressions,
                          "clicks": ap.clicks}
                         for ap, p in products],
        }

    async def get_sponsored(self, limit: int = 10):
        rows = await self.repo.get_sponsored_products(limit)
        return [
            {"ad_product_id": ap.id, "product_id": p.id, "name": p.name,
             "price": p.price, "image_url": p.image_url, "bid": ap.bid_amount}
            for ap, p, c in rows
        ]

    async def record_click(self, ad_product_id: int):
        await self.repo.record_click(ad_product_id)

    async def record_impression(self, ad_product_id: int):
        await self.repo.record_impression(ad_product_id)
