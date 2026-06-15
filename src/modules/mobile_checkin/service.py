from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.mobile_checkin import repository as repo
from src.modules.accommodation.models import Booking
from src.modules.hotel.models import Hotel, RoomType


async def start_mobile_checkin(db: AsyncSession, booking_id: int, checkin_data: dict) -> dict:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise ValueError("Booking not found")

    if booking.status != "confirmed":
        raise ValueError("Booking must be confirmed to start check-in")

    checkin = await repo.create_checkin_request(
        db=db,
        booking_id=booking_id,
        guest_id=booking.user_id,
        hotel_id=booking.hotel_id,
        checkin_data=checkin_data,
    )
    return {"checkin_id": checkin.id, "status": checkin.status, "message": "Check-in request created"}


async def verify_guest(db: AsyncSession, checkin_id: int, verified_by: int) -> dict:
    checkin = await repo.get_checkin_by_id(db, checkin_id)
    if not checkin:
        raise ValueError("Check-in request not found")
    if checkin.status != "pending":
        raise ValueError("Check-in is not in pending status")

    checkin = await repo.verify_checkin_request(db, checkin_id, verified_by)
    return {"checkin_id": checkin.id, "status": checkin.status, "message": "Guest verified successfully"}


async def complete_checkin(db: AsyncSession, checkin_id: int) -> dict:
    checkin = await repo.get_checkin_by_id(db, checkin_id)
    if not checkin:
        raise ValueError("Check-in request not found")
    if checkin.status != "verified":
        raise ValueError("Check-in must be verified before completion")

    result = await db.execute(select(Booking).where(Booking.id == checkin.booking_id))
    booking = result.scalar_one_or_none()

    result = await db.execute(select(RoomType).where(RoomType.id == booking.room_type_id))
    room_type = result.scalar_one_or_none()

    checkin = await repo.complete_checkin(db, checkin_id)

    key = await repo.generate_digital_key(
        db=db,
        booking_id=checkin.booking_id,
        hotel_id=checkin.hotel_id,
        room_type_id=booking.room_type_id,
        guest_id=checkin.guest_id,
        room_number=booking.room_number,
    )

    booking.status = "checked_in"
    await db.commit()

    return {
        "checkin_id": checkin.id,
        "status": checkin.status,
        "key_id": key.id,
        "key_code": key.key_code,
        "qr_code": key.qr_code,
        "message": "Check-in completed, digital key generated",
    }


async def check_out(db: AsyncSession, booking_id: int) -> dict:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise ValueError("Booking not found")

    keys = await repo.expire_booking_keys(db, booking_id)
    booking.status = "checked_out"
    await db.commit()

    return {
        "booking_id": booking_id,
        "expired_keys": len(keys),
        "status": booking.status,
        "message": "Checked out successfully, keys expired",
    }


async def request_early_checkin(db: AsyncSession, booking_id: int, requested_time) -> dict:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise ValueError("Booking not found")

    req = await repo.create_early_checkin_request(db, booking_id, requested_time)
    return {"request_id": req.id, "status": "pending", "message": "Early check-in request submitted"}


async def request_late_checkout(db: AsyncSession, booking_id: int, requested_time) -> dict:
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if not booking:
        raise ValueError("Booking not found")

    req = await repo.create_late_checkout_request(db, booking_id, requested_time)
    return {"request_id": req.id, "status": "pending", "message": "Late checkout request submitted"}


async def get_guest_keys(db: AsyncSession, guest_id: int) -> list:
    keys = await repo.get_guest_keys(db, guest_id)
    return [
        {
            "id": k.id,
            "hotel_id": k.hotel_id,
            "room_number": k.room_number,
            "key_code": k.key_code,
            "qr_code": k.qr_code,
            "status": k.status,
            "valid_from": k.valid_from.isoformat(),
            "valid_until": k.valid_until.isoformat(),
        }
        for k in keys
    ]
