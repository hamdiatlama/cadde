from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.database import get_db
from src.core.auth import get_current_user
from src.modules.mobile_checkin import service as checkin_service
from src.modules.mobile_checkin import repository as repo
from src.models.user import User

router = APIRouter(prefix="/mobile-checkin", tags=["mobile_checkin"])


class StartCheckinRequest(BaseModel):
    booking_id: int
    checkin_data: dict = {}


class EarlyCheckinRequest(BaseModel):
    booking_id: int
    requested_time: str


class LateCheckoutRequest(BaseModel):
    booking_id: int
    requested_time: str


@router.post("/start")
async def start_checkin(body: StartCheckinRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.start_mobile_checkin(db, body.booking_id, body.checkin_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/verify/{checkin_id}")
async def verify_guest(checkin_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.verify_guest(db, checkin_id, current_user.id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete/{checkin_id}")
async def complete_checkin(checkin_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.complete_checkin(db, checkin_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/checkout/{booking_id}")
async def checkout_booking(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.check_out(db, booking_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/keys/my")
async def list_my_keys(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    keys = await checkin_service.get_guest_keys(db, current_user.id)
    return {"keys": keys}


@router.get("/keys/{booking_id}")
async def list_booking_keys(booking_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    keys = await repo.get_booking_keys(db, booking_id)
    return {
        "keys": [
            {
                "id": k.id,
                "key_code": k.key_code,
                "status": k.status,
                "valid_from": k.valid_from.isoformat(),
                "valid_until": k.valid_until.isoformat(),
                "issued_at": k.issued_at.isoformat(),
            }
            for k in keys
        ]
    }


@router.post("/keys/{key_id}/revoke")
async def revoke_key(key_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    key = await repo.revoke_key(db, key_id)
    if not key:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key_id": key.id, "status": key.status, "message": "Key revoked"}


@router.post("/early-checkin")
async def request_early_checkin(body: EarlyCheckinRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.request_early_checkin(db, body.booking_id, body.requested_time)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/late-checkout")
async def request_late_checkout(body: LateCheckoutRequest, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        result = await checkin_service.request_late_checkout(db, body.booking_id, body.requested_time)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/requests/{hotel_id}")
async def list_checkin_requests(hotel_id: int, status: str = None, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    checkins = await repo.list_checkins(db, hotel_id, status)
    return {
        "checkins": [
            {
                "id": c.id,
                "booking_id": c.booking_id,
                "guest_id": c.guest_id,
                "status": c.status,
                "id_verified": c.id_verified,
                "checked_in_at": c.checked_in_at.isoformat() if c.checked_in_at else None,
                "created_at": c.created_at.isoformat(),
            }
            for c in checkins
        ]
    }
