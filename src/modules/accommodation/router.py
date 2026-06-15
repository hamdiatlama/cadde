from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.accommodation.service import AccommodationService
from src.modules.hotel.service import HotelService

router = APIRouter(prefix="/accommodation", tags=["accommodation"])


def get_service(db: AsyncSession = Depends(get_db)) -> AccommodationService:
    return AccommodationService(db)


def get_hotel_service(db: AsyncSession = Depends(get_db)) -> HotelService:
    return HotelService(db)


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
# Satisfaction Surveys
# ═══════════════════════════════════════════════════════════════════

@router.post("/surveys", status_code=201)
async def submit_survey(
    booking_id: int = Query(...),
    overall_score: int = Query(None, ge=1, le=10),
    would_recommend: bool = Query(None),
    checkin_experience: int = Query(None, ge=1, le=10),
    cleanliness_score: int = Query(None, ge=1, le=10),
    service_score: int = Query(None, ge=1, le=10),
    view_score: int = Query(None, ge=1, le=10),
    food_score: int = Query(None, ge=1, le=10),
    value_score: int = Query(None, ge=1, le=10),
    noise_score: int = Query(None, ge=1, le=10),
    bed_comfort: int = Query(None, ge=1, le=10),
    comments: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.submit_survey(current_user.id, {
        "booking_id": booking_id,
        "overall_score": overall_score,
        "would_recommend": would_recommend,
        "checkin_experience": checkin_experience,
        "cleanliness_score": cleanliness_score,
        "service_score": service_score,
        "view_score": view_score,
        "food_score": food_score,
        "value_score": value_score,
        "noise_score": noise_score,
        "bed_comfort": bed_comfort,
        "comments": comments,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/satisfaction")
async def get_property_satisfaction(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.get_hotel_satisfaction(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Guest Complaints
# ═══════════════════════════════════════════════════════════════════

@router.post("/complaints", status_code=201)
async def file_complaint(
    booking_id: int = Query(...),
    category: str = Query(...),
    priority: str = Query("normal"),
    description: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.file_complaint(current_user.id, {
        "booking_id": booking_id,
        "category": category,
        "priority": priority,
        "description": description,
    })
    await db.commit()
    return result


@router.get("/complaints/my")
async def list_my_complaints(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    complaints, total = await svc.repo.list_user_complaints(current_user.id, page, per_page)
    return {
        "complaints": [svc._format_complaint(c) for c in complaints],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/properties/{hotel_id}/complaints")
async def list_property_complaints(
    hotel_id: int,
    status: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    complaints, total = await svc.repo.list_hotel_complaints(hotel_id, status, page, per_page)
    return {
        "complaints": [svc._format_complaint(c) for c in complaints],
        "total": total, "page": page, "per_page": per_page,
    }


@router.post("/complaints/{complaint_id}/resolve")
async def resolve_complaint(
    complaint_id: int,
    resolution_notes: str = Query(None),
    compensation: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role not in ("seller", "admin"):
        raise HTTPException(403, "Only property owners can resolve complaints")
    svc = get_service(db)
    result = await svc.resolve_complaint(complaint_id, current_user.id, {
        "resolution_notes": resolution_notes,
        "compensation": compensation,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/complaint-stats")
async def get_complaint_stats(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.get_complaint_stats(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Guest Preferences
# ═══════════════════════════════════════════════════════════════════

@router.get("/preferences")
async def get_preferences(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.get_preferences(current_user.id)
    if not result:
        raise HTTPException(404, "No preferences found")
    return result


@router.put("/preferences")
async def update_preferences(
    preferred_room_type: str = Query(None),
    dietary_restrictions: str = Query(None),
    special_needs: str = Query(None),
    preferred_floor: str = Query(None),
    smoking_preference: str = Query(None),
    notes: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.save_preferences(current_user.id, {
        "preferred_room_type": preferred_room_type,
        "dietary_restrictions": dietary_restrictions,
        "special_needs": special_needs,
        "preferred_floor": preferred_floor,
        "smoking_preference": smoking_preference,
        "notes": notes,
    })
    await db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════
# Housekeeping
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/housekeeping", status_code=201)
async def log_housekeeping(
    hotel_id: int,
    room_type_id: int = Query(None),
    room_number: str = Query(None),
    cleaner_name: str = Query(None),
    status: str = Query("completed"),
    notes: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.log_housekeeping(hotel_id, {
        "room_type_id": room_type_id,
        "room_number": room_number,
        "cleaner_name": cleaner_name,
        "status": status,
        "notes": notes,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/housekeeping")
async def list_housekeeping(
    hotel_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    logs, total = await svc.repo.list_housekeeping_logs(hotel_id, page, per_page)
    return {
        "logs": [svc._format_housekeeping(h) for h in logs],
        "total": total, "page": page, "per_page": per_page,
    }


# ═══════════════════════════════════════════════════════════════════
# Fumigation / Pest Control (ÇOK ÖNEMLİ)
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/fumigation", status_code=201)
async def schedule_fumigation(
    hotel_id: int,
    scheduled_date: str = Query(None),
    chemical_used: str = Query(None),
    company_name: str = Query(None),
    technician_name: str = Query(None),
    target_pests: str = Query(None),
    areas_treated: str = Query(None),
    notes: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.schedule_fumigation(hotel_id, {
        "scheduled_date": scheduled_date,
        "chemical_used": chemical_used,
        "company_name": company_name,
        "technician_name": technician_name,
        "target_pests": target_pests,
        "areas_treated": areas_treated,
        "notes": notes,
    })
    await db.commit()
    return result


@router.put("/fumigation/{log_id}/complete")
async def complete_fumigation(
    log_id: int,
    fumigation_date: str = Query(None),
    next_fumigation_date: str = Query(None),
    chemical_used: str = Query(None),
    notes: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    log = await svc.repo.get_fumigation_log(log_id)
    if not log:
        raise HTTPException(404, "Fumigation log not found")
    await get_hotel_owner_check(log.hotel_id, current_user, db)
    result = await svc.complete_fumigation(log_id, {
        "fumigation_date": fumigation_date,
        "next_fumigation_date": next_fumigation_date,
        "chemical_used": chemical_used,
        "notes": notes,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/fumigation")
async def list_fumigation_logs(
    hotel_id: int,
    status: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    logs, total = await svc.repo.list_fumigation_logs(hotel_id, status, page, per_page)
    return {
        "logs": [svc._format_fumigation(f) for f in logs],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/properties/{hotel_id}/fumigation/status")
async def get_fumigation_status(
    hotel_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    return await svc.get_fumigation_status(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Hotel Kitchen / Restaurant
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/kitchens", status_code=201)
async def create_kitchen(
    hotel_id: int,
    name: str = Query(...),
    cuisine_type: str = Query(None),
    opening_time: str = Query("07:00"),
    closing_time: str = Query("22:00"),
    min_order_amount: float = Query(0),
    preparation_time_min: int = Query(30),
    phone: str = Query(None),
    description: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.create_kitchen(hotel_id, {
        "name": name, "cuisine_type": cuisine_type,
        "opening_time": opening_time, "closing_time": closing_time,
        "min_order_amount": min_order_amount,
        "preparation_time_min": preparation_time_min,
        "phone": phone, "description": description,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/kitchens")
async def list_kitchens(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    kitchens = await svc.repo.list_hotel_kitchens(hotel_id)
    return [svc._format_kitchen(k) for k in kitchens]


@router.post("/kitchens/{kitchen_id}/menu", status_code=201)
async def add_menu_item(
    kitchen_id: int,
    name: str = Query(...),
    description: str = Query(None),
    category: str = Query(None),
    price: float = Query(...),
    compare_price: float = Query(None),
    is_vegetarian: bool = Query(False),
    is_vegan: bool = Query(False),
    is_gluten_free: bool = Query(False),
    image_url: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    kitchen = await svc.repo.get_kitchen(kitchen_id)
    if not kitchen:
        raise HTTPException(404, "Kitchen not found")
    await get_hotel_owner_check(kitchen.hotel_id, current_user, db)
    result = await svc.add_menu_item(kitchen.hotel_id, kitchen_id, {
        "name": name, "description": description, "category": category,
        "price": price, "compare_price": compare_price,
        "is_vegetarian": is_vegetarian, "is_vegan": is_vegan,
        "is_gluten_free": is_gluten_free, "image_url": image_url,
    })
    await db.commit()
    return result


@router.get("/kitchens/{kitchen_id}/menu")
async def get_menu(
    kitchen_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    kitchen = await svc.repo.get_kitchen(kitchen_id)
    if not kitchen:
        raise HTTPException(404, "Kitchen not found")
    return await svc.get_kitchen_menu(kitchen_id)


# ═══════════════════════════════════════════════════════════════════
# In-Room Dining
# ═══════════════════════════════════════════════════════════════════

@router.post("/dining/order", status_code=201)
async def place_dining_order(
    booking_id: int = Query(...),
    kitchen_id: int = Query(...),
    room_number: str = Query(None),
    total_price: float = Query(...),
    special_instructions: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.place_dining_order(current_user.id, {
        "booking_id": booking_id,
        "kitchen_id": kitchen_id,
        "room_number": room_number,
        "total_price": total_price,
        "special_instructions": special_instructions,
    })
    await db.commit()
    return result


@router.get("/dining/orders/my")
async def list_my_dining_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    bookings_svc = get_hotel_service(db)
    bookings, _ = await bookings_svc.repo.list_user_bookings(current_user.id, page=1, per_page=100)
    all_orders = []
    for b in bookings:
        orders = await svc.repo.list_booking_dining_orders(b.id)
        all_orders.extend([svc._format_dining_order(o) for o in orders])
    return sorted(all_orders, key=lambda x: x["ordered_at"] or "", reverse=True)


@router.put("/dining/orders/{order_id}/status")
async def update_dining_order_status(
    order_id: int,
    status: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    order = await svc.repo.get_dining_order(order_id)
    if not order:
        raise HTTPException(404, "Order not found")
    await get_hotel_owner_check(order.hotel_id, current_user, db)
    result = await svc.update_dining_status(order_id, status)
    await db.commit()
    return result


@router.get("/kitchens/{kitchen_id}/orders")
async def list_kitchen_orders(
    kitchen_id: int,
    status: str = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    kitchen = await svc.repo.get_kitchen(kitchen_id)
    if not kitchen:
        raise HTTPException(404, "Kitchen not found")
    await get_hotel_owner_check(kitchen.hotel_id, current_user, db)
    orders, total = await svc.repo.list_kitchen_orders(kitchen_id, status, page, per_page)
    return {
        "orders": [svc._format_dining_order(o) for o in orders],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/kitchens/{kitchen_id}/rating")
async def get_kitchen_rating(
    kitchen_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    kitchen = await svc.repo.get_kitchen(kitchen_id)
    if not kitchen:
        raise HTTPException(404, "Kitchen not found")
    menu = await svc.get_kitchen_menu(kitchen_id)
    rating = await svc.repo.get_kitchen_rating(kitchen_id)
    reviews_raw, _ = await svc.repo.list_kitchen_reviews(kitchen_id, page=1, per_page=5)
    return {
        "kitchen": svc._format_kitchen(kitchen),
        "menu": menu,
        "rating": rating,
        "recent_reviews": [svc._format_kitchen_review(r) for r in reviews_raw],
    }


# ═══════════════════════════════════════════════════════════════════
# Tourism Associations (Dernek Üyelikleri)
# ═══════════════════════════════════════════════════════════════════

@router.get("/associations")
async def list_tourism_associations(db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    assocs = await svc.repo.list_associations()
    return [{"id": a.id, "name": a.name, "type": a.association_type, "city": a.city} for a in assocs]


@router.post("/properties/{hotel_id}/associations", status_code=201)
async def join_association(
    hotel_id: int,
    association_id: int = Query(...),
    membership_number: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.join_association(hotel_id, association_id, membership_number)
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/associations")
async def list_property_associations(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return await svc.get_property_associations(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Property Documents (Resmi İzin Belgeleri)
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/documents", status_code=201)
async def upload_document(
    hotel_id: int,
    document_type: str = Query(...),
    document_name: str = Query(None),
    file_url: str = Query(...),
    reference_number: str = Query(None),
    issuing_authority: str = Query(None),
    issue_date: str = Query(None),
    expiry_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.upload_document(hotel_id, {
        "document_type": document_type, "document_name": document_name,
        "file_url": file_url, "reference_number": reference_number,
        "issuing_authority": issuing_authority,
        "issue_date": issue_date, "expiry_date": expiry_date,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/documents")
async def list_documents(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    docs = await svc.repo.list_documents(hotel_id)
    return [
        {
            "id": d.id, "document_type": d.document_type,
            "document_name": d.document_name, "file_url": d.file_url,
            "reference_number": d.reference_number,
            "issuing_authority": d.issuing_authority,
            "is_verified": d.is_verified,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in docs
    ]


@router.get("/properties/{hotel_id}/document-stats")
async def get_document_stats(hotel_id: int, db: AsyncSession = Depends(get_db)):
    svc = get_service(db)
    return await svc.get_document_stats(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Location Duplicate Detection (Aynı Lokasyon Kontrolü)
# ═══════════════════════════════════════════════════════════════════

@router.get("/check-location")
async def check_location_duplicate(
    lat: float = Query(...),
    lng: float = Query(...),
    city: str = Query(None),
    address: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.check_location_duplicate(lat, lng, city, address)


@router.post("/properties/{hotel_id}/location-reopen-request", status_code=201)
async def request_location_reopen(
    hotel_id: int,
    existing_hotel_id: int = Query(...),
    reason: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.request_location_reopen(hotel_id, existing_hotel_id, current_user.id, reason)
    await db.commit()
    return result


@router.put("/location-reopen-requests/{request_id}/approve")
async def approve_location_reopen(
    request_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Only CC authority can approve location reopen")
    svc = get_service(db)
    result = await svc.approve_location_reopen(request_id, current_user.id)
    await db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════
# Suspension & Complaint Escalation (24 Saat Kuralı)
# ═══════════════════════════════════════════════════════════════════

@router.post("/complaints/{complaint_id}/respond")
async def respond_to_complaint(
    complaint_id: int,
    description: str = Query(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    complaint = await svc.repo.get_complaint(complaint_id)
    if not complaint:
        raise HTTPException(404, "Complaint not found")
    hotel = await get_hotel_owner_check(complaint.hotel_id, current_user, db)
    action = await svc.repo.create_complaint_action(
        complaint_id=complaint_id,
        action_type="response",
        description=description,
        performed_by=current_user.id,
    )
    await svc.repo.update_complaint_status(complaint_id, "resolved")
    await db.commit()
    return {"id": action.id, "action_type": "response", "deadline": action.deadline.isoformat() if action.deadline else None}


@router.post("/admin/escalate-overdue-complaints")
async def check_and_escalate(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin only")
    svc = get_service(db)
    result = await svc.check_and_suspend_overdue_complaints()
    await db.commit()
    return {"escalated": result, "count": len(result)}


@router.get("/properties/{hotel_id}/suspension-status")
async def get_suspension_status(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.get_hotel_suspension_status(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Guest Bans (Müşteri Men Etme Sistemi)
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/bans", status_code=201)
async def ban_guest(
    hotel_id: int,
    user_id: int = Query(...),
    reason_category: str = Query(...),
    description: str = Query(None),
    is_permanent: bool = Query(True),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.ban_guest(hotel_id, user_id, current_user.id, {
        "reason_category": reason_category,
        "description": description,
        "is_permanent": is_permanent,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/bans")
async def list_hotel_bans(
    hotel_id: int,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    bans, total = await svc.repo.list_hotel_bans(hotel_id, page, per_page)
    return {
        "bans": [{"id": b.id, "user_id": b.user_id, "reason_category": b.reason_category, "description": b.description, "is_permanent": b.is_permanent, "created_at": b.created_at.isoformat() if b.created_at else None} for b in bans],
        "total": total, "page": page, "per_page": per_page,
    }


@router.get("/properties/{hotel_id}/check-ban/{guest_id}")
async def check_guest_ban(
    hotel_id: int,
    guest_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.check_guest_banned(hotel_id, guest_id)


@router.post("/bans/{ban_id}/revoke")
async def revoke_ban(
    ban_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    result = await svc.revoke_ban(ban_id, current_user.id)
    await db.commit()
    return result


# ═══════════════════════════════════════════════════════════════════
# Safety & Compliance (Güvenlik, Yangın, İnşaat, Denetim)
# ═══════════════════════════════════════════════════════════════════

@router.put("/properties/{hotel_id}/building-info")
async def update_building_info(
    hotel_id: int,
    year_built: int = Query(None),
    architect: str = Query(None),
    contractor: str = Query(None),
    construction_company: str = Query(None),
    building_type: str = Query(None),
    number_of_floors: int = Query(None),
    has_elevator: bool = Query(None),
    has_generator: bool = Query(None),
    has_parking: bool = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.save_building_info(hotel_id, {
        "year_built": year_built, "architect": architect,
        "contractor": contractor, "construction_company": construction_company,
        "building_type": building_type, "number_of_floors": number_of_floors,
        "has_elevator": has_elevator, "has_generator": has_generator,
        "has_parking": has_parking,
    })
    await db.commit()
    return result


@router.put("/properties/{hotel_id}/fire-safety")
async def update_fire_safety(
    hotel_id: int,
    has_sprinkler: bool = Query(None),
    has_fire_alarm: bool = Query(None),
    has_fire_extinguisher: bool = Query(None),
    has_fire_escape: bool = Query(None),
    installation_company: str = Query(None),
    last_service_date: str = Query(None),
    next_service_date: str = Query(None),
    certificate_number: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.save_fire_safety(hotel_id, {
        "has_sprinkler": has_sprinkler, "has_fire_alarm": has_fire_alarm,
        "has_fire_extinguisher": has_fire_extinguisher, "has_fire_escape": has_fire_escape,
        "installation_company": installation_company,
        "last_service_date": last_service_date, "next_service_date": next_service_date,
        "certificate_number": certificate_number,
    })
    await db.commit()
    return result


@router.put("/properties/{hotel_id}/security-systems")
async def update_security_systems(
    hotel_id: int,
    has_cctv: bool = Query(None),
    has_alarm: bool = Query(None),
    has_security_personnel: bool = Query(None),
    has_room_safe: bool = Query(None),
    has_smoke_detector: bool = Query(None),
    installation_company: str = Query(None),
    verification_company: str = Query(None),
    verification_date: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.save_security_system(hotel_id, {
        "has_cctv": has_cctv, "has_alarm": has_alarm,
        "has_security_personnel": has_security_personnel,
        "has_room_safe": has_room_safe, "has_smoke_detector": has_smoke_detector,
        "installation_company": installation_company,
        "verification_company": verification_company,
        "verification_date": verification_date,
    })
    await db.commit()
    return result


@router.post("/properties/{hotel_id}/inspections", status_code=201)
async def add_inspection(
    hotel_id: int,
    inspection_type: str = Query(...),
    inspector_name: str = Query(None),
    inspector_organization: str = Query(None),
    inspection_date: str = Query(...),
    result: str = Query(None),
    valid_until: str = Query(None),
    findings: str = Query(None),
    document_url: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.add_inspection(hotel_id, {
        "inspection_type": inspection_type,
        "inspector_name": inspector_name,
        "inspector_organization": inspector_organization,
        "inspection_date": inspection_date,
        "result": result, "valid_until": valid_until,
        "findings": findings, "document_url": document_url,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/safety-compliance")
async def get_safety_compliance(
    hotel_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    return await svc.get_safety_compliance(hotel_id)


# ═══════════════════════════════════════════════════════════════════
# Nearby Places
# ═══════════════════════════════════════════════════════════════════

@router.post("/properties/{hotel_id}/nearby", status_code=201)
async def add_nearby_place(
    hotel_id: int,
    name: str = Query(...),
    category: str = Query(...),
    distance_km: float = Query(None),
    lat: float = Query(None),
    lng: float = Query(None),
    description: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await get_hotel_owner_check(hotel_id, current_user, db)
    svc = get_service(db)
    result = await svc.add_nearby_place(hotel_id, {
        "name": name, "category": category, "distance_km": distance_km,
        "lat": lat, "lng": lng, "description": description,
    })
    await db.commit()
    return result


@router.get("/properties/{hotel_id}/nearby")
async def list_nearby_places(
    hotel_id: int,
    category: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    places = await svc.repo.list_nearby_places(hotel_id, category)
    return [svc._format_nearby_place(p) for p in places]


# ═══════════════════════════════════════════════════════════════════
# Review Photos
# ═══════════════════════════════════════════════════════════════════

@router.post("/reviews/{review_id}/photos", status_code=201)
async def add_review_photo(
    review_id: int,
    url: str = Query(...),
    caption: str = Query(None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    photo = await svc.repo.add_review_photo(review_id, url, caption)
    await db.commit()
    return {"id": photo.id, "url": photo.url, "caption": photo.caption}


@router.get("/reviews/{review_id}/photos")
async def list_review_photos(
    review_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = get_service(db)
    photos = await svc.repo.list_review_photos(review_id)
    return [{"id": p.id, "url": p.url, "caption": p.caption} for p in photos]
