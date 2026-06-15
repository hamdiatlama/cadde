from fastapi import APIRouter, Depends, HTTPException
from src.modules.rental.repository import RentalRepository, get_rental_repo

router = APIRouter(prefix="/rental", tags=["rental"])


@router.post("/companies")
async def create_company(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_company(data)


@router.get("/companies")
async def list_companies(category: str = None, city: str = None,
                          repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_companies(category, city)


@router.get("/companies/{company_id}")
async def get_company(company_id: int, repo: RentalRepository = Depends(get_rental_repo)):
    c = await repo.get_company(company_id)
    if not c: raise HTTPException(404, "Firma bulunamadi")
    return c


@router.post("/branches")
async def create_branch(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_branch(data)


@router.get("/branches")
async def list_branches(company_id: int = None, city: str = None,
                         repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_branches(company_id, city)


@router.post("/vehicles")
async def create_vehicle(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_vehicle(data)


@router.get("/vehicles")
async def list_vehicles(category: str = None, company_id: int = None,
                         branch_id: int = None, city: str = None,
                         min_price: float = None, max_price: float = None,
                         repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_vehicles(category, company_id, branch_id, city, min_price, max_price)


@router.get("/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, repo: RentalRepository = Depends(get_rental_repo)):
    v = await repo.get_vehicle(vehicle_id)
    if not v: raise HTTPException(404, "Arac bulunamadi")
    return v


@router.post("/bookings")
async def create_booking(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_booking(data)


@router.get("/bookings/my")
async def my_bookings(user_id: int = 1, status: str = None,
                       repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_bookings(user_id=user_id, status=status)


@router.get("/bookings/{booking_id}")
async def get_booking(booking_id: int, repo: RentalRepository = Depends(get_rental_repo)):
    b = await repo.get_booking(booking_id)
    if not b: raise HTTPException(404, "Rezervasyon bulunamadi")
    return b


@router.post("/bookings/{booking_id}/return")
async def return_vehicle(booking_id: int, repo: RentalRepository = Depends(get_rental_repo)):
    b = await repo.return_vehicle(booking_id)
    if not b: raise HTTPException(404, "Rezervasyon bulunamadi")
    return b


@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: int, reason: str = None,
                          repo: RentalRepository = Depends(get_rental_repo)):
    b = await repo.cancel_booking(booking_id, reason)
    if not b: raise HTTPException(404, "Rezervasyon bulunamadi")
    return b


@router.post("/insurances")
async def create_insurance(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_insurance(data)


@router.get("/insurances")
async def list_insurances(company_id: int = None,
                           repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_insurances(company_id)


@router.post("/reviews")
async def create_review(data: dict, repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.create_review(data)


@router.get("/reviews")
async def list_reviews(vehicle_id: int = None,
                        repo: RentalRepository = Depends(get_rental_repo)):
    return await repo.list_reviews(vehicle_id)
