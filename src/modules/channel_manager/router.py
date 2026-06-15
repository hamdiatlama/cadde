from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.channel_manager.service import ChannelManagerService

router = APIRouter(prefix="/channel-manager", tags=["channel_manager"])


def get_service(db: AsyncSession = Depends(get_db)) -> ChannelManagerService:
    return ChannelManagerService(db)


@router.get("/channels")
async def list_ota_channels(db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    return await service.list_channels()


@router.post("/connect", status_code=201)
async def connect_ota(
    hotel_id: int = Query(...),
    ota_channel_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.connect_ota(hotel_id, ota_channel_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/disconnect/{connection_id}")
async def disconnect_ota(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.disconnect_ota(connection_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/connections/{hotel_id}")
async def list_connections(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_connections(hotel_id)


@router.get("/listings/{hotel_id}")
async def list_listings(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_listings(hotel_id)


@router.post("/sync/availability/{connection_id}")
async def sync_availability(
    connection_id: int,
    date_from: str = Query(None),
    date_to: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.sync_availability(connection_id, date_from, date_to)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/sync/rates/{connection_id}")
async def sync_rates(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.sync_rates(connection_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.post("/sync/bookings/{connection_id}")
async def import_ota_bookings(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    try:
        result = await service.import_ota_bookings(connection_id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/bookings/{hotel_id}")
async def list_ota_bookings(
    hotel_id: int,
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_ota_bookings(hotel_id, status)


@router.get("/analytics/{hotel_id}")
async def get_channel_analytics(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.get_channel_analytics(hotel_id)


@router.get("/sync-logs/{connection_id}")
async def list_sync_logs(
    connection_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_sync_logs(connection_id)
