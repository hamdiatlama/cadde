from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.hotel.service import HotelService

router = APIRouter(prefix="/hotels", tags=["hotels"])


# ─── helpers ───────────────────────────────────────────────────────

def get_service(db: AsyncSession = Depends(get_db)) -> HotelService:
    return HotelService(db)


async def get_hotel_owner_check(hotel_id: int, current_user: User, db: AsyncSession):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only hotels owners can manage hotels")
    service = HotelService(db)
    hotel = await service.get_hotel_by_id(hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    if hotel.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "You do not own this hotel")
    return hotel


# ─── Service Categories & Tags (Klik Sistemi) ─────────────────────

@router.get("/service-categories")
async def list_service_categories(db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    return await service.list_service_categories()


@router.get("/{hotel_id}/services")
async def get_property_services(hotel_id: int, db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    hotel = await service.repo.get_hotel(hotel_id)
    if not hotel:
        raise HTTPException(404, "Property not found")
    return await service.get_property_services(hotel_id)


@router.post("/{hotel_id}/services", status_code=201)
async def add_property_service(
    hotel_id: int,
    category_id: int = Query(...),
    name: str = Query(...),
    icon: str = Query(None),
    description: str = Query(None),
    is_free: bool = Query(True),
    price: float = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.add_property_service(hotel_id, category_id, name, icon, description, is_free, price)
    await db.commit()
    return result


@router.delete("/{hotel_id}/services/{service_id}")
async def remove_property_service(
    hotel_id: int,
    service_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    ok = await svc.remove_property_service(service_id)
    if not ok:
        raise HTTPException(404, "Service not found")
    await db.commit()
    return {"ok": True}


# ─── Public endpoints ──────────────────────────────────────────────

@router.get("/")
async def search_hotels(
    city: str = Query(None),
    property_type: str = Query(None),
    min_star: int = Query(None),
    max_price: float = Query(None),
    amenities: str = Query(None),
    guests: int = Query(None),
    check_in: str = Query(None),
    check_out: str = Query(None),
    sort_by: str = Query("created_at"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    result, total = await service.search_hotels(
        city=city, property_type=property_type, min_star=min_star, max_price=max_price,
        amenities=amenities, guests=guests,
        check_in=check_in, check_out=check_out,
        sort_by=sort_by, page=page, per_page=per_page,
    )
    return {"hotels": result, "total": total, "page": page, "per_page": per_page}


@router.get("/{slug}")
async def get_hotel_detail(slug: str, db: AsyncSession = Depends(get_db)):
    service = get_service(db)
    hotel = await service.get_hotel_by_slug(slug)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    return await service.get_hotel_detail(hotel.id)


@router.get("/{slug}/rooms/available")
async def get_available_rooms(
    slug: str,
    check_in: str = Query(...),
    check_out: str = Query(...),
    guests: int = Query(1, ge=1),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    hotel = await service.get_hotel_by_slug(slug)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    return await service.get_available_rooms(hotel.id, check_in, check_out, guests)


@router.get("/{slug}/reviews")
async def list_hotel_reviews(
    slug: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    hotel = await service.get_hotel_by_slug(slug)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    return await service.list_hotel_reviews(hotel.id, page, per_page)


# ─── User endpoints ────────────────────────────────────────────────

@router.post("/{slug}/calculate-price")
async def calculate_price(
    slug: str,
    room_type_id: int = Query(...),
    check_in: str = Query(...),
    check_out: str = Query(...),
    room_count: int = Query(1, ge=1),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    hotel = await service.get_hotel_by_slug(slug)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    return await service.calculate_price(hotel.id, room_type_id, check_in, check_out, room_count)


@router.post("/{slug}/book", status_code=201)
async def create_booking(
    slug: str,
    room_type_id: int = Query(...),
    check_in: str = Query(...),
    check_out: str = Query(...),
    guests: int = Query(1, ge=1),
    room_count: int = Query(1, ge=1),
    special_requests: str = Query(None),
    guest_name: str = Query(None),
    guest_email: str = Query(None),
    guest_phone: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    hotel = await service.get_hotel_by_slug(slug)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    result = await service.create_booking(
        hotel_id=hotel.id, room_type_id=room_type_id,
        user_id=current_user.id,
        check_in=check_in, check_out=check_out,
        guests=guests, room_count=room_count,
        special_requests=special_requests,
        guest_name=guest_name, guest_email=guest_email, guest_phone=guest_phone,
    )
    await db.commit()
    return result


@router.get("/bookings/my")
async def list_my_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    return await service.list_user_bookings(current_user.id)


@router.get("/bookings/{booking_no}")
async def get_booking_detail(
    booking_no: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    booking = await service.get_booking_by_no(booking_no)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Not your booking")
    return await service.get_booking_detail(booking.id)


@router.post("/bookings/{booking_no}/cancel")
async def cancel_booking(
    booking_no: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    booking = await service.get_booking_by_no(booking_no)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "Not your booking")
    result = await service.cancel_booking(booking.id)
    await db.commit()
    return result


@router.post("/bookings/{booking_no}/review", status_code=201)
async def add_booking_review(
    booking_no: str,
    rating: int = Query(..., ge=1, le=10),
    comment: str = Query(None),
    cleanliness: int = Query(None, ge=1, le=10),
    comfort: int = Query(None, ge=1, le=10),
    location_score: int = Query(None, ge=1, le=10),
    staff_score: int = Query(None, ge=1, le=10),
    value_score: int = Query(None, ge=1, le=10),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    service = get_service(db)
    booking = await service.get_booking_by_no(booking_no)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != current_user.id:
        raise HTTPException(403, "Not your booking")
    result = await service.add_review(
        booking_id=booking.id, hotel_id=booking.hotel_id,
        user_id=current_user.id,
        rating=rating, comment=comment,
        cleanliness=cleanliness, comfort=comfort,
        location_score=location_score, staff_score=staff_score,
        value_score=value_score,
    )
    await db.commit()
    return result


# ─── Seller / Hotel owner endpoints ───────────────────────────────

@router.post("/add", status_code=201)
async def add_hotel(
    name: str = Query(...),
    description: str = Query(None),
    property_type: str = Query("hotel"),
    listing_type: str = Query("entire_place"),
    star_rating: int = Query(3, ge=1, le=10),
    address: str = Query(None),
    city: str = Query(...),
    country: str = Query("Türkiye"),
    lat: float = Query(None),
    lng: float = Query(None),
    phone: str = Query(None),
    email: str = Query(None),
    website: str = Query(None),
    tax_id: str = Query(None),
    company_name: str = Query(None),
    company_description: str = Query(None),
    house_rules: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only property owners can manage")
    service = get_service(db)
    result = await service.create_hotel(
        owner_id=current_user.id,
        name=name, description=description,
        property_type=property_type, listing_type=listing_type,
        star_rating=star_rating, address=address,
        city=city, country=country,
        lat=lat, lng=lng, phone=phone, email=email,
        website=website, tax_id=tax_id,
        company_name=company_name, company_description=company_description,
        house_rules=house_rules,
    )
    await db.commit()
    return result


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    name: str = Query(None),
    description: str = Query(None),
    star_rating: int = Query(None, ge=1, le=10),
    address: str = Query(None),
    city: str = Query(None),
    country: str = Query(None),
    lat: float = Query(None),
    lng: float = Query(None),
    phone: str = Query(None),
    email: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.update_hotel(
        hotel_id=hotel_id,
        name=name, description=description,
        star_rating=star_rating, address=address,
        city=city, country=country,
        lat=lat, lng=lng, phone=phone, email=email,
    )
    await db.commit()
    return result


@router.post("/{hotel_id}/amenities", status_code=201)
async def add_hotel_amenity(
    hotel_id: int,
    name: str = Query(...),
    icon: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.add_amenity(hotel_id, name, icon)
    await db.commit()
    return result


@router.post("/{hotel_id}/photos", status_code=201)
async def add_hotel_photo(
    hotel_id: int,
    url: str = Query(...),
    caption: str = Query(None),
    category: str = Query("exterior"),
    is_main: bool = Query(False),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.add_photo(hotel_id, url, caption, is_main, category)
    await db.commit()
    return result


@router.put("/{hotel_id}/photos/{photo_id}/main")
async def set_main_photo(
    hotel_id: int,
    photo_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.set_main_photo(hotel_id, photo_id)
    await db.commit()
    return result


@router.post("/{hotel_id}/rooms", status_code=201)
async def create_room_type(
    hotel_id: int,
    name: str = Query(...),
    description: str = Query(None),
    max_guests: int = Query(2, ge=1),
    bed_type: str = Query(None),
    size_sqm: float = Query(None),
    quantity: int = Query(1, ge=1),
    base_price: float = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.create_room_type(
        hotel_id=hotel_id,
        name=name, description=description,
        max_guests=max_guests, bed_type=bed_type,
        size_sqm=size_sqm, quantity=quantity,
        base_price=base_price,
    )
    await db.commit()
    return result


@router.put("/{hotel_id}/rooms/{room_type_id}")
async def update_room_type(
    hotel_id: int,
    room_type_id: int,
    name: str = Query(None),
    description: str = Query(None),
    max_guests: int = Query(None, ge=1),
    bed_type: str = Query(None),
    size_sqm: float = Query(None),
    quantity: int = Query(None, ge=1),
    base_price: float = Query(None),
    is_active: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.update_room_type(
        room_type_id=room_type_id,
        name=name, description=description,
        max_guests=max_guests, bed_type=bed_type,
        size_sqm=size_sqm, quantity=quantity,
        base_price=base_price, is_active=is_active,
    )
    await db.commit()
    return result


@router.get("/{hotel_id}/rooms")
async def list_room_types(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    return await service.list_room_types(hotel_id)


@router.post("/{hotel_id}/rooms/{room_type_id}/seasonal-price", status_code=201)
async def set_seasonal_price(
    hotel_id: int,
    room_type_id: int,
    name: str = Query(None),
    start_date: str = Query(...),
    end_date: str = Query(...),
    price: float = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.set_seasonal_price(
        room_type_id=room_type_id,
        name=name, start_date=start_date,
        end_date=end_date, price=price,
    )
    await db.commit()
    return result


@router.get("/{hotel_id}/rooms/{room_type_id}/availability")
async def get_availability_calendar(
    hotel_id: int,
    room_type_id: int,
    start_date: str = Query(...),
    end_date: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    return await service.get_availability_calendar(room_type_id, start_date, end_date)


@router.post("/{hotel_id}/rooms/{room_type_id}/block")
async def block_dates(
    hotel_id: int,
    room_type_id: int,
    start_date: str = Query(...),
    end_date: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.block_dates(room_type_id, start_date, end_date)
    await db.commit()
    return result


@router.post("/{hotel_id}/rooms/{room_type_id}/unblock")
async def unblock_dates(
    hotel_id: int,
    room_type_id: int,
    start_date: str = Query(...),
    end_date: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    result = await service.unblock_dates(room_type_id, start_date, end_date)
    await db.commit()
    return result


@router.get("/{hotel_id}/bookings")
async def list_hotel_bookings(
    hotel_id: int,
    status: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    service = get_service(db)
    return await service.list_hotel_bookings(hotel_id, status, page, per_page)


@router.put("/bookings/{booking_id}/status")
async def update_booking_status(
    booking_id: int,
    status: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only hotels owners can manage hotels")
    service = get_service(db)
    booking = await service.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(404, "Booking not found")
    hotel = await service.get_hotel_by_id(booking.hotel_id)
    if not hotel:
        raise HTTPException(404, "Hotel not found")
    if hotel.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(403, "You do not own this hotel")
    result = await service.update_booking_status(booking_id, status)
    await db.commit()
    return result


# ─── Admin endpoints ───────────────────────────────────────────────

@router.get("/admin/all")
async def list_all_hotels_admin(
    city: str = Query(None),
    status: str = Query(None),
    min_rating: float = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin only")
    service = get_service(db)
    return await service.list_all_hotels(
        city=city, status=status,
        min_rating=min_rating,
        page=page, per_page=per_page,
    )
