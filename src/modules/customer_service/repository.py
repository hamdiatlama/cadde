import secrets
from datetime import datetime, timezone
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.customer_service.models import HelpArticle, ForumTopic, ForumPost, KycDocument, CoBrowsingSession


class HelpArticleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_article(self, title: str, slug: str, content: str = None, category: str = None, is_published: bool = False) -> HelpArticle:
        article = HelpArticle(title=title, slug=slug, content=content, category=category, is_published=is_published)
        self.db.add(article)
        return article

    async def search(self, q: str):
        pattern = f"%{q}%"
        r = await self.db.execute(
            select(HelpArticle).where(
                or_(HelpArticle.title.ilike(pattern), HelpArticle.content.ilike(pattern)),
                HelpArticle.is_published == True
            )
        )
        return r.scalars().all()

    async def get_by_slug(self, slug: str):
        r = await self.db.execute(select(HelpArticle).where(HelpArticle.slug == slug))
        article = r.scalar_one_or_none()
        if article:
            article.view_count += 1
        return article

    async def list_by_category(self, category: str = None):
        q = select(HelpArticle).where(HelpArticle.is_published == True)
        if category:
            q = q.where(HelpArticle.category == category)
        q = q.order_by(HelpArticle.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()


class ForumRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_topic(self, user_id: int, title: str, content: str) -> ForumTopic:
        topic = ForumTopic(user_id=user_id, title=title, content=content)
        self.db.add(topic)
        return topic

    async def list_topics(self):
        r = await self.db.execute(
            select(ForumTopic).order_by(ForumTopic.is_pinned.desc(), ForumTopic.created_at.desc())
        )
        return r.scalars().all()

    async def create_post(self, topic_id: int, user_id: int, content: str) -> ForumPost:
        post = ForumPost(topic_id=topic_id, user_id=user_id, content=content)
        self.db.add(post)
        return post

    async def get_topic_with_posts(self, topic_id: int):
        r = await self.db.execute(select(ForumTopic).where(ForumTopic.id == topic_id))
        topic = r.scalar_one_or_none()
        if not topic:
            return None
        topic.view_count += 1
        r = await self.db.execute(
            select(ForumPost).where(ForumPost.topic_id == topic_id).order_by(ForumPost.created_at)
        )
        posts = r.scalars().all()
        return {"topic": topic, "posts": posts}


class KycRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upload_document(self, user_id: int, doc_type: str, file_url: str, doc_number: str = None) -> KycDocument:
        doc = KycDocument(user_id=user_id, doc_type=doc_type, file_url=file_url, doc_number=doc_number)
        self.db.add(doc)
        return doc

    async def verify(self, doc_id: int):
        r = await self.db.execute(select(KycDocument).where(KycDocument.id == doc_id))
        doc = r.scalar_one_or_none()
        if doc:
            doc.status = "verified"
            doc.verified_at = datetime.now(timezone.utc)
        return doc

    async def list_by_user(self, user_id: int):
        r = await self.db.execute(
            select(KycDocument).where(KycDocument.user_id == user_id).order_by(KycDocument.created_at.desc())
        )
        return r.scalars().all()

    async def get_pending(self):
        r = await self.db.execute(
            select(KycDocument).where(KycDocument.status == "pending").order_by(KycDocument.created_at)
        )
        return r.scalars().all()


class CoBrowsingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_session(self, user_id: int, agent_id: int = None) -> CoBrowsingSession:
        token = secrets.token_urlsafe(32)
        session = CoBrowsingSession(user_id=user_id, agent_id=agent_id, session_token=token)
        self.db.add(session)
        return session

    async def end_session(self, token: str):
        r = await self.db.execute(
            select(CoBrowsingSession).where(
                CoBrowsingSession.session_token == token,
                CoBrowsingSession.status == "active"
            )
        )
        session = r.scalar_one_or_none()
        if session:
            session.status = "ended"
            session.ended_at = datetime.now(timezone.utc)
        return session
