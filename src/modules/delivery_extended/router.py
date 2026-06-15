from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.delivery_extended.repository import DeliveryExtendedRepository

router = APIRouter(prefix="/delivery-extended", tags=["delivery_extended"])


@router.post("/slots", status_code=201)
async def create_slot(date: str, start_time: str, end_time: str, max_orders: int = 10,
                      current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    s = await repo.create_slot(current_user.id, date, start_time, end_time, max_orders)
    await db.commit()
    return {"id": s.id, "date": s.date, "start_time": s.start_time, "end_time": s.end_time}


@router.get("/slots")
async def list_slots(date: str, db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    return await repo.list_available_slots(date)


@router.post("/slots/{id}/book")
async def book_slot(id: int, db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    s = await repo.book_slot(id)
    if not s:
        raise HTTPException(404, "Slot not found or fully booked")
    await db.commit()
    return {"id": s.id, "current_orders": s.current_orders, "max_orders": s.max_orders}


@router.post("/express/{order_id}", status_code=201)
async def create_express(order_id: int, fee: float, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    e = await repo.create_express(order_id, fee)
    await db.commit()
    return {"id": e.id, "status": e.status, "fee": e.fee}


@router.put("/express/{id}/assign")
async def assign_courier(id: int, courier_id: int, current_user: User = Depends(get_current_user),
                         db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    e = await repo.assign_courier(id, courier_id)
    if not e:
        raise HTTPException(404, "Express delivery not found")
    await db.commit()
    return {"id": e.id, "courier_id": e.courier_id, "status": e.status}


@router.post("/pickup-points", status_code=201)
async def create_pickup_point(name: str, address: str, city: str, lat: float = None, lng: float = None,
                              current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    p = await repo.create_pickup_point(name, address, city, lat, lng)
    await db.commit()
    return {"id": p.id, "name": p.name, "city": p.city}


@router.get("/pickup-points")
async def list_pickup_points(city: str = None, db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    return await repo.list_pickup_points(city)


@router.post("/international/{order_id}", status_code=201)
async def create_international_shipment(order_id: int, origin_country: str, destination_country: str,
                                        customs_value: float = None, shipping_cost: float = None,
                                        current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    s = await repo.create_international_shipment(order_id, origin_country, destination_country,
                                                  customs_value, shipping_cost)
    await db.commit()
    return {"id": s.id, "origin": s.origin_country, "destination": s.destination_country}


@router.get("/international/{id}")
async def get_international_shipment(id: int, db: AsyncSession = Depends(get_db)):
    repo = DeliveryExtendedRepository(db)
    s = await repo.get_shipment(id)
    if not s:
        raise HTTPException(404, "International shipment not found")
    return s
