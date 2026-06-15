from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.protection.service import ProtectionService

router = APIRouter(prefix="/protection", tags=["protection"])


@router.get("/status")
async def protection_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ProtectionService(db)
    return await svc.buyer_protection_status(current_user.id)


@router.post("/claims", status_code=201)
async def file_claim(
    order_id: int, reason: str, description: str = None, evidence: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ProtectionService(db)
    result, err = await svc.file_claim(current_user.id, order_id, reason, description, evidence)
    if err:
        raise HTTPException(400, err)
    await db.commit()
    return result


@router.get("/claims")
async def my_claims(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = ProtectionService(db)
    return await svc.my_claims(current_user.id)
