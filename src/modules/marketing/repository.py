import secrets
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.marketing.models import (
    EmailCampaign, SmsCampaign, Affiliate, AffiliateClick,
    AffiliateSale, BlogPost, CustomerSegment,
)


class EmailCampaignRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, seller_id: int, name: str, subject: str, body: str,
                     audience_segment: str = None, scheduled_at=None) -> EmailCampaign:
        c = EmailCampaign(
            seller_id=seller_id, name=name, subject=subject, body=body,
            audience_segment=audience_segment, scheduled_at=scheduled_at,
        )
        self.db.add(c)
        return c

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(EmailCampaign).where(EmailCampaign.seller_id == seller_id)
            .order_by(EmailCampaign.created_at.desc())
        )
        return r.scalars().all()

    async def mark_sent(self, campaign_id: int):
        r = await self.db.execute(
            select(EmailCampaign).where(EmailCampaign.id == campaign_id)
        )
        c = r.scalar_one_or_none()
        if c:
            c.status = "sent"
        return c


class SmsCampaignRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, seller_id: int, message: str, audience_count: int = 0) -> SmsCampaign:
        c = SmsCampaign(seller_id=seller_id, message=message, audience_count=audience_count)
        self.db.add(c)
        return c

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(SmsCampaign).where(SmsCampaign.seller_id == seller_id)
            .order_by(SmsCampaign.created_at.desc())
        )
        return r.scalars().all()


class AffiliateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_affiliate(self, user_id: int) -> Affiliate:
        code = secrets.token_hex(8)
        a = Affiliate(user_id=user_id, referral_code=code)
        self.db.add(a)
        return a

    async def get_by_code(self, code: str):
        r = await self.db.execute(
            select(Affiliate).where(Affiliate.referral_code == code)
        )
        return r.scalar_one_or_none()

    async def get_by_user(self, user_id: int):
        r = await self.db.execute(
            select(Affiliate).where(Affiliate.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def add_sale(self, affiliate_id: int, order_id: int, commission: float) -> AffiliateSale:
        s = AffiliateSale(affiliate_id=affiliate_id, order_id=order_id, commission=commission)
        self.db.add(s)
        r = await self.db.execute(select(Affiliate).where(Affiliate.id == affiliate_id))
        a = r.scalar_one_or_none()
        if a:
            a.total_earnings = Affiliate.total_earnings + commission
        return s

    async def add_click(self, affiliate_id: int, clicked_by: int = None, ip_address: str = None) -> AffiliateClick:
        c = AffiliateClick(affiliate_id=affiliate_id, clicked_by=clicked_by, ip_address=ip_address)
        self.db.add(c)
        return c

    async def get_stats(self, affiliate_id: int):
        r = await self.db.execute(
            select(func.count(AffiliateClick.id)).where(AffiliateClick.affiliate_id == affiliate_id)
        )
        total_clicks = r.scalar() or 0
        r = await self.db.execute(
            select(func.count(AffiliateSale.id)).where(AffiliateSale.affiliate_id == affiliate_id)
        )
        total_sales = r.scalar() or 0
        r = await self.db.execute(
            select(func.coalesce(func.sum(AffiliateSale.commission), 0))
            .where(AffiliateSale.affiliate_id == affiliate_id, AffiliateSale.status == "paid")
        )
        paid_earnings = r.scalar() or 0
        return {
            "total_clicks": total_clicks,
            "total_sales": total_sales,
            "paid_earnings": float(paid_earnings),
        }


class BlogPostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, author_id: int, title: str, slug: str, content: str = None,
                     excerpt: str = None, image_url: str = None, tags: str = None,
                     seller_id: int = None) -> BlogPost:
        p = BlogPost(
            author_id=author_id, title=title, slug=slug, content=content,
            excerpt=excerpt, image_url=image_url, tags=tags, seller_id=seller_id,
        )
        self.db.add(p)
        return p

    async def list_published(self):
        r = await self.db.execute(
            select(BlogPost).where(BlogPost.is_published == True)
            .order_by(BlogPost.published_at.desc())
        )
        return r.scalars().all()

    async def get_by_slug(self, slug: str):
        r = await self.db.execute(
            select(BlogPost).where(BlogPost.slug == slug)
        )
        return r.scalar_one_or_none()

    async def update_view_count(self, post_id: int):
        r = await self.db.execute(
            select(BlogPost).where(BlogPost.id == post_id)
        )
        p = r.scalar_one_or_none()
        if p:
            p.view_count = BlogPost.view_count + 1
        return p

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(BlogPost).where(BlogPost.seller_id == seller_id)
            .order_by(BlogPost.created_at.desc())
        )
        return r.scalars().all()


class CustomerSegmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, seller_id: int, name: str, criteria: str = None) -> CustomerSegment:
        s = CustomerSegment(seller_id=seller_id, name=name, criteria=criteria)
        self.db.add(s)
        return s

    async def list_by_seller(self, seller_id: int):
        r = await self.db.execute(
            select(CustomerSegment).where(CustomerSegment.seller_id == seller_id)
            .order_by(CustomerSegment.created_at.desc())
        )
        return r.scalars().all()
