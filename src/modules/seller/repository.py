from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.seller import Seller
from src.models.question import Question
from src.models.product import Product
from src.models.user import User


class SellerRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> Seller | None:
        r = await self.db.execute(select(Seller).where(Seller.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_by_id(self, seller_id: int) -> Seller | None:
        r = await self.db.execute(select(Seller).where(Seller.id == seller_id))
        return r.scalar_one_or_none()

    async def update(self, seller: Seller, data: dict) -> Seller:
        for field, val in data.items():
            setattr(seller, field, val)
        self.db.add(seller)
        return seller


class QuestionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int) -> Product | None:
        r = await self.db.execute(select(Product).where(Product.id == product_id))
        return r.scalar_one_or_none()

    async def create_question(self, product_id: int, user_id: int, seller_id: int, question: str) -> Question:
        q = Question(product_id=product_id, user_id=user_id, seller_id=seller_id, question=question)
        self.db.add(q)
        return q

    async def get_question_by_id(self, question_id: int) -> Question | None:
        r = await self.db.execute(select(Question).where(Question.id == question_id))
        return r.scalar_one_or_none()

    async def answer_question(self, question: Question, answer: str) -> Question:
        from datetime import datetime, timezone
        question.answer = answer
        question.answered_at = datetime.now(timezone.utc)
        self.db.add(question)
        return question

    async def get_questions_by_product(self, product_id: int) -> list[Question]:
        r = await self.db.execute(
            select(Question).where(Question.product_id == product_id)
            .order_by(Question.created_at.desc())
        )
        return list(r.scalars().all())

    async def get_questions_by_seller(self, seller_id: int) -> list[dict]:
        r = await self.db.execute(
            select(Question).join(Product).where(Product.seller_id == seller_id)
            .order_by(Question.created_at.desc())
        )
        questions = r.scalars().all()
        result = []
        for q in questions:
            u_r = await self.db.execute(select(User).where(User.id == q.user_id))
            u = u_r.scalar_one_or_none()
            result.append({
                "id": q.id, "product_id": q.product_id,
                "user_name": u.full_name if u else None,
                "question": q.question, "answer": q.answer,
                "answered_at": q.answered_at, "created_at": q.created_at,
            })
        return result

    async def get_questions_by_user(self, user_id: int) -> list[Question]:
        r = await self.db.execute(
            select(Question).where(Question.user_id == user_id)
            .order_by(Question.created_at.desc())
        )
        return list(r.scalars().all())
