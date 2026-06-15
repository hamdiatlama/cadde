from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.verification.repository import VerificationRepository

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/{product_id}", status_code=201)
async def request_verification(
    product_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = VerificationRepository(db)
    v = await repo.request_verification(product_id, current_user.id)
    await db.commit()
    return v


@router.put("/{id}")
async def update_verification(
    id: int, status: str, notes: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = VerificationRepository(db)
    v = await repo.update_verification(id, status, notes)
    if not v:
        raise HTTPException(404, "Verification not found")
    await db.commit()
    return v


@router.get("/{product_id}/status")
async def get_status(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = VerificationRepository(db)
    v = await repo.get_status(product_id)
    if not v:
        raise HTTPException(404, "No verification found for this product")
    return v
