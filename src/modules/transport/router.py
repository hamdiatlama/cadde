from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.transport.repository import TransportRepository
from src.modules.transport.service import TransportService

router = APIRouter(prefix="/transport", tags=["transport"])


async def get_repo(db: AsyncSession = Depends(get_db)):
    return TransportRepository(db)


async def get_service(db: AsyncSession = Depends(get_db)):
    return TransportService(TransportRepository(db))


# ════════════════════════════════════════════════════════════
#  FIRMA / ARAÇ / ŞOFÖR YÖNETİMİ
# ════════════════════════════════════════════════════════════

@router.get("/companies")
async def list_companies(vehicle_type: str = None, is_reseller: bool = None,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.list_companies(vehicle_type, is_reseller)


@router.post("/companies")
async def create_company(data: dict, svc: TransportService = Depends(get_service)):
    return await svc.register_company(data)


@router.put("/companies/{company_id}")
async def update_company(company_id: int, data: dict,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.update_company(company_id, data)


@router.get("/companies/{company_id}")
async def get_company(company_id: int, repo: TransportRepository = Depends(get_repo)):
    c = await repo.get_company(company_id)
    if not c: raise HTTPException(404, "Firma bulunamadı")
    return c


# ─── Araçlar ───────────────────────────────────────────────
@router.get("/vehicles")
async def list_vehicles(company_id: int = None, repo: TransportRepository = Depends(get_repo)):
    return await repo.list_vehicles(company_id)


@router.post("/vehicles")
async def create_vehicle(data: dict, svc: TransportService = Depends(get_service)):
    return await svc.add_vehicle(data.get("company_id"), data)


@router.put("/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, data: dict,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.update_vehicle(vehicle_id, data)


# ─── Şoförler ───────────────────────────────────────────────
@router.get("/drivers")
async def list_drivers(company_id: int = None, repo: TransportRepository = Depends(get_repo)):
    return await repo.list_drivers(company_id)


@router.post("/drivers")
async def create_driver(data: dict, svc: TransportService = Depends(get_service)):
    return await svc.add_driver(data.get("company_id"), data)


@router.put("/drivers/{driver_id}")
async def update_driver(driver_id: int, data: dict,
                         repo: TransportRepository = Depends(get_repo)):
    return await repo.update_driver(driver_id, data)


# ════════════════════════════════════════════════════════════
#  İSTASYON / ROTA / DURAK
# ════════════════════════════════════════════════════════════

@router.get("/stations/search")
async def search_stations(q: str = Query(min_length=2),
                           svc: TransportService = Depends(get_service)):
    return await svc.search_stations(q)


@router.get("/stations")
async def list_stations(city: str = None, repo: TransportRepository = Depends(get_repo)):
    return await repo.list_stations(city)


@router.get("/routes")
async def list_routes(company_id: int = None, vehicle_type: str = None,
                       repo: TransportRepository = Depends(get_repo)):
    return await repo.list_routes(company_id, vehicle_type)


@router.get("/routes/{route_id}/stops")
async def list_route_stops(route_id: int, can_pickup: bool = None,
                            repo: TransportRepository = Depends(get_repo)):
    return await repo.list_route_stops(route_id, can_pickup)


@router.post("/route-stops")
async def create_route_stop(data: dict, svc: TransportService = Depends(get_service)):
    return await svc.add_route_stop(
        data["route_id"], data.get("station_id"), data["name"],
        data.get("km_from_start", 0), data.get("minutes_from_departure", 0),
        data.get("lat"), data.get("lng"),
    )


# ════════════════════════════════════════════════════════════
#  SEFER / KOLTUK
# ════════════════════════════════════════════════════════════

@router.post("/schedules")
async def create_schedule(data: dict, svc: TransportService = Depends(get_service)):
    return await svc.create_schedule(data)


@router.get("/search")
async def search_trips(
    origin_id: int, destination_id: int, date: str = Query(min_length=10),
    vehicle_type: str = None, sort_by: str = "departure_time",
    min_price: float = None, max_price: float = None,
    is_pickup_route: bool = None, company_id: int = None,
    svc: TransportService = Depends(get_service),
):
    return await svc.search_trips(origin_id, destination_id, date, vehicle_type,
                                   sort_by=sort_by, min_price=min_price,
                                   max_price=max_price, is_pickup_route=is_pickup_route,
                                   company_id=company_id)


@router.get("/search-by-location")
async def search_by_location(
    from_lat: float, from_lng: float, to_lat: float, to_lng: float,
    date: str = Query(min_length=10), vehicle_type: str = None,
    svc: TransportService = Depends(get_service),
):
    return await svc.search_by_location(from_lat, from_lng, to_lat, to_lng, date, vehicle_type)


@router.get("/schedules/{schedule_id}")
async def get_schedule_detail(schedule_id: int,
                               svc: TransportService = Depends(get_service)):
    s = await svc.get_schedule_with_details(schedule_id)
    if not s: raise HTTPException(404, "Sefer bulunamadı")
    return s


@router.get("/schedules/{schedule_id}/stops")
async def get_schedule_stops(schedule_id: int,
                              svc: TransportService = Depends(get_service)):
    return await svc.get_route_stops(schedule_id)


@router.get("/schedules/{schedule_id}/seats")
async def list_available_seats(schedule_id: int, seat_class: str = None,
                                svc: TransportService = Depends(get_service)):
    return await svc.get_available_seats(schedule_id, seat_class)


# ════════════════════════════════════════════════════════════
#  BİLET
# ════════════════════════════════════════════════════════════

@router.post("/buy")
async def buy_ticket(
    schedule_id: int, seat_id: int,
    passenger_name: str, passenger_surname: str = None,
    passenger_id_no: str = None, passenger_phone: str = None,
    passenger_email: str = None,
    pickup_stop_id: int = None, dropoff_stop_id: int = None,
    pickup_lat: float = None, pickup_lng: float = None,
    pickup_address: str = None,
    user_id: int = 1,
    svc: TransportService = Depends(get_service),
):
    try:
        return await svc.buy_ticket(
            user_id, schedule_id, seat_id,
            passenger_name, passenger_surname,
            passenger_id_no, passenger_phone, passenger_email,
            pickup_stop_id, dropoff_stop_id,
            pickup_lat, pickup_lng, pickup_address,
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/tickets/{ticket_no}/cancel")
async def cancel_ticket(ticket_no: str, reason: str = None, user_id: int = 1,
                         svc: TransportService = Depends(get_service)):
    try:
        return await svc.cancel_ticket(ticket_no, user_id, reason)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/tickets/my")
async def my_tickets(status: str = None, user_id: int = 1,
                      svc: TransportService = Depends(get_service)):
    return await svc.get_user_tickets(user_id, status)


@router.get("/tickets/{ticket_no}")
async def get_ticket(ticket_no: str, svc: TransportService = Depends(get_service)):
    ticket = await svc.get_ticket_detail(ticket_no)
    if not ticket: raise HTTPException(404, "Bilet bulunamadı")
    return ticket


# ════════════════════════════════════════════════════════════
#  ŞOFÖR EKRANI / YOLCU ALMA
# ════════════════════════════════════════════════════════════

@router.get("/driver/{driver_id}/pickups")
async def driver_pickups(driver_id: int, date: str = None,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.get_driver_pickups(driver_id, date)


# ════════════════════════════════════════════════════════════
#  DEĞERLENDİRME
# ════════════════════════════════════════════════════════════

@router.post("/rate")
async def rate_transport(data: dict, svc: TransportService = Depends(get_service)):
    try:
        return await svc.rate_transport(
            data["ticket_id"], data.get("user_id", 1), data["company_id"],
            data.get("driver_id"), data.get("company_rating"),
            data.get("driver_rating"), data.get("cleanliness"),
            data.get("comfort"), data.get("punctuality"),
            data.get("overall"), data.get("comment"),
        )
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/ratings/company/{company_id}")
async def company_ratings(company_id: int,
                           repo: TransportRepository = Depends(get_repo)):
    return await repo.get_company_ratings(company_id)


@router.get("/ratings/driver/{driver_id}")
async def driver_ratings(driver_id: int,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.get_driver_ratings(driver_id)


# ════════════════════════════════════════════════════════════
#  BELGE YÖNETİMİ
# ════════════════════════════════════════════════════════════

@router.get("/documents")
async def list_documents(company_id: int = None, vehicle_id: int = None,
                          driver_id: int = None,
                          repo: TransportRepository = Depends(get_repo)):
    return await repo.list_documents(company_id, vehicle_id, driver_id)


@router.post("/documents")
async def create_document(data: dict,
                           repo: TransportRepository = Depends(get_repo)):
    return await repo.create_document(data)
