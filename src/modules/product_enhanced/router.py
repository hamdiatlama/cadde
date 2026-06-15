from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.product_enhanced.repository import (
    ProductQnARepository, ProductBundleRepository, GiftRegistryRepository,
    ProductBarcodeRepository, ProductExpiryRepository,
)

router = APIRouter(prefix="/product-enhanced", tags=["product_enhanced"])


@router.post("/questions", status_code=201)
async def ask_question(
    product_id: int, question: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductQnARepository(db)
    q = await repo.ask_question(product_id, current_user.id, question)
    await db.commit()
    return q


@router.post("/questions/{id}/answer", status_code=201)
async def answer_question(
    id: int, answer: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductQnARepository(db)
    a = await repo.answer_question(id, current_user.id, answer)
    await db.commit()
    return a


@router.get("/products/{product_id}/questions")
async def list_questions(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductQnARepository(db)
    return await repo.list_questions(product_id)


@router.post("/bundles", status_code=201)
async def create_bundle(
    name: str, total_price: float = None, discount_rate: float = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductBundleRepository(db)
    b = await repo.create_bundle(current_user.id, name, total_price, discount_rate)
    await db.commit()
    return b


@router.post("/bundles/{id}/items", status_code=201)
async def add_bundle_item(
    id: int, product_id: int, quantity: int = 1,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductBundleRepository(db)
    i = await repo.add_item(id, product_id, quantity)
    await db.commit()
    return i


@router.get("/bundles")
async def list_bundles(db: AsyncSession = Depends(get_db)):
    repo = ProductBundleRepository(db)
    return await repo.list_bundles()


@router.get("/bundles/seller")
async def seller_bundles(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductBundleRepository(db)
    return await repo.list_bundles(current_user.id)


@router.post("/gift-registries", status_code=201)
async def create_gift_registry(
    type: str, title: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GiftRegistryRepository(db)
    r = await repo.create_registry(current_user.id, type, title)
    await db.commit()
    return r


@router.post("/gift-registries/{id}/items", status_code=201)
async def add_gift_item(
    id: int, product_id: int, quantity: int = 1,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GiftRegistryRepository(db)
    i = await repo.add_item(id, product_id, quantity)
    await db.commit()
    return i


@router.get("/gift-registries/my")
async def my_gift_registries(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GiftRegistryRepository(db)
    return await repo.list_user_registries(current_user.id)


@router.get("/gift-registries/code/{code}")
async def get_gift_registry_by_code(code: str, db: AsyncSession = Depends(get_db)):
    repo = GiftRegistryRepository(db)
    r = await repo.get_by_code(code)
    if not r:
        raise HTTPException(404, "Gift registry not found")
    return r


@router.post("/barcodes", status_code=201)
async def add_barcode(
    product_id: int, barcode: str, type: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductBarcodeRepository(db)
    b = await repo.add_barcode(product_id, barcode, type)
    await db.commit()
    return b


@router.get("/barcodes/{barcode}")
async def find_by_barcode(barcode: str, db: AsyncSession = Depends(get_db)):
    repo = ProductBarcodeRepository(db)
    b = await repo.find_by_barcode(barcode)
    if not b:
        raise HTTPException(404, "Barcode not found")
    return b


@router.post("/expiry-batches", status_code=201)
async def add_expiry_batch(
    product_id: int, batch_no: str, lot_no: str = None, quantity: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = ProductExpiryRepository(db)
    b = await repo.add_batch(product_id, batch_no, lot_no, quantity)
    await db.commit()
    return b


@router.get("/expiry-batches/{product_id}")
async def list_expiry_batches(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductExpiryRepository(db)
    return await repo.list_batches(product_id)
