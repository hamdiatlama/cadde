from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.cicek.repository import FloristRepo


class FloristService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = FloristRepo(db)

    # --- Florist Profile ---
    async def register(self, user_id: int, data) -> dict:
        existing = await self.repo.get_by_user(user_id)
        if existing:
            return {"error": "Zaten bir çiçekçi dükkanınız var"}
        f = await self.repo.create_florist(user_id, data.model_dump())
        return {"id": f.id, "shop_name": f.shop_name, "slug": f.slug}

    async def get_my_shop(self, user_id: int):
        return await self.repo.get_by_user(user_id)

    async def get_shop(self, florist_id: int):
        return await self.repo.get_by_id(florist_id)

    async def get_shop_by_slug(self, slug: str):
        return await self.repo.get_by_slug(slug)

    async def update_shop(self, florist_id: int, user_id: int, data) -> dict | None:
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return None
        vals = data.model_dump(exclude_unset=True)
        f = await self.repo.update(florist_id, vals)
        return {"id": f.id, "shop_name": f.shop_name, "slug": f.slug}

    async def toggle_open(self, florist_id: int, user_id: int) -> dict | None:
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return None
        f = await self.repo.toggle_open(florist_id)
        return {"id": f.id, "is_open": f.is_open}

    async def list_florists(self, city: str | None = None, page: int = 1, limit: int = 20):
        items, total = await self.repo.list_active(city, page, limit)
        return items, total

    # --- Products ---
    async def create_product(self, seller_type: str, seller_id: int, data):
        p = await self.repo.create_product(seller_type, seller_id, data.model_dump())
        return p

    async def update_product(self, product_id: int, florist_id: int, user_id: int, data):
        p = await self.repo.get_product(product_id)
        if not p or p.seller_id != florist_id:
            return None
        return await self.repo.update_product(product_id, data.model_dump(exclude_unset=True))

    async def list_products(self, seller_type: str | None = None, seller_id: int | None = None,
                            category: str | None = None, occasion: str | None = None,
                            page: int = 1, limit: int = 20):
        return await self.repo.list_products(seller_type, seller_id, category, occasion, page, limit)

    async def get_product(self, product_id: int):
        return await self.repo.get_product(product_id)

    # --- Reminders ---
    async def create_reminder(self, user_id: int, data):
        return await self.repo.create_reminder(user_id, data.model_dump())

    async def list_reminders(self, user_id: int):
        return await self.repo.list_reminders(user_id)

    async def delete_reminder(self, reminder_id: int, user_id: int) -> bool:
        return await self.repo.delete_reminder(reminder_id, user_id)

    # --- Custom Order Design ---
    async def create_design(self, customer_id: int, data):
        return await self.repo.create_design(customer_id, data.model_dump())

    async def get_design(self, design_id: int):
        return await self.repo.get_design(design_id)

    # --- Images ---
    async def add_image(self, florist_id: int, user_id: int, data):
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return None
        return await self.repo.add_image(florist_id, data.model_dump())

    async def list_images(self, florist_id: int):
        return await self.repo.list_images(florist_id)

    async def delete_image(self, image_id: int, florist_id: int, user_id: int) -> bool:
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return False
        return await self.repo.delete_image(image_id, florist_id)

    # --- Cameras ---
    async def add_camera(self, florist_id: int, user_id: int, data):
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return None
        return await self.repo.add_camera(florist_id, data.model_dump())

    async def list_cameras(self, florist_id: int):
        return await self.repo.list_cameras(florist_id)

    # --- Freshness ---
    async def add_freshness_record(self, data):
        return await self.repo.add_freshness_record(data.model_dump())

    async def get_freshness_chain(self, order_id: int):
        return await self.repo.get_freshness_chain(order_id)

    # --- Documents ---
    async def add_document(self, florist_id: int, user_id: int, data):
        f = await self.repo.get_by_id(florist_id)
        if not f or f.user_id != user_id:
            return None
        return await self.repo.add_document(florist_id, data.model_dump())

    async def list_documents(self, florist_id: int):
        return await self.repo.list_documents(florist_id)

    async def total_score(self, florist_id: int) -> int:
        doc_score = await self.repo.total_document_score(florist_id)
        images = await self.repo.list_images(florist_id)
        img_score = sum(i.score_contribution or 0 for i in images)
        cameras = await self.repo.list_cameras(florist_id)
        cam_score = sum(c.score_contribution or 0 for c in cameras)
        total = doc_score + img_score + cam_score
        f = await self.repo.get_by_id(florist_id)
        if f:
            f.total_score = total
            await self.db.flush()
        return total

    # --- Ratings ---
    async def add_rating(self, user_id: int, data):
        rat = await self.repo.add_rating({**data.model_dump(), "rater_id": user_id, "rater_type": "musteri"})
        avg, cnt = await self.repo.get_florist_rating(data.rated_id)
        f = await self.repo.get_by_id(data.rated_id)
        if f:
            f.rating = round(avg, 1)
            f.review_count = cnt
            await self.db.flush()
        return rat
