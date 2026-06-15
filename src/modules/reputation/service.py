from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.reputation.repository import ReputationRepository
from src.modules.reputation.models import ExternalReview


class ReputationService:
    def __init__(self, db: AsyncSession):
        self.repo = ReputationRepository(db)

    async def import_external_review(self, hotel_id: int, platform: str, data: dict) -> dict:
        review_data = {
            "hotel_id": hotel_id,
            "platform": platform,
            "external_review_id": data.get("external_review_id"),
            "reviewer_name": data.get("reviewer_name"),
            "rating": data.get("rating"),
            "title": data.get("title"),
            "comment": data.get("comment"),
            "language": data.get("language"),
            "reviewed_at": data.get("reviewed_at"),
            "imported_at": datetime.now(timezone.utc),
        }
        review = await self.repo.reviews.create(review_data)
        await self.update_reputation_score(hotel_id)
        return {"id": review.id, "platform": review.platform, "rating": review.rating, "message": "Review imported"}

    async def respond_to_review(self, review_id: int, response_text: str, user_id: int) -> dict:
        review = await self.repo.reviews.get(review_id)
        if not review:
            raise ValueError("Review not found")
        response = await self.repo.create_review_response(review_id, response_text, user_id)
        return {"id": response.id, "review_id": response.review_id, "message": "Response saved"}

    async def update_reputation_score(self, hotel_id: int) -> dict:
        reviews = await self.repo.reviews.list_by_hotel(hotel_id)
        if not reviews:
            return {"overall_score": 0, "review_count": 0}

        review_count = len(reviews)
        avg_rating = sum(r.rating or 0 for r in reviews) / review_count

        platform_scores = {}
        for platform in ["booking_com", "google", "tripadvisor", "expedia"]:
            platform_reviews = [r for r in reviews if r.platform == platform]
            if platform_reviews:
                platform_scores[platform] = round(sum(r.rating or 0 for r in platform_reviews) / len(platform_reviews), 2)

        responded = sum(1 for r in reviews if r.is_responded)
        response_rate = round(responded / review_count, 2) if review_count else 0

        profile_data = {
            "overall_score": round(avg_rating, 2),
            "review_count": review_count,
            "response_rate": response_rate,
            "platform_scores": platform_scores,
        }
        await self.repo.profiles.upsert(hotel_id, profile_data)
        return profile_data

    async def analyze_sentiment(self, review_id: int) -> dict:
        review = await self.repo.reviews.get(review_id)
        if not review:
            raise ValueError("Review not found")

        comment = (review.comment or "") + " " + (review.title or "")
        positive_words = {"great", "excellent", "amazing", "wonderful", "good", "perfect", "clean", "comfortable", "friendly", "helpful", "beautiful", "nice", "best", "love", "fantastic"}
        negative_words = {"bad", "terrible", "awful", "poor", "dirty", "horrible", "worst", "disappointed", "rude", "uncomfortable", "noisy", "broken", "cold", "slow", "expensive"}
        neutral_words = {"ok", "okay", "fine", "average", "decent", "fair", "standard", "normal", "basic"}

        words = set(comment.lower().split())
        pos_count = sum(1 for w in words if w in positive_words)
        neg_count = sum(1 for w in words if w in negative_words)
        neu_count = sum(1 for w in words if w in neutral_words)

        total = pos_count + neg_count + neu_count
        if pos_count > neg_count and pos_count > neu_count:
            sentiment = "positive"
            score = pos_count / total if total else 0.5
        elif neg_count > pos_count and neg_count > neu_count:
            sentiment = "negative"
            score = -neg_count / total if total else -0.5
        else:
            sentiment = "neutral"
            score = 0

        keywords = [w for w in words if w in positive_words or w in negative_words or w in neutral_words]

        category_keywords = {
            "cleanliness": {"clean", "dirty", "tidy", "messy", "spotless", "filthy"},
            "service": {"friendly", "rude", "helpful", "staff", "service", "slow", "attentive", "unprofessional"},
            "location": {"location", "center", "near", "close", "convenient", "far", "noisy", "quiet"},
            "value": {"expensive", "cheap", "price", "value", "worth", "overpriced", "reasonable"},
            "food": {"breakfast", "food", "delicious", "tasty", "dinner", "restaurant", "meal", "menu"},
        }
        category = None
        for cat, cat_words in category_keywords.items():
            if words & cat_words:
                category = cat
                break

        existing = await self.repo.sentiment.get_by_review(review_id)
        if existing:
            existing.sentiment = sentiment
            existing.score = score
            existing.keywords = list(keywords)[:20]
            existing.category = category
            self.repo.db.add(existing)
            return {"id": existing.id, "sentiment": sentiment, "score": score, "keywords": list(keywords)[:20], "category": category}

        analysis = await self.repo.sentiment.create({
            "review_id": review_id,
            "sentiment": sentiment,
            "score": score,
            "keywords": list(keywords)[:20],
            "category": category,
        })
        return {"id": analysis.id, "sentiment": sentiment, "score": score, "keywords": list(keywords)[:20], "category": category}

    async def generate_alert(self, hotel_id: int, alert_type: str, severity: str, message: str) -> dict:
        alert = await self.repo.alerts.create({
            "hotel_id": hotel_id,
            "alert_type": alert_type,
            "severity": severity,
            "message": message,
        })
        return {"id": alert.id, "alert_type": alert.alert_type, "severity": alert.severity, "message": alert.message}

    async def get_reputation_dashboard(self, hotel_id: int) -> dict:
        return await self.repo.get_dashboard(hotel_id)

    async def get_sentiment_breakdown(self, hotel_id: int) -> dict:
        breakdown = await self.repo.sentiment.breakdown_by_hotel(hotel_id)
        keywords = await self.repo.sentiment.keywords_by_hotel(hotel_id)
        categories = await self.repo.sentiment.category_breakdown(hotel_id)
        return {
            "breakdown": breakdown,
            "keywords": keywords,
            "categories": categories,
        }
