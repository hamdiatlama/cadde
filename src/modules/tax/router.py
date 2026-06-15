from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.tax.repository import TaxService, TaxRepository

router = APIRouter(prefix="/tax", tags=["tax"])


@router.post("/calculate")
async def calculate_tax(subtotal: float, category_id: int = None, db: AsyncSession = Depends(get_db)):
    svc = TaxService(db)
    return await svc.calculate_tax(subtotal, category_id)


@router.post("/rates", status_code=201)
async def create_tax_rate(rate: float, tax_type: str = "kdv", category_id: int = None,
                            current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = TaxRepository(db)
    t = await repo.create_tax_rate(rate, tax_type, category_id)
    await db.commit()
    return {"id": t.id, "rate": t.rate, "tax_type": t.tax_type}


@router.get("/rates")
async def list_tax_rates(db: AsyncSession = Depends(get_db)):
    repo = TaxRepository(db)
    r = await repo.get_default_tax_rate()
    return {"default_rate": r.rate if r else 20, "tax_type": r.tax_type.value if r else "kdv"}


@router.post("/invoices", status_code=201)
async def create_invoice(order_id: int, buyer_id: int, seller_id: int, subtotal: float,
                           current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    svc = TaxService(db)
    calc = await svc.calculate_tax(subtotal)
    invoice_no = await svc.generate_invoice_no()
    repo = TaxRepository(db)
    inv = await repo.create_invoice(order_id, invoice_no, buyer_id, seller_id, subtotal, calc["tax_total"], calc["grand_total"])
    await db.commit()
    return {"id": inv.id, "invoice_no": inv.invoice_no, "subtotal": inv.subtotal, "tax_total": inv.tax_total, "grand_total": inv.grand_total}


@router.get("/invoices")
async def list_invoices(as_buyer: bool = True, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = TaxRepository(db)
    return await repo.list_invoices(current_user.id, as_buyer)
