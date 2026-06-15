from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.iot_manager.service import IotService
from src.modules.hotel.service import HotelService

router = APIRouter(prefix="/iot-manager", tags=["iot_manager"])


def get_service(db: AsyncSession = Depends(get_db)) -> IotService:
    return IotService(db)


async def get_hotel_owner_check(hotel_id: int, current_user: User, db: AsyncSession):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only property owners can manage")
    svc = HotelService(db)
    hotel = await svc.repo.get_hotel(hotel_id)
    if not hotel:
        raise HTTPException(404, "Property not found")
    if hotel.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "You do not own this property")
    return hotel


# ═══════════════════════════════════════════════════════════════════
# Devices
# ═══════════════════════════════════════════════════════════════════


@router.get("/devices/{hotel_id}")
async def list_devices(
    hotel_id: int,
    device_type: str = Query(None),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.list_devices(hotel_id, device_type, status)


@router.post("/devices", status_code=201)
async def register_device(
    hotel_id: int = Query(...),
    device_type: str = Query(...),
    device_name: str = Query(None),
    room_number: str = Query(None),
    room_type_id: int = Query(None),
    manufacturer: str = Query(None),
    model: str = Query(None),
    serial_number: str = Query(...),
    ip_address: str = Query(None),
    mac_address: str = Query(None),
    firmware_version: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.register_device(hotel_id, {
        "device_type": device_type,
        "device_name": device_name,
        "room_number": room_number,
        "room_type_id": room_type_id,
        "manufacturer": manufacturer,
        "model": model,
        "serial_number": serial_number,
        "ip_address": ip_address,
        "mac_address": mac_address,
        "firmware_version": firmware_version,
    })
    await db.commit()
    return result


@router.put("/devices/{device_id}")
async def update_device(
    device_id: int,
    device_name: str = Query(None),
    room_number: str = Query(None),
    room_type_id: int = Query(None),
    ip_address: str = Query(None),
    firmware_version: str = Query(None),
    status: str = Query(None),
    is_active: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    device = await svc.repo.get_device(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    await get_hotel_owner_check(device.hotel_id, current_user, db)
    update_data = {k: v for k, v in {
        "device_name": device_name, "room_number": room_number,
        "room_type_id": room_type_id, "ip_address": ip_address,
        "firmware_version": firmware_version, "status": status,
        "is_active": is_active,
    }.items() if v is not None}
    result = await svc.update_device(device_id, update_data)
    await db.commit()
    return result


@router.delete("/devices/{device_id}", status_code=204)
async def delete_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    device = await svc.repo.get_device(device_id)
    if not device:
        raise HTTPException(404, "Device not found")
    await get_hotel_owner_check(device.hotel_id, current_user, db)
    await svc.remove_device(device_id)
    await db.commit()


@router.post("/devices/{device_id}/command", status_code=201)
async def send_command(
    device_id: int,
    command_type: str = Query(...),
    command_value: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.send_command(device_id, command_type, command_value, current_user.id)
    await db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════
# Automation Rules
# ═══════════════════════════════════════════════════════════════════


@router.get("/rules/{hotel_id}")
async def list_rules(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.list_rules(hotel_id)


@router.post("/rules", status_code=201)
async def create_rule(
    hotel_id: int = Query(...),
    name: str = Query(...),
    trigger_event: str = Query(...),
    conditions: str = Query(None),
    actions: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    import json
    conditions_json = json.loads(conditions) if conditions else None
    actions_json = json.loads(actions) if actions else None
    result = await svc.create_rule(hotel_id, {
        "name": name, "trigger_event": trigger_event,
        "conditions": conditions_json, "actions": actions_json,
    })
    await db.commit()
    return result


@router.put("/rules/{rule_id}")
async def update_rule(
    rule_id: int,
    name: str = Query(None),
    trigger_event: str = Query(None),
    conditions: str = Query(None),
    actions: str = Query(None),
    is_active: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    rule = await svc.repo.get_rule(rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    await get_hotel_owner_check(rule.hotel_id, current_user, db)
    import json
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if trigger_event is not None:
        update_data["trigger_event"] = trigger_event
    if conditions is not None:
        update_data["conditions"] = json.loads(conditions)
    if actions is not None:
        update_data["actions"] = json.loads(actions)
    if is_active is not None:
        update_data["is_active"] = is_active
    result = await svc.update_rule(rule_id, update_data)
    await db.commit()
    return result


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_rule(
    rule_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    rule = await svc.repo.get_rule(rule_id)
    if not rule:
        raise HTTPException(404, "Rule not found")
    await get_hotel_owner_check(rule.hotel_id, current_user, db)
    await svc.delete_rule(rule_id)
    await db.commit()


# ═══════════════════════════════════════════════════════════════════
# Environment Data
# ═══════════════════════════════════════════════════════════════════


@router.get("/environment/{hotel_id}")
async def get_environment(
    hotel_id: int,
    room_number: str = Query(None),
    date: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.get_environment(hotel_id, room_number, date)


# ═══════════════════════════════════════════════════════════════════
# Dashboard
# ═══════════════════════════════════════════════════════════════════


@router.get("/dashboard/{hotel_id}")
async def get_dashboard(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.get_device_dashboard(hotel_id)
