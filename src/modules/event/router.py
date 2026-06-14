from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.user import User
from src.core.auth import get_current_user
from src.modules.event.service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/venues", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_venue(
    name: str, city: str, district: str = None, address: str = None,
    latitude: float = None, longitude: float = None, capacity: int = 0, phone: str = None,
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.create_venue(name, city, district, address, latitude, longitude, capacity, phone)
    await db.commit()
    return result


@router.get("/venues", response_model=list[dict])
async def list_venues(db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    return await svc.list_venues()


@router.get("/venues/{venue_id}", response_model=dict)
async def get_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    result = await svc.get_venue(venue_id)
    if not result:
        raise HTTPException(status_code=404, detail="Venue not found")
    return result


@router.delete("/venues/{venue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_venue(venue_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    await svc.repo.delete_venue(venue_id)
    await db.commit()


@router.post("/venues/{venue_id}/sections", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_section(
    venue_id: int, name: str, capacity: int = 0, price_multiplier: float = 1.0,
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.create_section(venue_id, name, capacity, price_multiplier)
    await db.commit()
    return result


@router.get("/venues/{venue_id}/sections", response_model=list[dict])
async def list_sections(venue_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    return await svc.list_sections(venue_id)


@router.delete("/sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_section(section_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    await svc.delete_section(section_id)
    await db.commit()


@router.post("/events", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str, category: str, venue_id: int, description: str = None,
    poster_url: str = None, min_age: int = 0, organizer: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.create_event(title, category, venue_id, description, poster_url, min_age, organizer)
    await db.commit()
    return result


@router.get("/events", response_model=list[dict])
async def list_events(
    category: str = Query(None), venue_id: int = Query(None),
    venue_type: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    return await svc.list_events(category, venue_id, venue_type)


@router.get("/events/{event_id}", response_model=dict)
async def get_event(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    result = await svc.get_event(event_id)
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.put("/events/{event_id}/status", response_model=dict)
async def update_event_status(
    event_id: int, status: str,
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.update_event_status(event_id, status)
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    await db.commit()
    return result


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    await svc.delete_event(event_id)
    await db.commit()


@router.post("/events/{event_id}/sessions", response_model=dict, status_code=status.HTTP_201_CREATED)
async def add_session(
    event_id: int, start_time: str, end_time: str = None, is_active: bool = True,
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    from datetime import datetime
    st = datetime.fromisoformat(start_time)
    et = datetime.fromisoformat(end_time) if end_time else None
    result = await svc.create_session(event_id, st, et, is_active)
    await db.commit()
    return result


@router.get("/events/{event_id}/sessions", response_model=list[dict])
async def list_sessions(event_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    return await svc.list_sessions(event_id)


@router.post("/sessions/{session_id}/pricing", response_model=dict, status_code=status.HTTP_201_CREATED)
async def set_pricing(
    session_id: int, section_id: int, price: float, currency: str = "TRY",
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.create_session_pricing(session_id, section_id, price, currency)
    await db.commit()
    return result


@router.get("/sessions/{session_id}/pricing", response_model=list[dict])
async def get_pricing(session_id: int, db: AsyncSession = Depends(get_db)):
    svc = EventService(db)
    return await svc.get_session_pricing(session_id)


@router.post("/sessions/{session_id}/seats", response_model=list[dict], status_code=status.HTTP_201_CREATED)
async def bulk_create_seats(
    session_id: int, section_id: int, seats: list[dict],
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.create_seats_bulk(section_id, seats)
    await db.commit()
    return result


@router.get("/sessions/{session_id}/sections/{section_id}/seats/available", response_model=list[dict])
async def get_available_seats(
    session_id: int, section_id: int,
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    return await svc.get_available_seats(session_id, section_id)


@router.post("/bookings", response_model=dict, status_code=status.HTTP_201_CREATED)
async def reserve_tickets(
    session_id: int, section_id: int, seat_ids: list[int] = None, qty: int = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    try:
        result = await svc.reserve_tickets(current_user.id, session_id, section_id, seat_ids, qty)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await db.commit()
    return result


@router.get("/bookings", response_model=list[dict])
async def list_my_bookings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    return await svc.list_bookings_by_user(current_user.id)


@router.get("/bookings/{booking_id}", response_model=dict)
async def get_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    result = await svc.get_booking_detail(booking_id, current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    return result


@router.post("/bookings/{booking_id}/confirm", response_model=dict)
async def confirm_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    try:
        result = await svc.confirm_booking(booking_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    await db.commit()
    return result


@router.post("/bookings/{booking_id}/cancel", response_model=dict)
async def cancel_booking(
    booking_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    svc = EventService(db)
    try:
        result = await svc.cancel_booking(booking_id, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    await db.commit()
    return result
