from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.customer_service.repository import (
    HelpArticleRepository, ForumRepository, KycRepository, CoBrowsingRepository
)

router = APIRouter(prefix="/customer-service", tags=["customer_service"])


@router.post("/help/articles", status_code=201)
async def create_help_article(
    title: str, slug: str, content: str = None, category: str = None, is_published: bool = False,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = HelpArticleRepository(db)
    article = await repo.create_article(title, slug, content, category, is_published)
    await db.commit()
    return article


@router.get("/help/articles")
async def search_help_articles(
    q: str = Query(""), category: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    repo = HelpArticleRepository(db)
    if q:
        return await repo.search(q)
    return await repo.list_by_category(category)


@router.get("/help/articles/{slug}")
async def get_help_article(slug: str, db: AsyncSession = Depends(get_db)):
    repo = HelpArticleRepository(db)
    article = await repo.get_by_slug(slug)
    if not article:
        raise HTTPException(404, "Article not found")
    await db.commit()
    return article


@router.post("/forum/topics", status_code=201)
async def create_forum_topic(
    title: str, content: str,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = ForumRepository(db)
    topic = await repo.create_topic(current_user.id, title, content)
    await db.commit()
    return topic


@router.get("/forum/topics")
async def list_forum_topics(db: AsyncSession = Depends(get_db)):
    repo = ForumRepository(db)
    return await repo.list_topics()


@router.get("/forum/topics/{topic_id}")
async def get_forum_topic(topic_id: int, db: AsyncSession = Depends(get_db)):
    repo = ForumRepository(db)
    result = await repo.get_topic_with_posts(topic_id)
    if not result:
        raise HTTPException(404, "Topic not found")
    await db.commit()
    return result


@router.post("/forum/topics/{topic_id}/posts", status_code=201)
async def create_forum_post(
    topic_id: int, content: str,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = ForumRepository(db)
    post = await repo.create_post(topic_id, current_user.id, content)
    await db.commit()
    return post


@router.post("/kyc/upload", status_code=201)
async def upload_kyc_document(
    doc_type: str, file_url: str, doc_number: str = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = KycRepository(db)
    doc = await repo.upload_document(current_user.id, doc_type, file_url, doc_number)
    await db.commit()
    return doc


@router.get("/kyc/my")
async def get_my_kyc(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = KycRepository(db)
    docs = await repo.list_by_user(current_user.id)
    return docs


@router.get("/admin/kyc/pending")
async def get_pending_kyc(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    repo = KycRepository(db)
    return await repo.get_pending()


@router.put("/admin/kyc/{doc_id}/verify")
async def verify_kyc_document(
    doc_id: int, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin access required")
    repo = KycRepository(db)
    doc = await repo.verify(doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    await db.commit()
    return doc


@router.post("/co-browsing/start", status_code=201)
async def start_co_browsing(
    agent_id: int = None,
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    repo = CoBrowsingRepository(db)
    session = await repo.create_session(current_user.id, agent_id)
    await db.commit()
    return session


@router.post("/co-browsing/{token}/end")
async def end_co_browsing(
    token: str, current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    repo = CoBrowsingRepository(db)
    session = await repo.end_session(token)
    if not session:
        raise HTTPException(404, "Active session not found")
    await db.commit()
    return session
