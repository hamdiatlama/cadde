from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.variant.service import VariantService

router = APIRouter(prefix="/variants", tags=["variants"])


@router.get("/{product_id}")
async def get_variants(product_id: int, db: AsyncSession = Depends(get_db)):
    svc = VariantService(db)
    return await svc.get_variants(product_id)


@router.get("/{product_id}/resolve")
async def resolve_sku(
    product_id: int, option_ids: str = Query(..., description="Comma-separated option IDs"),
    db: AsyncSession = Depends(get_db),
):
    ids = [int(x) for x in option_ids.split(",")]
    svc = VariantService(db)
    result = await svc.get_sku_by_selection(product_id, ids)
    if not result:
        raise HTTPException(404, "No SKU matches these options")
    return result


@router.post("/{product_id}/groups", status_code=201)
async def add_group(
    product_id: int, name: str, sort_order: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only sellers can manage variants")
    svc = VariantService(db)
    result = await svc.add_group(product_id, name, sort_order)
    await db.commit()
    return result


@router.post("/groups/{group_id}/options", status_code=201)
async def add_option(
    group_id: int, value: str, sort_order: int = 0,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = VariantService(db)
    result = await svc.add_option(group_id, value, sort_order)
    await db.commit()
    return result


@router.post("/{product_id}/skus", status_code=201)
async def add_sku(
    product_id: int, sku: str, option_ids: str = Query(...),
    barcode: str = None, price_override: float = None,
    compare_price_override: float = None, stock: int = 0, image_url: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    oids = [int(x) for x in option_ids.split(",")]
    svc = VariantService(db)
    result = await svc.add_sku(product_id, sku, oids, barcode=barcode,
                                price_override=price_override, compare_price_override=compare_price_override,
                                stock=stock, image_url=image_url)
    await db.commit()
    return result
