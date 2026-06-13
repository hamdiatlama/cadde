from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.store.schemas import ProductCreate, ProductUpdate
from src.modules.store.service import ProductService

router = APIRouter(prefix="/search", tags=["search"])

@router.post("/products", response_model=dict, status_code=201)
async def create_product(
    data: ProductCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ProductService(db)
    product, err = await svc.create_product(data, current_user)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return product

@router.put("/products/{product_id}", response_model=dict)
async def update_product(
    product_id: int, data: ProductUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ProductService(db)
    product, err = await svc.update_product(product_id, data, current_user)
    if err:
        raise HTTPException(status_code=400, detail=err)
    await db.commit()
    return product

@router.get("/products", response_model=dict)
async def search_products(
    q: str = Query(None), category: str = Query(None),
    subcategory: str = Query(None), occasion: str = Query(None),
    min_price: float = Query(None), max_price: float = Query(None),
    color: str = Query(None), seller_id: int = Query(None),
    sort_by: str = Query("created_at"), sort_order: str = Query("desc"),
    page: int = Query(1, ge=1), per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    svc = ProductService(db)
    return await svc.search_products(
        q, category, subcategory, occasion, min_price, max_price,
        color, seller_id, sort_by, sort_order, page, per_page
    )

@router.get("/categories", response_model=dict)
async def get_categories(db: AsyncSession = Depends(get_db)):
    svc = ProductService(db)
    return await svc.get_categories()

@router.get("/products/{product_id}", response_model=dict)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    svc = ProductService(db)
    product = await svc.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
