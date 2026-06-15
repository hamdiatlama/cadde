from datetime import datetime, timezone
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.reputation.models import (
    ReputationProfile, ExternalReview, ReviewResponse,
    SentimentAnalysis, ReputationAlert,
)


class ReputationProfileRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ReputationProfile:
        obj = ReputationProfile(**data)
        self.db.add(obj)
        return obj

    async def get(self, profile_id: int) -> ReputationProfile | None:
        r = await self.db.execute(select(ReputationProfile).where(ReputationProfile.id == profile_id))
        return r.scalar_one_or_none()

    async def get_by_hotel(self, hotel_id: int) -> ReputationProfile | None:
        r = await self.db.execute(select(ReputationProfile).where(ReputationProfile.hotel_id == hotel_id))
        return r.scalar_one_or_none()

    async def update(self, hotel_id: int, data: dict) -> ReputationProfile | None:
        profile = await self.get_by_hotel(hotel_id)
        if not profile:
            return None
        for field, val in data.items():
            setattr(profile, field, val)
        profile.updated_at = datetime.now(timezone.utc)
        self.db.add(profile)
        return profile

    async def upsert(self, hotel_id: int, data: dict) -> ReputationProfile:
        existing = await self.get_by_hotel(hotel_id)
        if existing:
            for field, val in data.items():
                setattr(existing, field, val)
            existing.updated_at = datetime.now(timezone.utc)
            self.db.add(existing)
            return existing
        data["hotel_id"] = hotel_id
        obj = ReputationProfile(**data)
        self.db.add(obj)
        return obj


class ExternalReviewRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ExternalReview:
        obj = ExternalReview(**data)
        self.db.add(obj)
        return obj

    async def get(self, review_id: int) -> ExternalReview | None:
        r = await self.db.execute(select(ExternalReview).where(ExternalReview.id == review_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(
        self, hotel_id: int, platform: str | None = None,
        sentiment: str | None = None, date_from=None, date_to=None,
    ) -> list[ExternalReview]:
        q = select(ExternalReview).where(ExternalReview.hotel_id == hotel_id)
        if platform:
            q = q.where(ExternalReview.platform == platform)
        if date_from:
            q = q.where(ExternalReview.reviewed_at >= date_from)
        if date_to:
            q = q.where(ExternalReview.reviewed_at <= date_to)
        if sentiment:
            sq = select(SentimentAnalysis.review_id).where(SentimentAnalysis.sentiment == sentiment)
            q = q.where(ExternalReview.id.in_(sq))
        q = q.order_by(ExternalReview.reviewed_at.desc())
        r = await self.db.execute(q)
        return list(r.scalars().all())

    async def list_by_platform(self, hotel_id: int, platform: str) -> list[ExternalReview]:
        r = await self.db.execute(
            select(ExternalReview).where(
                ExternalReview.hotel_id == hotel_id,
                ExternalReview.platform == platform,
            ).order_by(ExternalReview.reviewed_at.desc())
        )
        return list(r.scalars().all())

    async def count_by_hotel(self, hotel_id: int) -> int:
        r = await self.db.execute(
            select(func.count(ExternalReview.id)).where(ExternalReview.hotel_id == hotel_id)
        )
        return r.scalar() or 0

    async def avg_rating_by_hotel(self, hotel_id: int) -> float:
        r = await self.db.execute(
            select(func.avg(ExternalReview.rating)).where(ExternalReview.hotel_id == hotel_id)
        )
        return float(r.scalar() or 0)


class ReviewResponseRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ReviewResponse:
        obj = ReviewResponse(**data)
        self.db.add(obj)
        return obj

    async def get_by_review(self, review_id: int) -> ReviewResponse | None:
        r = await self.db.execute(
            select(ReviewResponse).where(ReviewResponse.review_id == review_id)
        )
        return r.scalar_one_or_none()


class SentimentAnalysisRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> SentimentAnalysis:
        obj = SentimentAnalysis(**data)
        self.db.add(obj)
        return obj

    async def get_by_review(self, review_id: int) -> SentimentAnalysis | None:
        r = await self.db.execute(
            select(SentimentAnalysis).where(SentimentAnalysis.review_id == review_id)
        )
        return r.scalar_one_or_none()

    async def breakdown_by_hotel(self, hotel_id: int) -> dict:
        r = await self.db.execute(
            select(
                SentimentAnalysis.sentiment,
                func.count(SentimentAnalysis.id),
                func.avg(SentimentAnalysis.score),
            ).join(ExternalReview, ExternalReview.id == SentimentAnalysis.review_id)
            .where(ExternalReview.hotel_id == hotel_id)
            .group_by(SentimentAnalysis.sentiment)
        )
        rows = r.all()
        return {
            "positive": {"count": 0, "avg_score": 0},
            "neutral": {"count": 0, "avg_score": 0},
            "negative": {"count": 0, "avg_score": 0},
            **{
                row[0]: {"count": row[1], "avg_score": round(float(row[2] or 0), 2)}
                for row in rows
            },
        }

    async def keywords_by_hotel(self, hotel_id: int) -> list[dict]:
        r = await self.db.execute(
            select(SentimentAnalysis.keywords, SentimentAnalysis.sentiment)
            .join(ExternalReview, ExternalReview.id == SentimentAnalysis.review_id)
            .where(ExternalReview.hotel_id == hotel_id)
        )
        rows = r.all()
        keyword_map = {}
        for row in rows:
            keywords = row[0] or []
            sentiment = row[1]
            for kw in keywords:
                if kw not in keyword_map:
                    keyword_map[kw] = {"keyword": kw, "positive": 0, "neutral": 0, "negative": 0}
                keyword_map[kw][sentiment] = keyword_map[kw].get(sentiment, 0) + 1
        return sorted(keyword_map.values(), key=lambda x: x["positive"] + x["neutral"] + x["negative"], reverse=True)

    async def category_breakdown(self, hotel_id: int) -> list[dict]:
        r = await self.db.execute(
            select(
                SentimentAnalysis.category,
                func.count(SentimentAnalysis.id),
                func.avg(SentimentAnalysis.score),
            ).join(ExternalReview, ExternalReview.id == SentimentAnalysis.review_id)
            .where(
                ExternalReview.hotel_id == hotel_id,
                SentimentAnalysis.category.isnot(None),
            )
            .group_by(SentimentAnalysis.category)
        )
        return [
            {"category": row[0], "count": row[1], "avg_score": round(float(row[2] or 0), 2)}
            for row in r.all()
        ]


class ReputationAlertRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: dict) -> ReputationAlert:
        obj = ReputationAlert(**data)
        self.db.add(obj)
        return obj

    async def get(self, alert_id: int) -> ReputationAlert | None:
        r = await self.db.execute(select(ReputationAlert).where(ReputationAlert.id == alert_id))
        return r.scalar_one_or_none()

    async def list_by_hotel(self, hotel_id: int, is_resolved: bool | None = None) -> list[ReputationAlert]:
        q = select(ReputationAlert).where(ReputationAlert.hotel_id == hotel_id)
        if is_resolved is not None:
            q = q.where(ReputationAlert.is_resolved == is_resolved)
        q = q.order_by(ReputationAlert.created_at.desc())
        r = await self.db.execute(q)
        return list(r.scalars().all())

    async def resolve(self, alert_id: int) -> ReputationAlert | None:
        alert = await self.get(alert_id)
        if not alert:
            return None
        alert.is_resolved = True
        self.db.add(alert)
        return alert


class ReputationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.profiles = ReputationProfileRepository(db)
        self.reviews = ExternalReviewRepository(db)
        self.responses = ReviewResponseRepository(db)
        self.sentiment = SentimentAnalysisRepository(db)
        self.alerts = ReputationAlertRepository(db)

    async def get_hotel_profile(self, hotel_id: int) -> dict | None:
        profile = await self.profiles.get_by_hotel(hotel_id)
        if not profile:
            return None
        return {
            "id": profile.id,
            "hotel_id": profile.hotel_id,
            "overall_score": profile.overall_score,
            "review_count": profile.review_count,
            "response_rate": profile.response_rate,
            "avg_response_time_hours": profile.avg_response_time_hours,
            "platform_scores": profile.platform_scores,
            "created_at": profile.created_at.isoformat() if profile.created_at else None,
            "updated_at": profile.updated_at.isoformat() if profile.updated_at else None,
        }

    async def list_external_reviews(
        self, hotel_id: int, platform: str | None = None,
        sentiment: str | None = None, date_from=None, date_to=None,
    ) -> list[dict]:
        reviews = await self.reviews.list_by_hotel(hotel_id, platform, sentiment, date_from, date_to)
        result = []
        for rv in reviews:
            sent = await self.sentiment.get_by_review(rv.id)
            resp = await self.responses.get_by_review(rv.id)
            result.append({
                "id": rv.id,
                "hotel_id": rv.hotel_id,
                "platform": rv.platform,
                "external_review_id": rv.external_review_id,
                "reviewer_name": rv.reviewer_name,
                "rating": rv.rating,
                "title": rv.title,
                "comment": rv.comment,
                "language": rv.language,
                "reviewed_at": rv.reviewed_at.isoformat() if rv.reviewed_at else None,
                "imported_at": rv.imported_at.isoformat() if rv.imported_at else None,
                "is_responded": rv.is_responded,
                "created_at": rv.created_at.isoformat() if rv.created_at else None,
                "sentiment": sent.sentiment if sent else None,
                "sentiment_score": sent.score if sent else None,
                "response": resp.response_text if resp else None,
            })
        return result

    async def list_alerts(self, hotel_id: int, is_resolved: bool | None = None) -> list[dict]:
        alerts = await self.alerts.list_by_hotel(hotel_id, is_resolved)
        return [
            {
                "id": a.id,
                "hotel_id": a.hotel_id,
                "alert_type": a.alert_type,
                "severity": a.severity,
                "message": a.message,
                "is_resolved": a.is_resolved,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in alerts
        ]

    async def create_review_response(self, review_id: int, response_text: str, user_id: int) -> ReviewResponse:
        data = {
            "review_id": review_id,
            "response_text": response_text,
            "responded_by": user_id,
        }
        obj = await self.responses.create(data)
        review = await self.reviews.get(review_id)
        if review:
            review.is_responded = True
            self.db.add(review)
        return obj

    async def get_dashboard(self, hotel_id: int) -> dict:
        profile = await self.profiles.get_by_hotel(hotel_id)
        recent_reviews = await self.reviews.list_by_hotel(hotel_id, limit=5) if hasattr(self.reviews, 'list_by_hotel') else []
        alerts = await self.alerts.list_by_hotel(hotel_id, is_resolved=False)
        sentiment_breakdown = await self.sentiment.breakdown_by_hotel(hotel_id)
        category_breakdown = await self.sentiment.category_breakdown(hotel_id)

        return {
            "profile": {
                "overall_score": profile.overall_score if profile else 0,
                "review_count": profile.review_count if profile else 0,
                "response_rate": profile.response_rate if profile else 0,
                "avg_response_time_hours": profile.avg_response_time_hours if profile else None,
                "platform_scores": profile.platform_scores if profile else {},
            } if profile else None,
            "recent_reviews": [
                {
                    "id": r.id, "platform": r.platform, "rating": r.rating,
                    "reviewer_name": r.reviewer_name, "comment": r.comment,
                    "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None,
                    "is_responded": r.is_responded,
                }
                for r in recent_reviews
            ],
            "alerts": [
                {
                    "id": a.id, "alert_type": a.alert_type, "severity": a.severity,
                    "message": a.message, "is_resolved": a.is_resolved,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                }
                for a in alerts
            ],
            "sentiment_breakdown": sentiment_breakdown,
            "category_breakdown": category_breakdown,
        }
