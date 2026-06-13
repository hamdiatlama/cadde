from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.seller.repository import SellerRepository, QuestionRepository
from src.modules.seller.events import publish_event, SellerEvent


class SellerProfileService:
    def __init__(self, db: AsyncSession):
        self.repo = SellerRepository(db)

    async def get_profile(self, user_id: int):
        seller = await self.repo.get_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        return seller

    async def get_by_id(self, seller_id: int):
        seller = await self.repo.get_by_id(seller_id)
        if not seller:
            raise ValueError("Seller not found")
        return seller

    async def update(self, user_id: int, data: dict) -> dict:
        seller = await self.repo.get_by_user_id(user_id)
        if not seller:
            raise ValueError("Seller profile not found")
        await self.repo.update(seller, data)
        await publish_event(SellerEvent.SELLER_PROFILE_UPDATED, {"seller_id": seller.id})
        return {"status": "updated"}


class QuestionService:
    def __init__(self, db: AsyncSession):
        self.repo = QuestionRepository(db)

    async def ask_question(self, product_id: int, user_id: int, question: str) -> dict:
        product = await self.repo.get_product_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        q = await self.repo.create_question(product_id, user_id, product.seller_id, question)
        await publish_event(SellerEvent.QUESTION_ASKED, {"question_id": q.id, "product_id": product_id})
        return {"id": q.id, "question": q.question, "created_at": q.created_at}

    async def answer_question(self, question_id: int, seller_user_id: int, answer: str) -> dict:
        from src.models.seller import Seller
        from sqlalchemy import select
        seller_r = await self.repo.db.execute(select(Seller).where(Seller.user_id == seller_user_id))
        seller = seller_r.scalar_one_or_none()
        if not seller:
            raise ValueError("Seller profile not found")

        question = await self.repo.get_question_by_id(question_id)
        if not question:
            raise ValueError("Question not found")

        product = await self.repo.get_product_by_id(question.product_id)
        if not product or product.seller_id != seller.id:
            raise ValueError("This question is not for your product")

        if question.answer:
            raise ValueError("Question already answered")

        await self.repo.answer_question(question, answer)
        await publish_event(SellerEvent.QUESTION_ANSWERED, {"question_id": question.id})
        return {"status": "answered"}

    async def get_product_questions(self, product_id: int) -> list:
        return await self.repo.get_questions_by_product(product_id)

    async def get_seller_questions(self, seller_user_id: int) -> list:
        from src.models.seller import Seller
        from sqlalchemy import select
        seller_r = await self.repo.db.execute(select(Seller).where(Seller.user_id == seller_user_id))
        seller = seller_r.scalar_one_or_none()
        if not seller:
            raise ValueError("Seller profile not found")
        return await self.repo.get_questions_by_seller(seller.id)

    async def get_my_questions(self, user_id: int) -> list:
        return await self.repo.get_questions_by_user(user_id)
