from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.core.auth import get_current_user
from src.modules.user.models import User
from src.modules.food_supplier.schemas import (
    SupplierCreate, SupplierUpdate, SupplierResponse, SupplierPageResponse,
    ProductCreate, ProductUpdate, ProductResponse,
    LinkSupplier, SupplierLinkResponse,
    IngredientCreate, IngredientUpdate, IngredientResponse,
    TransparencyScoreResponse, TraceResponse,
)
from src.modules.food_supplier.service import FoodSupplierService

router = APIRouter(prefix="/food", tags=["food-supplier"])


def _svc(db: AsyncSession = Depends(get_db)) -> FoodSupplierService:
    return FoodSupplierService(db)


# --- Supplier CRUD ---

@router.post("/suppliers", response_model=SupplierResponse)
async def register_supplier(
    data: SupplierCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    sup = await svc.register(user.id, data)
    await db.commit()
    return sup


@router.put("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def update_supplier(
    supplier_id: int,
    data: SupplierUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    sup = await svc.update(supplier_id, data, user.id)
    if not sup:
        raise HTTPException(404, "Supplier not found or access denied")
    await db.commit()
    return sup


@router.get("/suppliers", response_model=list[SupplierResponse])
async def list_suppliers(
    city: str = None,
    organic: bool = False,
    halal: bool = False,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    return await svc.list_suppliers(city, organic, halal)


@router.get("/suppliers/{supplier_id}", response_model=SupplierResponse)
async def get_supplier(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    sup = await svc.get_supplier(supplier_id)
    if not sup:
        raise HTTPException(404, "Supplier not found")
    return sup


# --- Supplier Products ---

@router.post("/suppliers/{supplier_id}/products", response_model=ProductResponse)
async def add_product(
    supplier_id: int,
    data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    prod = await svc.add_product(supplier_id, data, user.id)
    if not prod:
        raise HTTPException(404, "Supplier not found or access denied")
    await db.commit()
    return prod


@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    prod = await svc.update_product(product_id, data, user.id)
    if not prod:
        raise HTTPException(404, "Product not found or access denied")
    await db.commit()
    return prod


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    ok = await svc.delete_product(product_id, user.id)
    if not ok:
        raise HTTPException(404, "Product not found or access denied")
    await db.commit()
    return {"ok": True}


@router.get("/suppliers/{supplier_id}/products", response_model=list[ProductResponse])
async def list_products(
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    return await svc.list_products(supplier_id)


# --- Public Supplier Page ---

@router.get("/suppliers/page/{slug}", response_model=SupplierPageResponse)
async def supplier_page(slug: str, db: AsyncSession = Depends(get_db)):
    svc = FoodSupplierService(db)
    page = await svc.get_supplier_page(slug)
    if not page:
        raise HTTPException(404, "Supplier not found")
    return page


# --- Restaurant-Supplier Links ---

@router.post("/restaurants/{rest_id}/suppliers", response_model=SupplierLinkResponse)
async def link_supplier(
    rest_id: int,
    data: LinkSupplier,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    link = await svc.link_supplier(rest_id, data.supplier_id, data, user.id)
    if not link:
        raise HTTPException(400, "Cannot link supplier to restaurant")
    await db.commit()
    sup = await svc.get_supplier(data.supplier_id)
    return {
        "id": link.id,
        "restaurant_id": link.restaurant_id,
        "supplier_id": link.supplier_id,
        "supplier_name": sup.company_name if sup else "",
        "is_preferred": link.is_preferred,
        "contract_start": link.contract_start,
        "contract_end": link.contract_end,
        "notes": link.notes,
    }


@router.delete("/restaurants/{rest_id}/suppliers/{supplier_id}")
async def unlink_supplier(
    rest_id: int,
    supplier_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    ok = await svc.unlink_supplier(rest_id, supplier_id, user.id)
    if not ok:
        raise HTTPException(404, "Supplier link not found")
    await db.commit()
    return {"ok": True}


@router.get("/restaurants/{rest_id}/suppliers", response_model=list[SupplierLinkResponse])
async def list_restaurant_suppliers(
    rest_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    return await svc.list_restaurant_suppliers(rest_id)


# --- Menu Item Ingredients ---

@router.post("/menu/{item_id}/ingredients", response_model=IngredientResponse)
async def add_ingredient(
    item_id: int,
    data: IngredientCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    ing = await svc.add_ingredient(item_id, data)
    if not ing:
        raise HTTPException(400, "Cannot add ingredient")
    await db.commit()
    ings = await svc.list_ingredients(item_id)
    for i in ings:
        if i["id"] == ing.id:
            return i
    raise HTTPException(500, "Unexpected error")


@router.put("/ingredients/{ingredient_id}", response_model=IngredientResponse)
async def update_ingredient(
    ingredient_id: int,
    data: IngredientUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    ing = await svc.update_ingredient(ingredient_id, data)
    if not ing:
        raise HTTPException(404, "Ingredient not found")
    await db.commit()
    ings = await svc.list_ingredients(ing.menu_item_id)
    for i in ings:
        if i["id"] == ing.id:
            return i
    raise HTTPException(500, "Unexpected error")


@router.delete("/ingredients/{ingredient_id}")
async def delete_ingredient(
    ingredient_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    ok = await svc.delete_ingredient(ingredient_id)
    if not ok:
        raise HTTPException(404, "Ingredient not found")
    await db.commit()
    return {"ok": True}


@router.get("/menu/{item_id}/ingredients", response_model=list[IngredientResponse])
async def list_ingredients(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    return await svc.list_ingredients(item_id)


# --- Transparency Score ---

@router.get("/restaurants/{rest_id}/transparency", response_model=TransparencyScoreResponse)
async def get_transparency_score(
    rest_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    score = await svc.get_score(rest_id)
    if not score:
        raise HTTPException(404, "Transparency score not calculated yet")
    return score


@router.post("/restaurants/{rest_id}/transparency/recalculate", response_model=TransparencyScoreResponse)
async def recalculate_transparency(
    rest_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = FoodSupplierService(db)
    score = await svc.calculate_score(rest_id)
    await db.commit()
    return score


# --- Public Traceability ---

@router.get("/trace/{item_id}", response_model=TraceResponse)
async def trace_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    svc = FoodSupplierService(db)
    trace = await svc.get_trace(item_id)
    if not trace:
        raise HTTPException(404, "Menu item not found")
    return trace
