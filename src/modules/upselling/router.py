from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.upselling.service import UpsellingService
from src.modules.upselling.repository import UpsellingRepository
from datetime import date

router = APIRouter(prefix="/upselling", tags=["upselling"])


def get_service(db: AsyncSession = Depends(get_db)) -> UpsellingService:
    return UpsellingService(db)


@router.get("/offers/{hotel_id}")
async def list_offers(hotel_id: int, is_active: bool | None = Query(None), db: AsyncSession = Depends(get_db)):
    repo = UpsellingRepository(db)
    return await repo.list_offers(hotel_id, is_active)


@router.post("/offers", status_code=201)
async def create_offer(offer_data: dict, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    repo = UpsellingRepository(db)
    offer = await repo.offers.create(offer_data)
    await db.commit()
    return {"id": offer.id, "name": offer.name, "category": offer.category}


@router.put("/offers/{offer_id}")
async def update_offer(offer_id: int, offer_data: dict, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    repo = UpsellingRepository(db)
    offer = await repo.offers.update(offer_id, offer_data)
    if not offer:
        raise HTTPException(404, "Offer not found")
    await db.commit()
    return {"id": offer.id, "name": offer.name, "category": offer.category}


@router.delete("/offers/{offer_id}")
async def delete_offer(offer_id: int, current_user: User = Depends(get_current_user),
                       db: AsyncSession = Depends(get_db)):
    repo = UpsellingRepository(db)
    ok = await repo.offers.delete(offer_id)
    if not ok:
        raise HTTPException(404, "Offer not found")
    await db.commit()
    return {"ok": True}


@router.get("/available/{booking_id}")
async def get_available_offers(booking_id: int, trigger_event: str | None = Query(None),
                               db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    try:
        return await service.get_available_offers(booking_id, trigger_event)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/bookings/{booking_id}/add", status_code=201)
async def add_offer_to_booking(booking_id: int, body: dict, current_user: User = Depends(get_current_user),
                               db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    try:
        result = await service.add_upsell_to_booking(booking_id, body["offer_id"], body.get("quantity", 1))
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/items/{item_id}/confirm")
async def confirm_upsell(item_id: int, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    try:
        result = await service.confirm_upsell_item(item_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.put("/items/{item_id}/cancel")
async def cancel_upsell(item_id: int, current_user: User = Depends(get_current_user),
                        db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    try:
        result = await service.cancel_upsell_item(item_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/report/{hotel_id}")
async def get_report(hotel_id: int, report_date: str = Query(...), db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    try:
        dt = date.fromisoformat(report_date)
    except ValueError:
        raise HTTPException(400, "Invalid date format, use YYYY-MM-DD")
    result = await service.generate_ancillary_report(hotel_id, dt)
    await db.commit()
    return result


@router.post("/campaigns", status_code=201)
async def create_campaign(campaign_data: dict, current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    result = await service.create_campaign(campaign_data.pop("hotel_id"), campaign_data)
    await db.commit()
    return result
