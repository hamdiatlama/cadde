from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.fulfillment.models import FulfillmentRequest
from src.modules.fulfillment.repository import FulfillmentRepository

router = APIRouter(prefix="/fulfillment", tags=["fulfillment"])


@router.post("/centers", status_code=201)
async def create_center(name: str, address: str = None, city: str = None,
                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    c = await repo.create_center(name, address, city)
    await db.commit()
    return {"id": c.id, "name": c.name}


@router.get("/centers")
async def list_centers(db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    return await repo.list_centers()


@router.post("/requests/{order_id}", status_code=201)
async def create_request(order_id: int, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    fr = await repo.create_request(current_user.id, order_id)
    await db.commit()
    return {"id": fr.id, "status": fr.status}


@router.put("/requests/{id}/assign")
async def assign_center(id: int, center_id: int, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    fr = await repo.assign_center(id, center_id)
    if not fr:
        raise HTTPException(404, "Fulfillment request not found")
    await db.commit()
    return {"id": fr.id, "center_id": fr.center_id}


@router.put("/requests/{id}/status")
async def update_status(id: int, status: str, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    fr = await repo.update_status(id, status)
    if not fr:
        raise HTTPException(404, "Fulfillment request not found")
    await db.commit()
    return {"id": fr.id, "status": fr.status}


@router.get("/requests")
async def list_my_requests(current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    return await repo.list_by_seller(current_user.id)


@router.get("/requests/admin")
async def list_all_requests(center_id: int = None, db: AsyncSession = Depends(get_db)):
    repo = FulfillmentRepository(db)
    if center_id:
        return await repo.list_by_center(center_id)
    from sqlalchemy import select
    r = await db.execute(select(FulfillmentRequest).order_by(FulfillmentRequest.created_at.desc()))
    return r.scalars().all()
