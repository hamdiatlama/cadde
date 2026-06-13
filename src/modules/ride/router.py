import uuid

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.ride.service import RideService
from src.modules.ride.repository import RideRepository
from src.modules.ride.websocket_manager import manager as ws_manager
from src.modules.ride.models import Driver, Ride
from src.modules.ride.schemas import (
    RideCreateRequest, RideResponse, DriverLocationUpdate,
    SafetyConfirmRequest, EmergencyContactRequest,
    IncidentReportRequest, RideRatingRequest,
    DriverRegisterRequest, DriverResponse, RideSafetyResponse,
    SpoofingStatus,
)

router = APIRouter(prefix="/rides", tags=["rides"])


async def get_driver_or_404(user: User, db: AsyncSession) -> Driver:
    repo = RideRepository(db)
    driver = await repo.get_driver_by_user_id(user.id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found. Register as a driver first.")
    return driver


def get_service(db: AsyncSession = Depends(get_db)) -> RideService:
    return RideService(db)


# ─── WebSocket: Canli Surucu Takibi ──────────────────────────────

@router.websocket("/track/{ride_id}")
async def ride_track_websocket(websocket: WebSocket, ride_id: int, client_id: str = None):
    if not client_id:
        client_id = str(uuid.uuid4())[:8]
    await ws_manager.connect(ride_id, client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text('{"type":"pong"}')
            elif data.startswith("ping:"):
                await websocket.send_text(f'{{"type":"pong","seq":{data.split(":")[1]}}}')
    except WebSocketDisconnect:
        ws_manager.disconnect(ride_id, client_id)


# ─── 1) Cagir (Fiyat kitlenir, surge belli olur) ────────────────

@router.post("/", response_model=RideResponse, status_code=201)
async def create_ride(
    data: RideCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    ride = await service.create_ride(current_user.id, data)
    await db.commit()
    await db.refresh(ride)
    return RideResponse.model_validate(ride)


# ─── 2) Surucu Kabul ────────────────────────────────────────────

@router.post("/{ride_id}/accept", response_model=RideResponse)
async def accept_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can accept rides")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    try:
        ride = await service.accept_ride(ride_id, driver)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── 2) Surucu Red (iptal cezasi mekanizmasi) ──────────────────

@router.post("/{ride_id}/reject", response_model=RideResponse)
async def reject_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can reject rides")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    try:
        ride = await service.reject_ride(ride_id, driver)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── 3) Guvenlik: Plaka / foto dogrulama ──────────────────────

@router.post("/{ride_id}/safety/confirm", response_model=dict)
async def confirm_safety(
    ride_id: int,
    data: SafetyConfirmRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        result = await service.confirm_safety(ride_id, current_user.id, data.plate_confirmed, data.photo_confirmed)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 3) Guvenlik: Acil durum kisisini ekle ────────────────────

@router.post("/{ride_id}/safety/emergency-contact", response_model=dict)
async def set_emergency_contact(
    ride_id: int,
    data: EmergencyContactRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        result = await service.set_emergency_contact(ride_id, current_user.id, data.phone)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 3) Guvenlik: Olay bildirimi ──────────────────────────────

@router.post("/{ride_id}/safety/report-incident", response_model=dict)
async def report_incident(
    ride_id: int,
    data: IncidentReportRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        result = await service.report_incident(ride_id, current_user.id, data.incident_type, data.description)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 3) Guvenlik: Yolculuk paylasma linki ─────────────────────

@router.post("/{ride_id}/safety/share", response_model=dict)
async def share_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        result = await service.share_ride(ride_id, current_user.id)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 4) Surucu Vardi ──────────────────────────────────────────

@router.post("/{ride_id}/arrived", response_model=RideResponse)
async def driver_arrived(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can mark arrival")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    try:
        ride = await service.driver_arrived(ride_id, driver)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 5) Baslat ──────────────────────────────────────────────────

@router.post("/{ride_id}/start", response_model=RideResponse)
async def start_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can start rides")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    try:
        ride = await service.start_ride(ride_id, driver)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 6) Tamamla (rota dogrulama + fiyat kesinlesir) ───────────

@router.post("/{ride_id}/complete", response_model=RideResponse)
async def complete_ride(
    ride_id: int,
    actual_latitude: float = Query(None),
    actual_longitude: float = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can complete rides")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    try:
        ride = await service.complete_ride(ride_id, driver, actual_latitude, actual_longitude)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── 7) Iptal (musteri) ──────────────────────────────────────

