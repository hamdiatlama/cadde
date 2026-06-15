from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.cicek.models import (
    FloristProfile, FlowerProducerProfile, FlowerWholesalerProfile,
    MaterialSupplierProfile, FlowerProduct, CustomOrderDesign,
    SpecialDayReminder, FloristImage, FloristCamera, FreshnessChain,
    FloristDocumentScore, FlowerRating, DeliveryTimeLog,
)


class FloristRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # --- Florist Profile ---
    async def create_florist(self, user_id: int, data: dict) -> FloristProfile:
        f = FloristProfile(user_id=user_id, **data)
        self.db.add(f)
        await self.db.flush()
        return f

    async def get_by_user(self, user_id: int) -> FloristProfile | None:
        r = await self.db.execute(select(FloristProfile).where(FloristProfile.user_id == user_id))
        return r.scalar_one_or_none()

    async def get_by_slug(self, slug: str) -> FloristProfile | None:
        r = await self.db.execute(select(FloristProfile).where(FloristProfile.slug == slug))
        return r.scalar_one_or_none()

    async def get_by_id(self, florist_id: int) -> FloristProfile | None:
        r = await self.db.execute(select(FloristProfile).where(FloristProfile.id == florist_id))
        return r.scalar_one_or_none()

    async def update(self, florist_id: int, data: dict) -> FloristProfile | None:
        f = await self.get_by_id(florist_id)
        if not f:
            return None
        for k, v in data.items():
            setattr(f, k, v)
        await self.db.flush()
        return f

    async def list_active(self, city: str | None = None, page: int = 1, limit: int = 20) -> tuple[list[FloristProfile], int]:
        q = select(FloristProfile).where(FloristProfile.is_active == True)
        if city:
            q = q.where(FloristProfile.city == city)
        cnt = await self.db.execute(select(func.count()).select_from(q.subquery()))
        total = cnt.scalar() or 0
        q = q.order_by(FloristProfile.total_score.desc(), FloristProfile.rating.desc()).offset((page - 1) * limit).limit(limit)
        r = await self.db.execute(q)
        return list(r.scalars().all()), total

    async def toggle_open(self, florist_id: int) -> FloristProfile | None:
        f = await self.get_by_id(florist_id)
        if not f:
            return None
        f.is_open = not f.is_open
        await self.db.flush()
        return f

    # --- Products ---
    async def create_product(self, seller_type: str, seller_id: int, data: dict) -> FlowerProduct:
        p = FlowerProduct(seller_type=seller_type, seller_id=seller_id, **data)
        self.db.add(p)
        await self.db.flush()
        return p

    async def get_product(self, product_id: int) -> FlowerProduct | None:
        r = await self.db.execute(select(FlowerProduct).where(FlowerProduct.id == product_id))
        return r.scalar_one_or_none()

    async def update_product(self, product_id: int, data: dict) -> FlowerProduct | None:
        p = await self.get_product(product_id)
        if not p:
            return None
        for k, v in data.items():
            setattr(p, k, v)
        await self.db.flush()
        return p

    async def list_products(self, seller_type: str | None = None, seller_id: int | None = None,
                            category: str | None = None, occasion: str | None = None,
                            page: int = 1, limit: int = 20) -> tuple[list[FlowerProduct], int]:
        q = select(FlowerProduct).where(FlowerProduct.is_active == True)
        if seller_type:
            q = q.where(FlowerProduct.seller_type == seller_type)
        if seller_id:
            q = q.where(FlowerProduct.seller_id == seller_id)
        if category:
            q = q.where(FlowerProduct.category == category)
        if occasion:
            q = q.where(FlowerProduct.occasion == occasion)
        cnt = await self.db.execute(select(func.count()).select_from(q.subquery()))
        total = cnt.scalar() or 0
        q = q.order_by(FlowerProduct.created_at.desc()).offset((page - 1) * limit).limit(limit)
        r = await self.db.execute(q)
        return list(r.scalars().all()), total

    # --- Special Day Reminders ---
    async def create_reminder(self, user_id: int, data: dict) -> SpecialDayReminder:
        r = SpecialDayReminder(user_id=user_id, **data)
        self.db.add(r)
        await self.db.flush()
        return r

    async def list_reminders(self, user_id: int) -> list[SpecialDayReminder]:
        r = await self.db.execute(
            select(SpecialDayReminder).where(SpecialDayReminder.user_id == user_id, SpecialDayReminder.is_active == True)
            .order_by(SpecialDayReminder.reminder_date)
        )
        return list(r.scalars().all())

    async def delete_reminder(self, reminder_id: int, user_id: int) -> bool:
        r = await self.db.execute(
            select(SpecialDayReminder).where(SpecialDayReminder.id == reminder_id, SpecialDayReminder.user_id == user_id)
        )
        rem = r.scalar_one_or_none()
        if not rem:
            return False
        rem.is_active = False
        await self.db.flush()
        return True

    # --- Custom Order Design ---
    async def create_design(self, customer_id: int, data: dict) -> CustomOrderDesign:
        d = CustomOrderDesign(customer_id=customer_id, **data)
        self.db.add(d)
        await self.db.flush()
        return d

    async def get_design(self, design_id: int) -> CustomOrderDesign | None:
        r = await self.db.execute(select(CustomOrderDesign).where(CustomOrderDesign.id == design_id))
        return r.scalar_one_or_none()

    # --- Florist Images ---
    async def add_image(self, florist_id: int, data: dict) -> FloristImage:
        img = FloristImage(florist_id=florist_id, **data)
        self.db.add(img)
        await self.db.flush()
        return img

    async def list_images(self, florist_id: int) -> list[FloristImage]:
        r = await self.db.execute(
            select(FloristImage).where(FloristImage.florist_id == florist_id, FloristImage.is_active == True)
        )
        return list(r.scalars().all())

    async def delete_image(self, image_id: int, florist_id: int) -> bool:
        r = await self.db.execute(
            select(FloristImage).where(FloristImage.id == image_id, FloristImage.florist_id == florist_id)
        )
        img = r.scalar_one_or_none()
        if not img:
            return False
        img.is_active = False
        await self.db.flush()
        return True

    # --- Florist Cameras ---
    async def add_camera(self, florist_id: int, data: dict) -> FloristCamera:
        cam = FloristCamera(florist_id=florist_id, **data)
        self.db.add(cam)
        await self.db.flush()
        return cam

    async def list_cameras(self, florist_id: int) -> list[FloristCamera]:
        r = await self.db.execute(select(FloristCamera).where(FloristCamera.florist_id == florist_id))
        return list(r.scalars().all())

    # --- Freshness Chain ---
    async def add_freshness_record(self, data: dict) -> FreshnessChain:
        rec = FreshnessChain(**data)
        self.db.add(rec)
        await self.db.flush()
        return rec

    async def get_freshness_chain(self, order_id: int) -> list[FreshnessChain]:
        r = await self.db.execute(
            select(FreshnessChain).where(FreshnessChain.order_id == order_id).order_by(FreshnessChain.happened_at)
        )
        return list(r.scalars().all())

    # --- Document Scores ---
    async def add_document(self, florist_id: int, data: dict) -> FloristDocumentScore:
        doc = FloristDocumentScore(florist_id=florist_id, **data)
        self.db.add(doc)
        await self.db.flush()
        return doc

    async def list_documents(self, florist_id: int) -> list[FloristDocumentScore]:
        r = await self.db.execute(
            select(FloristDocumentScore).where(FloristDocumentScore.florist_id == florist_id, FloristDocumentScore.is_active == True)
        )
        return list(r.scalars().all())

    async def total_document_score(self, florist_id: int) -> int:
        r = await self.db.execute(
            select(func.coalesce(func.sum(FloristDocumentScore.score), 0))
            .where(FloristDocumentScore.florist_id == florist_id, FloristDocumentScore.is_confirmed == True)
        )
        return r.scalar() or 0

    # --- Ratings ---
    async def add_rating(self, data: dict) -> FlowerRating:
        rat = FlowerRating(**data)
        self.db.add(rat)
        await self.db.flush()
        return rat

    async def get_florist_rating(self, florist_id: int) -> tuple[float, int]:
        r = await self.db.execute(
            select(func.avg(FlowerRating.score), func.count(FlowerRating.id))
            .where(FlowerRating.rated_id == florist_id, FlowerRating.rated_type == "florist")
        )
        row = r.one()
        return float(row[0] or 0), row[1] or 0
