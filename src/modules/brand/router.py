from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.brand.repository import BrandRepository

router = APIRouter(prefix="/brands", tags=["brands"])


@router.post("/", status_code=201)
async def create_brand(
    name: str, trademark_no: str = None, logo_url: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BrandRepository(db)
    b = await repo.create_brand(name, current_user.id, trademark_no, logo_url)
    await db.commit()
    return b


@router.get("/")
async def list_brands(db: AsyncSession = Depends(get_db)):
    repo = BrandRepository(db)
    return await repo.list_brands()


@router.get("/{id}")
async def get_brand(id: int, db: AsyncSession = Depends(get_db)):
    repo = BrandRepository(db)
    b = await repo.get_brand(id)
    if not b:
        raise HTTPException(404, "Brand not found")
    return b


@router.put("/{id}")
async def update_brand(
    id: int, name: str = None, trademark_no: str = None, logo_url: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = BrandRepository(db)
    kwargs = {k: v for k, v in {"name": name, "trademark_no": trademark_no, "logo_url": logo_url}.items() if v is not None}
    b = await repo.update_brand(id, **kwargs)
    if not b:
        raise HTTPException(404, "Brand not found")
    await db.commit()
    return b
