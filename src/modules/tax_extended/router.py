from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.tax_extended.repository import (
    TaxRateAddressRepository, GibInvoiceRepository, InternationalDocumentRepository,
)

router = APIRouter(prefix="/tax-extended", tags=["tax_extended"])


@router.post("/rates", status_code=201)
async def set_tax_rate(
    country: str, rate: float, state: str = None, city: str = None, tax_type: str = "vat",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = TaxRateAddressRepository(db)
    r = await repo.set_rate(country, rate, state, city, tax_type)
    await db.commit()
    return r


@router.get("/rates")
async def list_tax_rates(db: AsyncSession = Depends(get_db)):
    repo = TaxRateAddressRepository(db)
    return await repo.list_rates()


@router.post("/calculate")
async def calculate_tax(
    country: str, amount: float, state: str = None, city: str = None,
    db: AsyncSession = Depends(get_db),
):
    repo = TaxRateAddressRepository(db)
    rate = await repo.get_rate(country, state, city)
    if not rate:
        raise HTTPException(404, "No tax rate found for this address")
    tax_amount = amount * rate.rate / 100
    return {"rate": rate.rate, "tax_type": rate.tax_type, "tax_amount": tax_amount, "total": amount + tax_amount}


@router.post("/gib/invoices/{order_id}", status_code=201)
async def create_gib_invoice(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = GibInvoiceRepository(db)
    inv = await repo.create_invoice(order_id)
    await db.commit()
    return inv


@router.get("/gib/invoices/{order_id}")
async def get_gib_invoice(order_id: int, db: AsyncSession = Depends(get_db)):
    repo = GibInvoiceRepository(db)
    inv = await repo.get_by_order(order_id)
    if not inv:
        raise HTTPException(404, "Invoice not found")
    return inv


@router.post("/international/documents/{order_id}/{doc_type}", status_code=201)
async def generate_document(
    order_id: int, doc_type: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = InternationalDocumentRepository(db)
    doc = await repo.generate_doc(order_id, doc_type)
    await db.commit()
    return doc


@router.get("/international/documents/{order_id}")
async def list_documents(order_id: int, db: AsyncSession = Depends(get_db)):
    repo = InternationalDocumentRepository(db)
    return await repo.list_by_order(order_id)
