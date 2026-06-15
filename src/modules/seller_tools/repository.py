import json
from datetime import datetime, timezone
from sqlalchemy import select, func as sa_func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.seller_tools.models import ListingScore, SellerAcademyCourse, SellerAcademyProgress
from src.modules.store.models import Product


class ListingScoreRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def calculate_score(self, product_id: int) -> dict:
        r = await self.db.execute(select(Product).where(Product.id == product_id))
        product = r.scalar_one_or_none()
        if not product:
            raise ValueError("Product not found")

        suggestions = []

        title_score = 0
        if product.name:
            tl = len(product.name)
            if tl >= 50:
                title_score = 30
            elif tl >= 30:
                title_score = 20
            elif tl >= 10:
                title_score = 10
            if tl < 30:
                suggestions.append("Ürün başlığı en az 30 karakter olmalıdır")
        else:
            suggestions.append("Ürün başlığı girilmemiş")

        description_score = 0
        if product.description:
            dl = len(product.description)
            if dl >= 200:
                description_score = 25
            elif dl >= 100:
                description_score = 15
            elif dl >= 50:
                description_score = 5
            if dl < 100:
                suggestions.append("Ürün açıklaması en az 100 karakter olmalıdır")
        else:
            suggestions.append("Ürün açıklaması girilmemiş")

        image_score = 0
        if product.image_url:
            image_score = 15
        else:
            suggestions.append("Ürün görseli eklenmemiş")

        price_score = 0
        if product.price and product.price > 0:
            if product.compare_price and product.compare_price > product.price:
                price_score = 15
            else:
                price_score = 10
        else:
            suggestions.append("Ürün fiyatı geçersiz")

        category_score = 0
        if product.category:
            category_score = 15
        else:
            suggestions.append("Ürün kategorisi seçilmemiş")

        total = title_score + description_score + image_score + price_score + category_score

        r = await self.db.execute(
            select(ListingScore).where(ListingScore.product_id == product_id)
        )
        existing = r.scalar_one_or_none()
        if existing:
            existing.score = total
            existing.title_score = title_score
            existing.description_score = description_score
            existing.image_score = image_score
            existing.price_score = price_score
            existing.category_score = category_score
            existing.suggestions = json.dumps(suggestions, ensure_ascii=False)
            existing.calculated_at = sa_func.now()
        else:
            ls = ListingScore(
                product_id=product_id, score=total,
                title_score=title_score, description_score=description_score,
                image_score=image_score, price_score=price_score,
                category_score=category_score,
                suggestions=json.dumps(suggestions, ensure_ascii=False)
            )
            self.db.add(ls)

        return {
            "score": total, "title_score": title_score,
            "description_score": description_score, "image_score": image_score,
            "price_score": price_score, "category_score": category_score,
            "suggestions": suggestions
        }

    async def get_score(self, product_id: int):
        r = await self.db.execute(
            select(ListingScore).where(ListingScore.product_id == product_id)
        )
        ls = r.scalar_one_or_none()
        if not ls:
            return None
        return {
            "score": ls.score, "title_score": ls.title_score,
            "description_score": ls.description_score, "image_score": ls.image_score,
            "price_score": ls.price_score, "category_score": ls.category_score,
            "suggestions": json.loads(ls.suggestions) if ls.suggestions else [],
            "calculated_at": ls.calculated_at
        }

    async def get_suggestions(self, product_id: int):
        r = await self.db.execute(
            select(ListingScore).where(ListingScore.product_id == product_id)
        )
        ls = r.scalar_one_or_none()
        if not ls:
            return None
        return {"product_id": product_id, "suggestions": json.loads(ls.suggestions) if ls.suggestions else []}


class SellerAcademyRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_course(self, title: str, description: str = None, content_url: str = None, category: str = None, duration_minutes: int = None, is_published: bool = False) -> SellerAcademyCourse:
        course = SellerAcademyCourse(
            title=title, description=description, content_url=content_url,
            category=category, duration_minutes=duration_minutes, is_published=is_published
        )
        self.db.add(course)
        return course

    async def list_courses(self, category: str = None, published_only: bool = True):
        q = select(SellerAcademyCourse)
        if published_only:
            q = q.where(SellerAcademyCourse.is_published == True)
        if category:
            q = q.where(SellerAcademyCourse.category == category)
        q = q.order_by(SellerAcademyCourse.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def track_progress(self, seller_id: int, course_id: int) -> SellerAcademyProgress:
        r = await self.db.execute(
            select(SellerAcademyProgress).where(
                SellerAcademyProgress.seller_id == seller_id,
                SellerAcademyProgress.course_id == course_id
            )
        )
        progress = r.scalar_one_or_none()
        if progress:
            progress.completed = True
            progress.completed_at = datetime.now(timezone.utc)
        else:
            progress = SellerAcademyProgress(
                seller_id=seller_id, course_id=course_id,
                completed=True, completed_at=datetime.now(timezone.utc)
            )
            self.db.add(progress)
        return progress

    async def get_progress(self, seller_id: int):
        r = await self.db.execute(
            select(SellerAcademyProgress).where(SellerAcademyProgress.seller_id == seller_id)
        )
        return r.scalars().all()
