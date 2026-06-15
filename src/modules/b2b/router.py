from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.b2b.repository import B2bRepository

router = APIRouter(prefix="/b2b", tags=["b2b"])


@router.get("/price-tiers/{product_id}")
async def get_price_tiers(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    return await repo.list_price_tiers(product_id)


@router.post("/price-tiers", status_code=201)
async def create_price_tier(product_id: int, min_qty: int, unit_price: float, max_qty: int = None,
                              current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    t = await repo.create_price_tier(product_id, min_qty, unit_price, max_qty)
    await db.commit()
    return {"id": t.id, "min_qty": t.min_qty, "unit_price": t.unit_price}


@router.get("/price/{product_id}/{qty}")
async def get_b2b_price(product_id: int, qty: int, db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    tier = await repo.get_price_tier(product_id, qty)
    if not tier:
        raise HTTPException(404, "No tier found for this quantity")
    return {"product_id": product_id, "quantity": qty, "unit_price": tier.unit_price, "total": round(tier.unit_price * qty, 2)}


@router.post("/customer", status_code=201)
async def register_b2b_customer(company_name: str, tax_office: str = None, tax_number: str = None,
                                  current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    c = await repo.get_or_create_customer(current_user.id, company_name, tax_office, tax_number)
    await db.commit()
    return {"id": c.id, "company_name": c.company_name, "is_approved": c.is_approved}


@router.post("/quotes", status_code=201)
async def request_quote(seller_id: int, items: list[dict], notes: str = None,
                         current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    customer = await repo.get_or_create_customer(current_user.id)
    if not customer.is_approved:
        raise HTTPException(403, "B2B account not approved yet")
    quote = await repo.create_quote(customer.id, seller_id, notes)
    total = 0
    for item in items:
        tier = await repo.get_price_tier(item["product_id"], item["quantity"])
        unit_price = tier.unit_price if tier else item.get("unit_price", 0)
        await repo.add_quote_item(quote.id, item["product_id"], item["quantity"], unit_price)
        total += unit_price * item["quantity"]
    quote.total_amount = round(total, 2)
    await db.commit()
    return {"id": quote.id, "total_amount": quote.total_amount, "status": quote.status}


@router.get("/quotes")
async def list_quotes(seller_id: int = None, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = B2bRepository(db)
    return await repo.list_quotes(seller_id=seller_id, customer_id=current_user.id if current_user.role == "user" else None)
