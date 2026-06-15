from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.advertising.models import AdCampaign, AdProduct
from src.models.product import Product


class AdRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_campaign(self, **kwargs) -> AdCampaign:
        c = AdCampaign(**kwargs)
        self.db.add(c)
        return c

    async def update_campaign(self, c: AdCampaign, **kwargs):
        for k, v in kwargs.items(): setattr(c, k, v)

    async def get_campaign(self, campaign_id: int):
        r = await self.db.execute(select(AdCampaign).where(AdCampaign.id == campaign_id))
        return r.scalar_one_or_none()

    async def list_seller_campaigns(self, seller_id: int):
        r = await self.db.execute(
            select(AdCampaign).where(AdCampaign.seller_id == seller_id).order_by(AdCampaign.created_at.desc())
        )
        return r.scalars().all()

    async def list_active_campaigns(self):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(AdCampaign).where(
                AdCampaign.is_active == True, AdCampaign.start_date <= now,
                (AdCampaign.end_date == None) | (AdCampaign.end_date >= now),
            )
        )
        return r.scalars().all()

    async def add_product(self, **kwargs) -> AdProduct:
        ap = AdProduct(**kwargs)
        self.db.add(ap)
        return ap

    async def get_campaign_products(self, campaign_id: int):
        r = await self.db.execute(
            select(AdProduct, Product).join(Product, Product.id == AdProduct.product_id)
            .where(AdProduct.campaign_id == campaign_id, AdProduct.is_active == True)
        )
        return r.all()

    async def get_sponsored_products(self, limit: int = 10):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(AdProduct, Product, AdCampaign)
            .join(Product, Product.id == AdProduct.product_id)
            .join(AdCampaign, AdCampaign.id == AdProduct.campaign_id)
            .where(
                AdProduct.is_active == True, AdCampaign.is_active == True,
                AdCampaign.start_date <= now,
                (AdCampaign.end_date == None) | (AdCampaign.end_date >= now),
                AdCampaign.spent < AdCampaign.total_budget,
            )
            .order_by(AdProduct.bid_amount.desc())
            .limit(limit)
        )
        return r.all()

    async def record_click(self, ad_product_id: int):
        ap = await self.db.execute(select(AdProduct).where(AdProduct.id == ad_product_id))
        ap = ap.scalar_one_or_none()
        if ap:
            ap.clicks = (ap.clicks or 0) + 1
            c = await self.get_campaign(ap.campaign_id)
            if c:
                c.clicks = (c.clicks or 0) + 1
                c.spent = (c.spent or 0) + (ap.bid_amount or 0)

    async def record_impression(self, ad_product_id: int):
        ap = await self.db.execute(select(AdProduct).where(AdProduct.id == ad_product_id))
        ap = ap.scalar_one_or_none()
        if ap:
            ap.impressions = (ap.impressions or 0) + 1
            c = await self.get_campaign(ap.campaign_id)
            if c:
                c.impressions = (c.impressions or 0) + 1
