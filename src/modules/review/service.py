from src.modules.review.repository import ReviewRepository
from src.models.review import Review

class ReviewService:
    def __init__(self, db):
        self.repo = ReviewRepository(db)

    async def create_review(self, user_id: int, order_id: int, product_id: int,
                            rating: int, comment: str | None, title: str | None,
                            photo_urls: str | None):
        if rating < 1 or rating > 5:
            return None, "Rating must be between 1 and 5"

        order = await self.repo.get_order(order_id, user_id)
        if not order:
            return None, "Order not found"
        if order.status != "delivered":
            return None, "Can only review delivered orders"

        product = await self.repo.get_product(product_id)
        if not product:
            return None, "Product not found"

        existing = await self.repo.get_existing_review(order_id, product_id, user_id)
        if existing:
            return None, "You already reviewed this product in this order"

        review = Review(
            order_id=order_id, user_id=user_id, product_id=product_id,
            seller_id=product.seller_id, rating=rating, title=title,
            comment=comment, photo_urls=photo_urls, is_verified=True,
        )
        await self.repo.create_review(review)

        avg, cnt = await self.repo.get_product_stats(product_id)
        product.rating = round(float(avg), 1) if avg else rating
        product.review_count = (cnt or 0) + 1

        return review, None

    async def get_product_reviews(self, product_id: int, page: int, per_page: int):
        offset = (page - 1) * per_page
        reviews = await self.repo.get_product_reviews(product_id, offset, per_page)
        return [
            {"id": r.id, "user_id": r.user_id, "rating": r.rating, "title": r.title,
             "comment": r.comment,
             "photo_urls": r.photo_urls.split(",") if r.photo_urls else [],
             "is_verified": r.is_verified,
             "created_at": r.created_at.isoformat() if r.created_at else None}
            for r in reviews
        ]

    async def get_my_reviews(self, user_id: int):
        reviews = await self.repo.get_user_reviews(user_id)
        return [
            {"id": r.id, "product_id": r.product_id, "rating": r.rating,
             "title": r.title, "comment": r.comment,
             "photo_urls": r.photo_urls.split(",") if r.photo_urls else [],
             "created_at": r.created_at.isoformat() if r.created_at else None}
            for r in reviews
        ]
