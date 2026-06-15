from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.comparison.service import ComparisonService

router = APIRouter(prefix="/compare", tags=["comparison"])


@router.get("/")
async def get_comparison(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ComparisonService(db)
    return await svc.get_comparison(current_user.id)


@router.post("/{product_id}", status_code=201)
async def add_to_comparison(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ComparisonService(db)
    result, err = await svc.add_product(current_user.id, product_id)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.delete("/{product_id}")
async def remove_from_comparison(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ComparisonService(db)
    await svc.remove_product(current_user.id, product_id)
    await db.commit()
    return {"ok": True}
