import re
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from sqlalchemy import select
from src.modules.marketing.models import BlogPost
from src.modules.marketing.repository import (
    EmailCampaignRepository, SmsCampaignRepository, AffiliateRepository,
    BlogPostRepository, CustomerSegmentRepository,
)

router = APIRouter(prefix="/marketing", tags=["marketing"])


class EmailCampaignCreate(BaseModel):
    name: str
    subject: str
    body: str
    audience_segment: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class SmsCampaignCreate(BaseModel):
    message: str
    audience_count: int = 0


class BlogPostCreate(BaseModel):
    title: str
    content: Optional[str] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    image_url: Optional[str] = None
    tags: Optional[str] = None
    is_published: Optional[bool] = None


class CustomerSegmentCreate(BaseModel):
    name: str
    criteria: Optional[str] = None


def _generate_slug(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


@router.post("/email-campaigns", status_code=201)
async def create_email_campaign(
    data: EmailCampaignCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailCampaignRepository(db)
    c = await repo.create(
        seller_id=current_user.id, name=data.name, subject=data.subject,
        body=data.body, audience_segment=data.audience_segment,
        scheduled_at=data.scheduled_at,
    )
    await db.commit()
    return c


@router.get("/email-campaigns")
async def list_email_campaigns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = EmailCampaignRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.post("/sms-campaigns", status_code=201)
async def create_sms_campaign(
    data: SmsCampaignCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SmsCampaignRepository(db)
    c = await repo.create(
        seller_id=current_user.id, message=data.message,
        audience_count=data.audience_count,
    )
    await db.commit()
    return c


@router.get("/sms-campaigns")
async def list_sms_campaigns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = SmsCampaignRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.post("/affiliates/register", status_code=201)
async def register_affiliate(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = AffiliateRepository(db)
    existing = await repo.get_by_user(current_user.id)
    if existing:
        raise HTTPException(400, "Already registered as affiliate")
    a = await repo.create_affiliate(current_user.id)
    await db.commit()
    return a


@router.get("/affiliates/my")
async def my_affiliate(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = AffiliateRepository(db)
    a = await repo.get_by_user(current_user.id)
    if not a:
        raise HTTPException(404, "Not registered as affiliate")
    return a


@router.get("/affiliates/stats")
async def affiliate_stats(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = AffiliateRepository(db)
    a = await repo.get_by_user(current_user.id)
    if not a:
        raise HTTPException(404, "Not registered as affiliate")
    stats = await repo.get_stats(a.id)
    return {**stats, "referral_code": a.referral_code, "commission_rate": a.commission_rate,
            "total_earnings": a.total_earnings}


@router.post("/affiliates/click", status_code=201)
async def record_affiliate_click(
    referral_code: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = AffiliateRepository(db)
    a = await repo.get_by_code(referral_code)
    if not a:
        raise HTTPException(404, "Invalid referral code")
    c = await repo.add_click(a.id, clicked_by=current_user.id)
    await db.commit()
    return {"id": c.id}


@router.post("/blog/posts", status_code=201)
async def create_blog_post(
    data: BlogPostCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BlogPostRepository(db)
    slug = _generate_slug(data.title)
    existing = await repo.get_by_slug(slug)
    if existing:
        slug = f"{slug}-{int(datetime.now(timezone.utc).timestamp())}"
    p = await repo.create(
        author_id=current_user.id, title=data.title, slug=slug,
        content=data.content, excerpt=data.excerpt, image_url=data.image_url,
        tags=data.tags,
    )
    await db.commit()
    return p


@router.put("/blog/posts/{post_id}")
async def update_blog_post(
    post_id: int, data: BlogPostUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BlogPostRepository(db)
    r = await db.execute(
        select(BlogPost).where(BlogPost.id == post_id, BlogPost.author_id == current_user.id)
    )
    p = r.scalar_one_or_none()
    if not p:
        raise HTTPException(404, "Blog post not found")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(p, field, value)
    if data.is_published and not p.published_at:
        p.published_at = datetime.now(timezone.utc)
    await db.commit()
    return p


@router.get("/blog/posts")
async def list_published_posts(db: AsyncSession = Depends(get_db)):
    repo = BlogPostRepository(db)
    return await repo.list_published()


@router.get("/blog/posts/{slug}")
async def get_blog_post(slug: str, db: AsyncSession = Depends(get_db)):
    repo = BlogPostRepository(db)
    p = await repo.get_by_slug(slug)
    if not p or not p.is_published:
        raise HTTPException(404, "Blog post not found")
    await repo.update_view_count(p.id)
    await db.commit()
    return p


@router.get("/blog/posts/seller")
async def list_seller_posts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BlogPostRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.post("/segments", status_code=201)
async def create_segment(
    data: CustomerSegmentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = CustomerSegmentRepository(db)
    s = await repo.create(seller_id=current_user.id, name=data.name, criteria=data.criteria)
    await db.commit()
    return s


@router.get("/segments")
async def list_segments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = CustomerSegmentRepository(db)
    return await repo.list_by_seller(current_user.id)
