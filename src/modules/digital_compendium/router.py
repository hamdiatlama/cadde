from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from src.database import get_db
from src.core.auth import get_current_user
from src.models.user import User
from src.modules.digital_compendium.service import DigitalCompendiumService
from src.modules.hotel.service import HotelService

router = APIRouter(prefix="/digital-compendium", tags=["digital_compendium"])


class CreateCompendiumBody(BaseModel):
    welcome_message: str | None = None
    wifi_ssid: str | None = None
    wifi_password: str | None = None
    breakfast_info: str | None = None
    restaurant_info: str | None = None
    room_service_info: str | None = None
    spa_info: str | None = None
    gym_info: str | None = None
    parking_info: str | None = None
    house_rules: str | None = None
    emergency_info: str | None = None
    checkout_info: str | None = None
    local_attractions: dict | None = None
    hotel_services: dict | None = None
    contact_info: str | None = None
    is_published: bool = False


class CreatePageBody(BaseModel):
    compendium_id: int
    title: str
    content: str | None = None
    icon: str | None = None
    sort_order: int = 0


class UpdatePageBody(BaseModel):
    title: str | None = None
    content: str | None = None
    icon: str | None = None
    sort_order: int | None = None
    is_active: bool | None = None


class RoomServiceBody(BaseModel):
    booking_id: int
    category: str
    item_name: str
    quantity: int = 1
    notes: str | None = None


def get_service(db: AsyncSession = Depends(get_db)) -> DigitalCompendiumService:
    return DigitalCompendiumService(db)


async def get_hotel_owner_check(hotel_id: int, current_user: User, db: AsyncSession):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only hotel owners can manage compendiums")
    svc = HotelService(db)
    hotel = await svc.get_hotel_by_id(hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    if hotel.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "You do not own this hotel")
    return hotel


@router.post("/create", status_code=201)
async def create_compendium(
    hotel_id: int = Query(...),
    body: CreateCompendiumBody = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    try:
        result = await svc.create_compendium(hotel_id, body.dict(exclude_none=True) if body else {})
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/{compendium_id}")
async def update_compendium(
    compendium_id: int,
    body: CreateCompendiumBody = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    c = await svc.repo.get_compendium(compendium_id)
    if not c:
        raise HTTPException(404, "Compendium not found")
    await get_hotel_owner_check(c.hotel_id, current_user, db)
    try:
        result = await svc.update_compendium(compendium_id, body.dict(exclude_none=True) if body else {})
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/{hotel_id}")
async def get_compendium(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.get_compendium(hotel_id)
    if not result:
        raise HTTPException(404, "Compendium not found")
    return result


@router.get("/guest/{booking_id}")
async def get_guest_compendium(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.get_guest_compendium(booking_id)
        if not result:
            raise HTTPException(404, "Compendium not published")
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/pages/{compendium_id}")
async def list_pages(
    compendium_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    c = await svc.repo.get_compendium(compendium_id)
    if not c:
        raise HTTPException(404, "Compendium not found")
    return await svc.list_pages(compendium_id)


@router.post("/pages", status_code=201)
async def create_page(
    body: CreatePageBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    c = await svc.repo.get_compendium(body.compendium_id)
    if not c:
        raise HTTPException(404, "Compendium not found")
    await get_hotel_owner_check(c.hotel_id, current_user, db)
    result = await svc.create_page(body.compendium_id, body.dict(exclude={"compendium_id"}))
    await db.commit()
    return result


@router.put("/pages/{page_id}")
async def update_page(
    page_id: int,
    body: UpdatePageBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    p = await svc.repo.get_page(page_id)
    if not p:
        raise HTTPException(404, "Page not found")
    c = await svc.repo.get_compendium(p.compendium_id)
    if c:
        await get_hotel_owner_check(c.hotel_id, current_user, db)
    try:
        result = await svc.update_page(page_id, body.dict(exclude_none=True))
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/notify/welcome/{booking_id}", status_code=201)
async def send_welcome_notification(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.send_welcome_notification(booking_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/notify/checkout/{booking_id}", status_code=201)
async def send_checkout_reminder(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.send_checkout_reminder(booking_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/notifications/{booking_id}")
async def list_notifications(
    booking_id: int,
    is_read: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.list_notifications(booking_id, is_read)


@router.post("/room-service", status_code=201)
async def create_room_service(
    body: RoomServiceBody,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.request_room_service(body.booking_id, body.category, body.item_name, body.quantity, body.notes)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/room-service/{hotel_id}")
async def list_room_service_requests(
    hotel_id: int,
    status: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.list_room_service_requests(hotel_id, status)


@router.put("/room-service/{request_id}/status")
async def update_room_service_status(
    request_id: int,
    status: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    try:
        result = await svc.update_room_service_status(request_id, status)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(400, str(e))
