from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.account.address.service import AddressService
from src.modules.account.address.schemas import AddressCreate, AddressUpdate

router = APIRouter(prefix="/addresses", tags=["addresses"])

@router.get("", response_model=list[dict])
async def list_addresses(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AddressService(db)
    addrs = await svc.list_addresses(current_user.id)
    return [{
        "id": a.id, "label": a.label, "full_name": a.full_name,
        "phone": a.phone, "address_line": a.address_line,
        "city": a.city, "district": a.district,
        "neighborhood": a.neighborhood,
        "latitude": a.latitude, "longitude": a.longitude,
        "is_default": a.is_default,
    } for a in addrs]

@router.post("", response_model=dict, status_code=201)
async def create_address(
    data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AddressService(db)
    addr = await svc.create_address(current_user.id, data)
    await db.commit()
    return {"status": "created", "id": addr.id}

@router.put("/{addr_id}", response_model=dict)
async def update_address(
    addr_id: int,
    data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AddressService(db)
    addr = await svc.update_address(addr_id, current_user.id, data)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.commit()
    return {"status": "updated"}

@router.delete("/{addr_id}", response_model=dict)
async def delete_address(
    addr_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AddressService(db)
    addr = await svc.delete_address(addr_id, current_user.id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.commit()
    return {"status": "deleted"}

@router.put("/{addr_id}/default", response_model=dict)
async def set_default_address(
    addr_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = AddressService(db)
    addr = await svc.set_default(addr_id, current_user.id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    await db.commit()
    return {"status": "set_default"}
