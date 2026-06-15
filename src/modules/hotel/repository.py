import random
import string
from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func, update, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import case
from src.modules.hotel.models import (
    Hotel, HotelAmenity, HotelPhoto, RoomType, RoomAmenity, RoomPhoto,
    SeasonalPrice, Booking, RoomAvailability, HotelReview,
    ServiceCategory, PropertyService,
    HotelStatus, BookingStatus, PropertyType, PhotoCategory,
)
from src.modules.accommodation.models import PropertyDocument


def _generate_booking_no() -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"HTL-{suffix}"


class HotelRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_hotel(self, data: dict) -> Hotel:
        slug = data.get("name", "").lower().replace(" ", "-")
        slug = "".join(c for c in slug if c.isalnum() or c == "-").strip("-")
        hotel = Hotel(slug=slug, **data)
        self.db.add(hotel)
        return hotel

    async def get_hotel(self, hotel_id: int) -> Hotel | None:
        r = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        return r.scalar_one_or_none()

    async def get_hotel_by_slug(self, slug: str) -> Hotel | None:
        r = await self.db.execute(select(Hotel).where(Hotel.slug == slug))
        return r.scalar_one_or_none()

    async def list_hotels(self, city=None, min_star=None, max_price=None, amenities=None, guests=None, check_in=None, check_out=None, property_type=None, sort_by="created_at", page=1, per_page=20):
        query = select(Hotel).where(Hotel.status == HotelStatus.ACTIVE)
        if city:
            query = query.where(Hotel.city.ilike(f"%{city}%"))
        if min_star is not None:
            query = query.where(Hotel.star_rating >= min_star)
        if property_type:
            if isinstance(property_type, str):
                query = query.where(Hotel.property_type == property_type)
            else:
                query = query.where(Hotel.property_type.in_(property_type))

        has_extra_filters = any([
            max_price is not None, guests is not None, amenities,
            check_in is not None and check_out is not None,
        ])

        if not has_extra_filters:
            count_q = select(func.count()).select_from(query.subquery())
            total = (await self.db.execute(count_q)).scalar()
            if sort_by == "rating":
                query = query.order_by(Hotel.rating.desc(), Hotel.review_count.desc())
            elif sort_by == "review_count":
                query = query.order_by(Hotel.review_count.desc())
            elif sort_by == "popular":
                subq = select(PropertyService.hotel_id, func.count(PropertyService.id).label("sc")).where(
                    PropertyService.is_active == True
                ).group_by(PropertyService.hotel_id).subquery()
                query = query.outerjoin(subq, Hotel.id == subq.c.hotel_id)
                query = query.order_by(
                    func.coalesce(subq.c.sc, 0).desc(),
                    Hotel.rating.desc(),
                    Hotel.review_count.desc(),
                )
            elif sort_by == "featured":
                subq = select(PropertyService.hotel_id, func.count(PropertyService.id).label("sc")).where(
                    PropertyService.is_active == True
                ).group_by(PropertyService.hotel_id).subquery()
                query = query.outerjoin(subq, Hotel.id == subq.c.hotel_id)
                doc_q = select(PropertyDocument.hotel_id, func.count(PropertyDocument.id).label("dc")).where(
                    PropertyDocument.is_verified == True
                ).group_by(PropertyDocument.hotel_id).subquery()
                query = query.outerjoin(doc_q, Hotel.id == doc_q.c.hotel_id).reset_joinpoint()
                query = query.order_by(
                    func.coalesce(subq.c.sc, 0).desc(),
                    func.coalesce(doc_q.c.dc, 0).desc(),
                    Hotel.rating.desc(),
                    Hotel.review_count.desc(),
                )
            elif sort_by == "price_asc":
                query = query.order_by(Hotel.id.asc())
            elif sort_by == "price_desc":
                query = query.order_by(Hotel.id.desc())
            else:
                query = query.order_by(Hotel.created_at.desc())
            query = query.offset((page - 1) * per_page).limit(per_page)
            r = await self.db.execute(query)
            return list(r.scalars().all()), total

        r = await self.db.execute(query)
        hotels = list(r.scalars().all())
        filtered = []
        for hotel in hotels:
            if not await self._hotel_matches_filters(hotel.id, max_price, guests, amenities, check_in, check_out):
                continue
            filtered.append(hotel)
        if sort_by == "rating":
            filtered.sort(key=lambda h: h.rating or 0, reverse=True)
        elif sort_by == "review_count":
            filtered.sort(key=lambda h: h.review_count or 0, reverse=True)
        total = len(filtered)
        start = (page - 1) * per_page
        return filtered[start:start + per_page], total

    async def _hotel_matches_filters(self, hotel_id, max_price, guests, amenities, check_in, check_out) -> bool:
        if max_price is not None:
            r = await self.db.execute(
                select(func.count(RoomType.id)).where(
                    RoomType.hotel_id == hotel_id, RoomType.is_active == True,
                    RoomType.base_price <= max_price,
                )
            )
            if r.scalar() == 0:
                return False
        if guests is not None:
            r = await self.db.execute(
                select(func.count(RoomType.id)).where(
                    RoomType.hotel_id == hotel_id, RoomType.is_active == True,
                    RoomType.max_guests >= guests,
                )
            )
            if r.scalar() == 0:
                return False
        if amenities:
            for amenity in amenities:
                r = await self.db.execute(
                    select(func.count(HotelAmenity.id)).where(
                        HotelAmenity.hotel_id == hotel_id,
                        HotelAmenity.name.ilike(f"%{amenity}%"),
                    )
                )
                if r.scalar() == 0:
                    return False
        if check_in and check_out:
            rt_ids = await self._get_hotel_room_type_ids(hotel_id)
            if not rt_ids:
                return False
            for rt_id in rt_ids:
                if await self._room_type_available_for_range(rt_id, check_in, check_out):
                    return True
            return False
        return True

    async def _get_hotel_room_type_ids(self, hotel_id: int) -> list[int]:
        r = await self.db.execute(
            select(RoomType.id).where(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        )
        return list(r.scalars().all())

    async def _room_type_available_for_range(self, room_type_id: int, check_in, check_out) -> bool:
        bad = await self.db.execute(
            select(func.count(RoomAvailability.id)).where(
                RoomAvailability.room_type_id == room_type_id,
                RoomAvailability.date >= check_in,
                RoomAvailability.date < check_out,
                or_(
                    RoomAvailability.available_count <= 0,
                    RoomAvailability.is_blocked == True,
                ),
            )
        )
        return bad.scalar() == 0

    async def update_hotel(self, hotel_id: int, data: dict) -> Hotel | None:
        hotel = await self.get_hotel(hotel_id)
        if not hotel:
            return None
        for field, val in data.items():
            setattr(hotel, field, val)
        self.db.add(hotel)
        return hotel

    async def update_rating(self, hotel_id: int):
        r = await self.db.execute(
            select(func.avg(HotelReview.rating), func.count(HotelReview.id))
            .where(HotelReview.hotel_id == hotel_id)
        )
        avg, cnt = r.one()
        hotel = await self.get_hotel(hotel_id)
        if hotel:
            hotel.rating = round(float(avg), 2) if avg else 0.0
            hotel.review_count = cnt or 0
            self.db.add(hotel)

    async def add_amenity(self, hotel_id: int, name: str, icon: str = None) -> HotelAmenity:
        amenity = HotelAmenity(hotel_id=hotel_id, name=name, icon=icon)
        self.db.add(amenity)
        return amenity

    async def list_amenities(self, hotel_id: int) -> list[HotelAmenity]:
        r = await self.db.execute(
            select(HotelAmenity).where(HotelAmenity.hotel_id == hotel_id)
        )
        return list(r.scalars().all())

    async def add_photo(self, hotel_id: int, url: str, caption: str = None, is_main: bool = False, category: str = "exterior") -> HotelPhoto:
        if is_main:
            await self.db.execute(
                update(HotelPhoto).where(
                    HotelPhoto.hotel_id == hotel_id, HotelPhoto.is_main == True
                ).values(is_main=False)
            )
        photo = HotelPhoto(hotel_id=hotel_id, url=url, caption=caption, is_main=is_main, category=category)
        self.db.add(photo)
        return photo

    async def list_photos(self, hotel_id: int) -> list[HotelPhoto]:
        r = await self.db.execute(
            select(HotelPhoto).where(HotelPhoto.hotel_id == hotel_id).order_by(HotelPhoto.sort_order)
        )
        return list(r.scalars().all())

    async def set_main_photo(self, photo_id: int, hotel_id: int) -> HotelPhoto | None:
        r = await self.db.execute(
            select(HotelPhoto).where(HotelPhoto.id == photo_id, HotelPhoto.hotel_id == hotel_id)
        )
        photo = r.scalar_one_or_none()
        if not photo:
            return None
        await self.db.execute(
            update(HotelPhoto).where(
                HotelPhoto.hotel_id == hotel_id, HotelPhoto.is_main == True
            ).values(is_main=False)
        )
        photo.is_main = True
        self.db.add(photo)
        return photo

    async def create_room_type(self, hotel_id: int, data: dict) -> RoomType:
        room = RoomType(hotel_id=hotel_id, **data)
        self.db.add(room)
        await self.db.flush()
        today = datetime.now(timezone.utc).date()
        for i in range(365):
            day = today + timedelta(days=i)
            avail = RoomAvailability(
                room_type_id=room.id,
                date=datetime.combine(day, datetime.min.time()),
                available_count=room.quantity,
            )
            self.db.add(avail)
        return room

    async def get_room_type(self, room_type_id: int) -> RoomType | None:
        r = await self.db.execute(select(RoomType).where(RoomType.id == room_type_id))
        return r.scalar_one_or_none()

    async def list_room_types(self, hotel_id: int) -> list[RoomType]:
        r = await self.db.execute(
            select(RoomType).where(RoomType.hotel_id == hotel_id, RoomType.is_active == True)
        )
        return list(r.scalars().all())

    async def update_room_type(self, room_type_id: int, data: dict) -> RoomType | None:
        room = await self.get_room_type(room_type_id)
        if not room:
            return None
        for field, val in data.items():
            setattr(room, field, val)
        self.db.add(room)
        return room

    async def get_available_rooms(self, hotel_id: int, check_in, check_out, guests: int) -> list[RoomType]:
        r = await self.db.execute(
            select(RoomType).where(
                RoomType.hotel_id == hotel_id,
                RoomType.is_active == True,
                RoomType.max_guests >= guests,
            )
        )
        rooms = list(r.scalars().all())
        available = []
        for rm in rooms:
            if await self._room_type_available_for_range(rm.id, check_in, check_out):
                available.append(rm)
        return available

    async def set_seasonal_price(self, room_type_id: int, name: str, start_date, end_date, price: float) -> SeasonalPrice:
        sp = SeasonalPrice(
            room_type_id=room_type_id, name=name,
            start_date=start_date, end_date=end_date, price=price,
        )
        self.db.add(sp)
        return sp

    async def list_seasonal_prices(self, room_type_id: int) -> list[SeasonalPrice]:
        r = await self.db.execute(
            select(SeasonalPrice).where(
                SeasonalPrice.room_type_id == room_type_id,
                SeasonalPrice.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def get_effective_price(self, room_type_id: int, date) -> float:
        r = await self.db.execute(
            select(SeasonalPrice).where(
                SeasonalPrice.room_type_id == room_type_id,
                SeasonalPrice.is_active == True,
                SeasonalPrice.start_date <= date,
                SeasonalPrice.end_date >= date,
            ).order_by(SeasonalPrice.price.asc()).limit(1)
        )
        sp = r.scalar_one_or_none()
        if sp:
            return sp.price
        room = await self.get_room_type(room_type_id)
        return room.base_price if room else 0

    async def block_dates(self, room_type_id: int, start_date, end_date):
        current = start_date
        while current <= end_date:
            r = await self.db.execute(
                select(RoomAvailability).where(
                    RoomAvailability.room_type_id == room_type_id,
                    func.date(RoomAvailability.date) == current.date(),
                )
            )
            avail = r.scalar_one_or_none()
            if avail:
                avail.is_blocked = True
                avail.available_count = 0
                self.db.add(avail)
            current += timedelta(days=1)

    async def unblock_dates(self, room_type_id: int, start_date, end_date):
        room = await self.get_room_type(room_type_id)
        qty = room.quantity if room else 0
        current = start_date
        while current <= end_date:
            r = await self.db.execute(
                select(RoomAvailability).where(
                    RoomAvailability.room_type_id == room_type_id,
                    func.date(RoomAvailability.date) == current.date(),
                )
            )
            avail = r.scalar_one_or_none()
            if avail:
                avail.is_blocked = False
                avail.available_count = qty
                self.db.add(avail)
            current += timedelta(days=1)

    async def get_availability(self, room_type_id: int, start_date, end_date) -> list[RoomAvailability]:
        r = await self.db.execute(
            select(RoomAvailability).where(
                RoomAvailability.room_type_id == room_type_id,
                RoomAvailability.date >= start_date,
                RoomAvailability.date <= end_date,
            ).order_by(RoomAvailability.date)
        )
        return list(r.scalars().all())

    async def update_availability_on_booking(self, room_type_id: int, check_in, check_out, room_count: int):
        await self.db.execute(
            update(RoomAvailability)
            .where(
                RoomAvailability.room_type_id == room_type_id,
                RoomAvailability.date >= check_in,
                RoomAvailability.date < check_out,
                RoomAvailability.is_blocked == False,
            )
            .values(available_count=RoomAvailability.available_count - room_count)
        )

    async def restore_availability_on_cancel(self, booking: Booking):
        await self.db.execute(
            update(RoomAvailability)
            .where(
                RoomAvailability.room_type_id == booking.room_type_id,
                RoomAvailability.date >= booking.check_in,
                RoomAvailability.date < booking.check_out,
            )
            .values(available_count=RoomAvailability.available_count + booking.room_count)
        )

    async def create_booking(self, data: dict) -> Booking:
        booking = Booking(booking_no=_generate_booking_no(), **data)
        self.db.add(booking)
        await self.db.flush()
        await self.update_availability_on_booking(
            booking.room_type_id, booking.check_in, booking.check_out, booking.room_count,
        )
        return booking

    async def get_booking(self, booking_id: int) -> Booking | None:
        r = await self.db.execute(select(Booking).where(Booking.id == booking_id))
        return r.scalar_one_or_none()

    async def get_booking_by_no(self, booking_no: str) -> Booking | None:
        r = await self.db.execute(select(Booking).where(Booking.booking_no == booking_no))
        return r.scalar_one_or_none()

    async def list_hotel_bookings(self, hotel_id: int, status=None, page=1, per_page=20):
        query = select(Booking).where(Booking.hotel_id == hotel_id)
        if status:
            query = query.where(Booking.status == status)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(Booking.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def list_user_bookings(self, user_id: int, page=1, per_page=20):
        query = select(Booking).where(Booking.user_id == user_id)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(Booking.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def update_booking_status(self, booking_id: int, status: BookingStatus) -> Booking | None:
        booking = await self.get_booking(booking_id)
        if not booking:
            return None
        if status == BookingStatus.CANCELLED and booking.status != BookingStatus.CANCELLED:
            await self.restore_availability_on_cancel(booking)
            booking.cancelled_at = datetime.now(timezone.utc)
        booking.status = status
        self.db.add(booking)
        return booking

    async def check_availability(self, room_type_id: int, check_in, check_out, room_count: int) -> bool:
        bad = await self.db.execute(
            select(func.count(RoomAvailability.id)).where(
                RoomAvailability.room_type_id == room_type_id,
                RoomAvailability.date >= check_in,
                RoomAvailability.date < check_out,
                or_(
                    RoomAvailability.available_count < room_count,
                    RoomAvailability.is_blocked == True,
                ),
            )
        )
        return bad.scalar() == 0

    async def create_review(self, hotel_id: int, user_id: int, booking_id: int, data: dict) -> HotelReview:
        review = HotelReview(hotel_id=hotel_id, user_id=user_id, booking_id=booking_id, **data)
        self.db.add(review)
        return review

    async def list_reviews(self, hotel_id: int, page=1, per_page=20):
        query = select(HotelReview).where(HotelReview.hotel_id == hotel_id)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(HotelReview.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    # ─── Service Categories (Klik/Tag Sistemi) ──────────────────

    async def list_service_categories(self) -> list[ServiceCategory]:
        r = await self.db.execute(
            select(ServiceCategory).where(ServiceCategory.is_active == True)
            .order_by(ServiceCategory.sort_order)
        )
        return list(r.scalars().all())

    async def create_service_category(self, name: str, icon: str = None, sort_order: int = 0) -> ServiceCategory:
        cat = ServiceCategory(name=name, icon=icon, sort_order=sort_order)
        self.db.add(cat)
        return cat

    async def add_property_service(self, hotel_id: int, category_id: int, name: str, icon: str = None, description: str = None, is_free: bool = True, price: float = None) -> PropertyService:
        ps = PropertyService(hotel_id=hotel_id, category_id=category_id, name=name, icon=icon, description=description, is_free=is_free, price=price)
        self.db.add(ps)
        return ps

    async def list_property_services(self, hotel_id: int) -> list[PropertyService]:
        r = await self.db.execute(
            select(PropertyService).where(
                PropertyService.hotel_id == hotel_id,
                PropertyService.is_active == True,
            )
        )
        return list(r.scalars().all())

    async def remove_property_service(self, service_id: int) -> bool:
        r = await self.db.execute(
            select(PropertyService).where(PropertyService.id == service_id)
        )
        ps = r.scalar_one_or_none()
        if not ps:
            return False
        ps.is_active = False
        self.db.add(ps)
        return True

    async def get_property_services_grouped(self, hotel_id: int) -> dict:
        services = await self.list_property_services(hotel_id)
        categories = await self.list_service_categories()
        result = {}
        for cat in categories:
            items = [s for s in services if s.category_id == cat.id]
            if items:
                result[cat.name] = {
                    "icon": cat.icon,
                    "services": [
                        {"id": s.id, "name": s.name, "icon": s.icon,
                         "description": s.description, "is_free": s.is_free, "price": s.price}
                        for s in items
                    ],
                }
        return result

    async def get_hotel_rating(self, hotel_id: int) -> dict:
        r = await self.db.execute(
            select(
                func.avg(HotelReview.rating),
                func.count(HotelReview.id),
                func.avg(HotelReview.cleanliness),
                func.avg(HotelReview.comfort),
                func.avg(HotelReview.location_score),
                func.avg(HotelReview.staff_score),
                func.avg(HotelReview.value_score),
            ).where(HotelReview.hotel_id == hotel_id)
        )
        avg_rating, count, cleanliness, comfort, location, staff, value = r.one()
        return {
            "average_rating": round(float(avg_rating), 2) if avg_rating else 0,
            "review_count": count or 0,
            "cleanliness": round(float(cleanliness), 2) if cleanliness else 0,
            "comfort": round(float(comfort), 2) if comfort else 0,
            "location": round(float(location), 2) if location else 0,
            "staff": round(float(staff), 2) if staff else 0,
            "value": round(float(value), 2) if value else 0,
        }
