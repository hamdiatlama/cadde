from fastapi import APIRouter, Depends, HTTPException
from src.modules.tourism.repository import TourismRepository, get_tourism_repo

router = APIRouter(prefix="/tourism", tags=["tourism"])


# ─── Provider ────────────────────────────────────────────────
@router.post("/providers")
async def create_provider(data: dict,
                           repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.create_provider(data)


@router.get("/providers/my")
async def my_provider(user_id: int = 1,
                       repo: TourismRepository = Depends(get_tourism_repo)):
    p = await repo.get_provider_by_user(user_id)
    if not p: raise HTTPException(404, "Sağlayıcı kaydınız bulunamadı")
    return p


@router.get("/providers")
async def list_providers(is_verified: bool = None, is_active: bool = None,
                          repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.list_providers(is_verified, is_active)


@router.get("/providers/{provider_id}")
async def get_provider(provider_id: int,
                        repo: TourismRepository = Depends(get_tourism_repo)):
    p = await repo.get_provider(provider_id)
    if not p: raise HTTPException(404, "Sağlayıcı bulunamadı")
    return p


# ─── Experience ──────────────────────────────────────────────
@router.post("/experiences")
async def create_experience(data: dict,
                             repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.create_experience(data)


@router.get("/experiences")
async def list_experiences(category: str = None, city: str = None,
                            provider_id: int = None, is_active: bool = None,
                            repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.list_experiences(category, city, provider_id, is_active)


@router.get("/experiences/{exp_id}")
async def get_experience(exp_id: int,
                          repo: TourismRepository = Depends(get_tourism_repo)):
    e = await repo.get_experience(exp_id)
    if not e: raise HTTPException(404, "Deneyim bulunamadı")
    return e


@router.put("/experiences/{exp_id}")
async def update_experience(exp_id: int, data: dict,
                             repo: TourismRepository = Depends(get_tourism_repo)):
    e = await repo.update_experience(exp_id, data)
    if not e: raise HTTPException(404, "Deneyim bulunamadı")
    return e


# ─── Schedule ────────────────────────────────────────────────
@router.post("/schedules")
async def create_schedule(data: dict,
                           repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.create_schedule(data)


@router.get("/schedules")
async def list_schedules(experience_id: int = None, date: str = None,
                          repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.list_schedules(experience_id, date)


# ─── Booking ─────────────────────────────────────────────────
@router.post("/bookings")
async def create_booking(data: dict,
                          repo: TourismRepository = Depends(get_tourism_repo)):
    try:
        return await repo.create_booking(data)
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.get("/bookings/my")
async def my_bookings(user_id: int = 1, status: str = None,
                       repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.list_bookings(user_id=user_id, status=status)


@router.get("/bookings/{booking_no}")
async def get_booking(booking_no: str,
                       repo: TourismRepository = Depends(get_tourism_repo)):
    b = await repo.get_booking_by_no(booking_no)
    if not b: raise HTTPException(404, "Rezervasyon bulunamadı")
    return b


@router.post("/bookings/{booking_id}/cancel")
async def cancel_booking(booking_id: int, reason: str = None,
                          repo: TourismRepository = Depends(get_tourism_repo)):
    b = await repo.cancel_booking(booking_id, reason)
    if not b: raise HTTPException(404, "Rezervasyon bulunamadı")
    return b


# ─── Review ──────────────────────────────────────────────────
@router.post("/reviews")
async def create_review(data: dict,
                         repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.create_review(data)


@router.get("/reviews")
async def list_reviews(experience_id: int = None,
                        repo: TourismRepository = Depends(get_tourism_repo)):
    return await repo.list_reviews(experience_id)
