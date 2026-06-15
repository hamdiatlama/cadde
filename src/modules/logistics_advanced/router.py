from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.logistics_advanced.repository import (
    CarrierRepository, ShipmentRepository, CarbonFootprintRepository, GiftWrapRepository,
)

router = APIRouter(prefix="/logistics-advanced", tags=["logistics_advanced"])


@router.post("/carriers", status_code=201)
async def add_carrier(name: str, api_url: str = None, api_key: str = None, services: str = None,
                      db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CarrierRepository(db)
    c = await repo.create_carrier(name=name, api_url=api_url, api_key=api_key, services=services)
    await db.commit()
    return {"id": c.id, "name": c.name}


@router.post("/carriers/{carrier_id}/rates", status_code=201)
async def add_rate(carrier_id: int, service_name: str, price: float, weight_min: float = 0, weight_max: float = None,
                   estimated_days_min: int = None, estimated_days_max: int = None,
                   db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CarrierRepository(db)
    r = await repo.add_rate(carrier_id, service_name=service_name, price=price,
                            weight_min=weight_min, weight_max=weight_max,
                            estimated_days_min=estimated_days_min, estimated_days_max=estimated_days_max)
    await db.commit()
    return {"id": r.id, "service_name": r.service_name, "price": r.price}


@router.get("/carriers/rates")
async def rate_shopping(weight: float = Query(...), db: AsyncSession = Depends(get_db)):
    repo = CarrierRepository(db)
    return await repo.get_rates(weight)


@router.post("/shipments/{order_id}", status_code=201)
async def create_shipment(order_id: int, carrier_id: int, service: str, weight: float = None,
                          db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ShipmentRepository(db)
    s = await repo.create_shipment(order_id, carrier_id, service, weight=weight)
    await db.commit()
    return {"id": s.id, "status": s.status}


@router.get("/shipments/{shipment_id}")
async def get_shipment(shipment_id: int, db: AsyncSession = Depends(get_db)):
    repo = ShipmentRepository(db)
    s = await repo.get_by_id(shipment_id)
    if not s:
        raise HTTPException(404, "Shipment not found")
    return s


@router.get("/shipments/tracking/{tracking_no}")
async def track_shipment(tracking_no: str, db: AsyncSession = Depends(get_db)):
    repo = ShipmentRepository(db)
    s = await repo.get_by_tracking(tracking_no)
    if not s:
        raise HTTPException(404, "Shipment not found")
    return s


@router.post("/carbon/calculate/{order_id}")
async def calculate_carbon(order_id: int, weight: float = Query(...), distance: float = Query(...),
                           db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = CarbonFootprintRepository(db)
    cf = await repo.calculate(order_id, weight, distance)
    await db.commit()
    return {"id": cf.id, "co2_grams": cf.co2_grams, "offset_cost": cf.offset_cost}


@router.post("/carbon/offset/{order_id}")
async def pay_offset(order_id: int, db: AsyncSession = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    repo = CarbonFootprintRepository(db)
    cf = await repo.create_offset(order_id)
    if not cf:
        raise HTTPException(404, "No unpaid carbon footprint found")
    await db.commit()
    return {"id": cf.id, "offset_paid": cf.offset_paid}


@router.get("/carbon/seller/total")
async def seller_carbon_total(db: AsyncSession = Depends(get_db),
                              current_user: User = Depends(get_current_user)):
    repo = CarbonFootprintRepository(db)
    return await repo.get_total(current_user.id)


@router.post("/gift-wraps", status_code=201)
async def create_gift_wrap(name: str, price: float = 0,
                           db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = GiftWrapRepository(db)
    gw = await repo.create_option(current_user.id, name=name, price=price)
    await db.commit()
    return {"id": gw.id, "name": gw.name, "price": gw.price}


@router.get("/gift-wraps")
async def list_gift_wraps(db: AsyncSession = Depends(get_db),
                          current_user: User = Depends(get_current_user)):
    repo = GiftWrapRepository(db)
    return await repo.list_options(current_user.id)
