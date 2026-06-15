import secrets
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.product_enhanced.models import (
    ProductQuestion, ProductAnswer, ProductBundle, BundleItem,
    GiftRegistry, GiftRegistryItem, ProductBarcode, ProductExpiryBatch,
)


class ProductQnARepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def ask_question(self, product_id: int, user_id: int, question: str) -> ProductQuestion:
        q = ProductQuestion(product_id=product_id, user_id=user_id, question=question)
        self.db.add(q)
        return q

    async def answer_question(self, question_id: int, user_id: int, answer: str) -> ProductAnswer:
        a = ProductAnswer(question_id=question_id, user_id=user_id, answer=answer)
        self.db.add(a)
        return a

    async def list_questions(self, product_id: int):
        r = await self.db.execute(
            select(ProductQuestion).where(ProductQuestion.product_id == product_id)
            .order_by(ProductQuestion.created_at.desc())
        )
        return r.scalars().all()


class ProductBundleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_bundle(self, seller_id: int, name: str, total_price: float = None, discount_rate: float = 0) -> ProductBundle:
        b = ProductBundle(seller_id=seller_id, name=name, total_price=total_price, discount_rate=discount_rate)
        self.db.add(b)
        return b

    async def add_item(self, bundle_id: int, product_id: int, quantity: int = 1) -> BundleItem:
        i = BundleItem(bundle_id=bundle_id, product_id=product_id, quantity=quantity)
        self.db.add(i)
        return i

    async def list_bundles(self, seller_id: int = None):
        q = select(ProductBundle).where(ProductBundle.is_active == True)
        if seller_id:
            q = q.where(ProductBundle.seller_id == seller_id)
        q = q.order_by(ProductBundle.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def calculate_price(self, bundle_id: int) -> dict:
        r = await self.db.execute(
            select(BundleItem).where(BundleItem.bundle_id == bundle_id)
        )
        items = r.scalars().all()
        subtotal = sum(getattr(i, "quantity", 1) * getattr(i, "product_price", 0) for i in items)
        r2 = await self.db.execute(select(ProductBundle).where(ProductBundle.id == bundle_id))
        bundle = r2.scalar_one_or_none()
        discount = (bundle.discount_rate or 0) / 100
        total = subtotal * (1 - discount)
        return {"subtotal": subtotal, "discount_rate": bundle.discount_rate, "total": total}


class GiftRegistryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_registry(self, user_id: int, type: str, title: str, event_date: datetime = None, is_public: bool = True) -> GiftRegistry:
        share_code = secrets.token_hex(8)
        r = GiftRegistry(user_id=user_id, type=type, title=title, event_date=event_date, is_public=is_public, share_code=share_code)
        self.db.add(r)
        return r

    async def add_item(self, registry_id: int, product_id: int, quantity: int = 1) -> GiftRegistryItem:
        i = GiftRegistryItem(registry_id=registry_id, product_id=product_id, quantity=quantity)
        self.db.add(i)
        return i

    async def get_by_code(self, share_code: str):
        r = await self.db.execute(select(GiftRegistry).where(GiftRegistry.share_code == share_code))
        return r.scalar_one_or_none()

    async def purchase_item(self, item_id: int, quantity: int = 1) -> GiftRegistryItem:
        r = await self.db.execute(select(GiftRegistryItem).where(GiftRegistryItem.id == item_id))
        item = r.scalar_one_or_none()
        if item and item.purchased_quantity + quantity <= item.quantity:
            item.purchased_quantity += quantity
        return item

    async def list_user_registries(self, user_id: int):
        r = await self.db.execute(
            select(GiftRegistry).where(GiftRegistry.user_id == user_id)
            .order_by(GiftRegistry.created_at.desc())
        )
        return r.scalars().all()


class ProductBarcodeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_barcode(self, product_id: int, barcode: str, type: str = None) -> ProductBarcode:
        b = ProductBarcode(product_id=product_id, barcode=barcode, type=type)
        self.db.add(b)
        return b

    async def find_by_barcode(self, barcode: str):
        r = await self.db.execute(select(ProductBarcode).where(ProductBarcode.barcode == barcode))
        return r.scalar_one_or_none()

    async def list_by_product(self, product_id: int):
        r = await self.db.execute(
            select(ProductBarcode).where(ProductBarcode.product_id == product_id)
        )
        return r.scalars().all()


class ProductExpiryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_batch(self, product_id: int, batch_no: str, lot_no: str = None, quantity: int = 0, expiry_date: datetime = None) -> ProductExpiryBatch:
        b = ProductExpiryBatch(product_id=product_id, batch_no=batch_no, lot_no=lot_no, quantity=quantity, expiry_date=expiry_date)
        self.db.add(b)
        return b

    async def list_batches(self, product_id: int):
        r = await self.db.execute(
            select(ProductExpiryBatch).where(ProductExpiryBatch.product_id == product_id)
            .order_by(ProductExpiryBatch.expiry_date)
        )
        return r.scalars().all()

    async def get_expiring_soon(self, days: int = 30):
        cutoff = datetime.now(timezone.utc) + timedelta(days=days)
        r = await self.db.execute(
            select(ProductExpiryBatch).where(
                ProductExpiryBatch.expiry_date <= cutoff,
                ProductExpiryBatch.expiry_date >= datetime.now(timezone.utc),
                ProductExpiryBatch.quantity > 0
            ).order_by(ProductExpiryBatch.expiry_date)
        )
        return r.scalars().all()
