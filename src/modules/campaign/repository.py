from sqlalchemy import select, func, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.campaign.models import Campaign, CampaignUsage, FlashSale
from src.models.product import Product


class CampaignRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_campaign(self, **kwargs) -> Campaign:
        c = Campaign(**kwargs)
        self.db.add(c)
        return c

    async def update_campaign(self, c: Campaign, **kwargs):
        for k, v in kwargs.items():
            setattr(c, k, v)

    async def get_campaign(self, campaign_id: int):
        r = await self.db.execute(select(Campaign).where(Campaign.id == campaign_id))
        return r.scalar_one_or_none()

    async def list_active_campaigns(self):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(Campaign).where(
                Campaign.is_active == True,
                Campaign.start_date <= now,
                Campaign.end_date >= now,
            ).order_by(Campaign.sort_order.asc(), Campaign.created_at.desc())
        )
        return r.scalars().all()

    async def list_campaigns(self, page: int = 1, per_page: int = 20):
        q = select(Campaign).order_by(Campaign.created_at.desc())
        q = q.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def check_usage(self, campaign_id: int, user_id: int):
        r = await self.db.execute(
            select(func.count()).where(
                CampaignUsage.campaign_id == campaign_id,
                CampaignUsage.user_id == user_id,
            )
        )
        return r.scalar()

    async def record_usage(self, campaign_id: int, user_id: int, order_id: int, amount: float):
        cu = CampaignUsage(campaign_id=campaign_id, user_id=user_id, order_id=order_id, discount_amount=amount)
        self.db.add(cu)
        c = await self.get_campaign(campaign_id)
        if c:
            c.current_uses = (c.current_uses or 0) + 1

    async def create_flash_sale(self, **kwargs) -> FlashSale:
        fs = FlashSale(**kwargs)
        self.db.add(fs)
        return fs

    async def get_flash_sale(self, flash_id: int):
        r = await self.db.execute(select(FlashSale).where(FlashSale.id == flash_id))
        return r.scalar_one_or_none()

    async def list_active_flash_sales(self):
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        r = await self.db.execute(
            select(FlashSale, Product).join(Product, Product.id == FlashSale.product_id)
            .where(
                FlashSale.is_active == True,
                FlashSale.start_date <= now,
                FlashSale.end_date >= now,
                (FlashSale.quantity_limit == 0) | (FlashSale.sold_count < FlashSale.quantity_limit),
            ).order_by(FlashSale.end_date.asc())
        )
        return r.all()

    async def increment_flash_sold(self, flash_id: int, qty: int = 1):
        fs = await self.get_flash_sale(flash_id)
        if fs:
            fs.sold_count = (fs.sold_count or 0) + qty
