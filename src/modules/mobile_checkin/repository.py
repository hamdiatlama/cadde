import secrets
from datetime import datetime, timezone, timedelta

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.mobile_checkin.models import DigitalKey, MobileCheckin, EarlyCheckinRequest, LateCheckoutRequest


async def generate_digital_key(db: AsyncSession, booking_id: int, hotel_id: int, room_type_id: int, guest_id: int, room_number: str = None, valid_days: int = 1) -> DigitalKey:
    key_code = secrets.token_hex(32)
    qr_code = f"https://api.webplatform.app/keys/{key_code}"
    now = datetime.now(timezone.utc)
    key = DigitalKey(
        booking_id=booking_id,
        hotel_id=hotel_id,
        room_type_id=room_type_id,
        room_number=room_number,
        guest_id=guest_id,
        key_code=key_code,
        qr_code=qr_code,
        status="active",
        valid_from=now,
        valid_until=now + timedelta(days=valid_days),
        issued_at=now,
    )
    db.add(key)
    await db.commit()
    await db.refresh(key)
    return key


async def validate_key(db: AsyncSession, key_code: str) -> DigitalKey | None:
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(DigitalKey).where(
            and_(
                DigitalKey.key_code == key_code,
                DigitalKey.status == "active",
                DigitalKey.valid_from <= now,
                DigitalKey.valid_until >= now,
            )
        )
    )
    return result.scalar_one_or_none()


async def revoke_key(db: AsyncSession, key_id: int) -> DigitalKey | None:
    result = await db.execute(select(DigitalKey).where(DigitalKey.id == key_id))
    key = result.scalar_one_or_none()
    if key:
        key.status = "revoked"
        await db.commit()
        await db.refresh(key)
    return key


async def get_booking_keys(db: AsyncSession, booking_id: int) -> list[DigitalKey]:
    result = await db.execute(
        select(DigitalKey).where(DigitalKey.booking_id == booking_id).order_by(DigitalKey.created_at.desc())
    )
    return result.scalars().all()


async def get_guest_keys(db: AsyncSession, guest_id: int) -> list[DigitalKey]:
    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(DigitalKey).where(
            and_(
                DigitalKey.guest_id == guest_id,
                DigitalKey.status == "active",
                DigitalKey.valid_until >= now,
            )
        ).order_by(DigitalKey.valid_until.asc())
    )
    return result.scalars().all()


async def create_checkin_request(db: AsyncSession, booking_id: int, guest_id: int, hotel_id: int, checkin_data: dict) -> MobileCheckin:
    checkin = MobileCheckin(
        booking_id=booking_id,
        guest_id=guest_id,
        hotel_id=hotel_id,
        checkin_data=checkin_data,
        status="pending",
        id_verified=False,
    )
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    return checkin


async def verify_checkin_request(db: AsyncSession, checkin_id: int, verified_by: int) -> MobileCheckin | None:
    result = await db.execute(select(MobileCheckin).where(MobileCheckin.id == checkin_id))
    checkin = result.scalar_one_or_none()
    if checkin:
        checkin.id_verified = True
        checkin.verified_by = verified_by
        checkin.status = "verified"
        await db.commit()
        await db.refresh(checkin)
    return checkin


async def complete_checkin(db: AsyncSession, checkin_id: int) -> MobileCheckin | None:
    result = await db.execute(select(MobileCheckin).where(MobileCheckin.id == checkin_id))
    checkin = result.scalar_one_or_none()
    if checkin:
        checkin.status = "completed"
        checkin.checked_in_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(checkin)
    return checkin


async def list_checkins(db: AsyncSession, hotel_id: int, status: str = None) -> list[MobileCheckin]:
    query = select(MobileCheckin).where(MobileCheckin.hotel_id == hotel_id)
    if status:
        query = query.where(MobileCheckin.status == status)
    query = query.order_by(MobileCheckin.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


async def expire_booking_keys(db: AsyncSession, booking_id: int) -> list[DigitalKey]:
    result = await db.execute(select(DigitalKey).where(DigitalKey.booking_id == booking_id))
    keys = result.scalars().all()
    for key in keys:
        key.status = "expired"
    await db.commit()
    return keys


async def create_early_checkin_request(db: AsyncSession, booking_id: int, requested_time) -> EarlyCheckinRequest:
    req = EarlyCheckinRequest(booking_id=booking_id, requested_time=requested_time)
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def create_late_checkout_request(db: AsyncSession, booking_id: int, requested_time) -> LateCheckoutRequest:
    req = LateCheckoutRequest(booking_id=booking_id, requested_time=requested_time)
    db.add(req)
    await db.commit()
    await db.refresh(req)
    return req


async def get_checkin_by_id(db: AsyncSession, checkin_id: int) -> MobileCheckin | None:
    result = await db.execute(select(MobileCheckin).where(MobileCheckin.id == checkin_id))
    return result.scalar_one_or_none()


async def get_digital_key_by_id(db: AsyncSession, key_id: int) -> DigitalKey | None:
    result = await db.execute(select(DigitalKey).where(DigitalKey.id == key_id))
    return result.scalar_one_or_none()