@router.post("/{ride_id}/cancel", response_model=RideResponse)
async def cancel_ride(
    ride_id: int,
    reason: str = "Iptal edildi",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        ride = await service.cancel_ride(ride_id, current_user.id, reason)
        await db.commit()
        await db.refresh(ride)
        return RideResponse.model_validate(ride)
    except ValueError as e:
        raise HTTPException(status_code=404 if "not found" in str(e).lower() else 400, detail=str(e))


# ─── 8) Surucuyu degerlendir ─────────────────────────────────

@router.post("/{ride_id}/rate", response_model=dict)
async def rate_ride(
    ride_id: int,
    data: RideRatingRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = RideService(db)
    try:
        result = await service.rate_ride(ride_id, current_user.id, data.rating, data.comment, data.categories)
        await db.commit()
        return result
    except ValueError as e:
        raise HTTPException(status_code=400 if "already" in str(e).lower() else 404, detail=str(e))


# ─── 9) Surucu ceza durumunu sifirla (admin) ──────────────────

@router.post("/driver/{driver_id}/reset-penalty", response_model=dict)
async def reset_driver_penalty(
    driver_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    repo = RideRepository(db)
    driver = await repo.get_driver_by_id(driver_id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    await repo.reset_penalty(driver)
    await db.commit()
    return {"status": "penalty_reset"}


# ─── 10) Surucu kayit ─────────────────────────────────────────

@router.post("/driver/register", response_model=dict)
async def register_driver(
    data: DriverRegisterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RideRepository(db)
    existing = await repo.get_driver_by_user_id(current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="You are already registered as a driver")

    driver = Driver(
        user_id=current_user.id,
        license_plate=data.license_plate,
        vehicle_model=data.vehicle_model,
        vehicle_color=data.vehicle_color,
    )
    db.add(driver)
    await db.commit()
    return {"status": "driver_registered", "license_plate": data.license_plate}


# ─── 11) Surucu konum guncelle (GPS spoofing ile) ────────────

@router.post("/driver/location", response_model=dict)
async def update_driver_location(
    data: DriverLocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can update location")

    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    result = await service.update_driver_location(
        driver,
        data.latitude, data.longitude,
        data.speed_kmh, data.heading, data.accuracy_m,
        source=data.source,
    )

    # Broadcast to all watchers of this driver's active rides
    active_rides = await db.execute(
        select(Ride).where(
            Ride.driver_id == driver.id,
            Ride.status.in_(["accepted", "arrived", "in_progress"]),
        )
    )
    for ride in active_rides.scalars().all():
        await ws_manager.broadcast_location(
            ride.id, driver.id,
            data.latitude, data.longitude,
            data.speed_kmh, data.heading,
        )

    await db.commit()
    return result


# ─── 12) GPS Spoofing Durumu ─────────────────────────────────

@router.get("/driver/spoofing-status", response_model=SpoofingStatus)
async def get_spoofing_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers")
    driver = await get_driver_or_404(current_user, db)
    service = RideService(db)
    result = await service.get_spoofing_status(driver)
    return SpoofingStatus(**result)


# ─── Sorgulamalar ───────────────────────────────────────────────

@router.get("/", response_model=list[RideResponse])
async def list_my_rides(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RideRepository(db)
    rides = await repo.get_customer_rides(current_user.id)
    return [RideResponse.model_validate(r) for r in rides]


@router.get("/driver/pending", response_model=list[RideResponse])
async def pending_rides(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can view pending rides")
    repo = RideRepository(db)
    rides = await repo.get_pending_rides()
    return [RideResponse.model_validate(r) for r in rides]


@router.get("/driver/history", response_model=list[RideResponse])
async def driver_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("driver", "admin"):
        raise HTTPException(status_code=403, detail="Only drivers can view ride history")
    driver = await get_driver_or_404(current_user, db)
    repo = RideRepository(db)
    rides = await repo.get_driver_rides(driver.id)
    return [RideResponse.model_validate(r) for r in rides]


@router.get("/{ride_id}", response_model=RideResponse)
async def get_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RideRepository(db)
    ride = await repo.get_ride_by_id(ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    if ride.customer_id != current_user.id:
        driver = await repo.get_driver_by_user_id(current_user.id)
        if not driver or ride.driver_id != driver.id:
            raise HTTPException(status_code=404, detail="Ride not found")

    resp = RideResponse.model_validate(ride)
    if ride.driver_id:
        d = await repo.get_driver_by_id(ride.driver_id)
        if d:
            u_result = await db.execute(select(User).where(User.id == d.user_id))
            u = u_result.scalar_one_or_none()
            if u:
                resp.driver_name = u.full_name
            resp.driver_plate = d.license_plate
            resp.driver_vehicle = f"{d.vehicle_model} ({d.vehicle_color})" if d.vehicle_model else None
    return resp


# ─── Surucu Profili ─────────────────────────────────────────────

@router.get("/driver/me", response_model=DriverResponse)
async def get_my_driver_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = RideRepository(db)
    driver = await repo.get_driver_by_user_id(current_user.id)
    if not driver:
        raise HTTPException(status_code=404, detail="Driver profile not found")
    return DriverResponse.model_validate(driver)
