"""Courier API endpoints.

Implements the full courier lifecycle per the project prompt:
- Location updates with GPS spoofing detection
- Real-time tracking via WebSocket broadcast
- Nearby courier search with proper geo math
- Race-condition-safe courier assignment
- Shift management (mesai baslat/bitir)
- Earnings tracking
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.courier.service import CourierService
from src.modules.courier.repository import CourierRepository
from src.modules.courier.websocket_manager import manager as ws_manager
from src.modules.courier.schemas import (
    LocationUpdate, CourierResponse, CourierNearbyResponse,
    TrackResponse, AssignResponse, DeliverResponse,
    ShiftStartResponse, ShiftEndResponse, EarningsResponse,
    SpoofingStatus, LocationHistoryResponse,
)
from src.modules.courier.models import Courier

router = APIRouter(prefix="/courier", tags=["courier"])


async def get_courier_or_404(user: User, db: AsyncSession) -> Courier:
    repo = CourierRepository(db)
    courier = await repo.get_by_user_id(user.id)
    if not courier:
        courier = await repo.create_or_update(user.id)
    return courier


def get_service(db: AsyncSession = Depends(get_db)) -> CourierService:
    return CourierService(db)


# ─── WebSocket: Canli Takip ──────────────────────────────────────

@router.websocket("/track/{order_id}")
async def courier_track_websocket(websocket: WebSocket, order_id: int, client_id: str = None):
    if not client_id:
        client_id = str(uuid.uuid4())[:8]
    await ws_manager.connect(order_id, client_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_text('{"type":"pong"}')
            elif data.startswith("ping:"):
                await websocket.send_text(f'{{"type":"pong","seq":{data.split(":")[1]}}}')
    except WebSocketDisconnect:
        ws_manager.disconnect(order_id, client_id)


# ─── Konum Guncelleme ───────────────────────────────────────────

@router.post("/location", response_model=dict)
async def update_courier_location(
    data: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler konum guncelleyebilir")

    courier = await get_courier_or_404(current_user, db)
    service = CourierService(db)
    result = await service.update_location(
        courier,
        data.latitude, data.longitude,
        data.speed_kmh, data.heading, data.accuracy_m,
        source=data.source,
    )

    # Broadcast to all watchers of this courier's active orders
    from src.models.order import Order as OrderModel
    orders_r = await db.execute(
        select(OrderModel)
        .where(
            OrderModel.courier_id == current_user.id,
            OrderModel.status.in_(["in_transit", "preparing"]),
        )
    )
    for order in orders_r.scalars().all():
        await ws_manager.broadcast_location(
            order.id, courier.id,
            data.latitude, data.longitude,
            data.speed_kmh, data.heading,
        )

    await db.commit()
    return result


# ─── Kurye Takip (HTTP) ─────────────────────────────────────────

@router.get("/track/{order_id}", response_model=TrackResponse)
async def get_courier_location(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = CourierService(db)
    try:
        result = await service.get_tracking(order_id)
        return TrackResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── Kurye Ata ──────────────────────────────────────────────────

@router.post("/{order_id}/assign", response_model=AssignResponse)
async def assign_courier(
    order_id: int,
    db: AsyncSession = Depends(get_db),
):
    service = CourierService(db)
    try:
        result = await service.assign_courier(order_id)
        await db.commit()
        return AssignResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404 if "bulunamadi" in str(e) else 400, detail=str(e))


# ─── Teslim Et ──────────────────────────────────────────────────

@router.post("/{order_id}/deliver", response_model=DeliverResponse)
async def mark_delivered(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler teslimat yapabilir")

    service = CourierService(db)
    try:
        result = await service.complete_delivery(order_id, current_user.id)
        await db.commit()
        return DeliverResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# ─── Yakindaki Kuryeler ─────────────────────────────────────────

@router.get("/nearby", response_model=list[CourierNearbyResponse])
async def get_nearby_couriers(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(5, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    service = CourierService(db)
    results = await service.find_nearby(latitude, longitude, radius_km)
    return [CourierNearbyResponse(**r) for r in results]


# ─── Kurye Bilgisi ──────────────────────────────────────────────

@router.get("/me", response_model=CourierResponse)
async def get_my_courier_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    repo = CourierRepository(db)
    courier = await repo.get_by_user_id(current_user.id)
    if not courier:
        raise HTTPException(status_code=404, detail="Kurye profili bulunamadi")
    return CourierResponse.model_validate(courier)


# ─── Mesai Baslat ───────────────────────────────────────────────

@router.post("/shift/start", response_model=ShiftStartResponse)
async def start_shift(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler mesai baslatabilir")

    courier = await get_courier_or_404(current_user, db)
    service = CourierService(db)
    try:
        result = await service.start_shift(courier)
        await db.commit()
        return ShiftStartResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Mesai Bitir ────────────────────────────────────────────────

@router.post("/shift/end", response_model=ShiftEndResponse)
async def end_shift(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler mesai bitirebilir")

    courier = await get_courier_or_404(current_user, db)
    service = CourierService(db)
    try:
        result = await service.end_shift(courier)
        await db.commit()
        return ShiftEndResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Kazanc ──────────────────────────────────────────────────────

@router.get("/earnings", response_model=EarningsResponse)
async def get_earnings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler kazanc gorebilir")

    courier = await get_courier_or_404(current_user, db)
    service = CourierService(db)
    result = await service.get_earnings(courier)
    return EarningsResponse(**result)


# ─── GPS Spoofing Durumu ───────────────────────────────────────

@router.get("/spoofing-status", response_model=SpoofingStatus)
async def get_spoofing_status(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kuryeler")

    courier = await get_courier_or_404(current_user, db)
    service = CourierService(db)
    result = await service.get_spoofing_status(courier)
    return SpoofingStatus(**result)


# ─── Kurye Kayit ────────────────────────────────────────────────

@router.post("/register", response_model=CourierResponse)
async def register_courier(
    vehicle_type: str = Query("motorcycle"),
    vehicle_plate: str = Query(None),
    max_load_kg: float = Query(50),
    service_zone: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("courier", "admin"):
        raise HTTPException(status_code=403, detail="Sadece kurye rolundeki kullanicilar kayit olabilir")

    repo = CourierRepository(db)
    existing = await repo.get_by_user_id(current_user.id)
    if existing:
        existing.vehicle_type = vehicle_type
        if vehicle_plate:
            existing.vehicle_plate = vehicle_plate
        if max_load_kg:
            existing.max_load_kg = max_load_kg
        if service_zone:
            existing.service_zone = service_zone
        courier = existing
    else:
        courier = Courier(
            user_id=current_user.id,
            vehicle_type=vehicle_type,
            vehicle_plate=vehicle_plate,
            max_load_kg=max_load_kg,
            service_zone=service_zone,
        )
        db.add(courier)

    await db.commit()
    await db.refresh(courier)
    return CourierResponse.model_validate(courier)
