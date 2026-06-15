from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.dropshipping.repository import DropshippingRepository

router = APIRouter(prefix="/dropshipping", tags=["dropshipping"])


@router.post("/suppliers", status_code=201)
async def create_supplier(
    name: str, api_url: str = None, api_key: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = DropshippingRepository(db)
    s = await repo.create_supplier(name, api_url, api_key)
    await db.commit()
    return s


@router.get("/suppliers")
async def list_suppliers(db: AsyncSession = Depends(get_db)):
    repo = DropshippingRepository(db)
    return await repo.list_suppliers()


@router.post("/products/link", status_code=201)
async def link_product(
    supplier_id: int, product_id: int, supplier_sku: str = None, cost_price: float = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = DropshippingRepository(db)
    dp = await repo.link_product(supplier_id, product_id, supplier_sku, cost_price)
    await db.commit()
    return dp


@router.get("/products")
async def list_products(db: AsyncSession = Depends(get_db)):
    repo = DropshippingRepository(db)
    return await repo.list_products()
