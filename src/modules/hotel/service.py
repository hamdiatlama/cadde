from datetime import datetime, timedelta, timezone
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.hotel.repository import HotelRepository
from src.modules.hotel.models import BookingStatus, Hotel


class HotelService:
    def __init__(self, db: AsyncSession):
        self.repo = HotelRepository(db)

    async def search_hotels(self, filters: dict) -> tuple[list[dict], int]:
        hotels, total = await self.repo.list_hotels(**filters)
        result = []
        for h in hotels:
            hotel_data = self._format_hotel(h)
            hotel_data["service_count"] = len(
                (await self.repo.list_property_services(h.id))
            )
            result.append(hotel_data)
        return result, total

    async def get_hotel_detail(self, slug: str) -> dict | None:
        hotel = await self.repo.get_hotel_by_slug(slug)
        if not hotel:
            return None
        amenities = await self.repo.list_amenities(hotel.id)
        photos = await self.repo.list_photos(hotel.id)
        room_types = await self.repo.list_room_types(hotel.id)
        rating = await self.repo.get_hotel_rating(hotel.id)
        reviews_raw, _ = await self.repo.list_reviews(hotel.id, page=1, per_page=10)
        services = await self.repo.get_property_services_grouped(hotel.id)

        room_data = []
        for rt in room_types:
            today = datetime.now(timezone.utc)
            effective_price = await self.repo.get_effective_price(rt.id, today)
            room_data.append(self._format_room_type(rt, effective_price))

        return {
            **self._format_hotel(hotel),
            "amenities": [{"id": a.id, "name": a.name, "icon": a.icon} for a in amenities],
            "photos": [{"id": p.id, "url": p.url, "caption": p.caption, "category": p.category.value if hasattr(p.category, 'value') else p.category, "is_main": p.is_main} for p in photos],
            "room_types": room_data,
            "reviews": [self._format_review(r) for r in reviews_raw],
            "rating_summary": rating,
            "services_grouped": services,
        }

    async def check_room_availability(self, hotel_id: int, check_in, check_out, guests: int) -> list[dict]:
        rooms = await self.repo.get_available_rooms(hotel_id, check_in, check_out, guests)
        result = []
        for rm in rooms:
            daily_prices = []
            current = check_in
            while current < check_out:
                price = await self.repo.get_effective_price(rm.id, current)
                daily_prices.append({"date": current.isoformat() if hasattr(current, "isoformat") else str(current), "price": price})
                current += timedelta(days=1)
            total = sum(d["price"] for d in daily_prices)
            result.append({**self._format_room_type(rm, daily_prices[0]["price"] if daily_prices else rm.base_price), "daily_prices": daily_prices, "total_price": total})
        return result

    async def calculate_booking_price(self, room_type_id: int, check_in, check_out, room_count: int) -> dict:
        room = await self.repo.get_room_type(room_type_id)
        if not room:
            raise ValueError("Room type not found")
        nights = (check_out - check_in).days
        if nights <= 0:
            raise ValueError("Invalid date range")
        total = 0.0
        breakdown = []
        current = check_in
        while current < check_out:
            price = await self.repo.get_effective_price(room_type_id, current)
            night_total = price * room_count
            total += night_total
            breakdown.append({"date": current.isoformat() if hasattr(current, "isoformat") else str(current), "unit_price": price, "room_count": room_count, "night_total": night_total})
            current += timedelta(days=1)
        return {"nights": nights, "room_count": room_count, "unit_price": room.base_price, "breakdown": breakdown, "total": total}

    async def create_booking(self, user_id: int, data: dict) -> dict:
        hotel_id = data.get("hotel_id")
        room_type_id = data.get("room_type_id")
        check_in = data.get("check_in")
        check_out = data.get("check_out")
        room_count = data.get("room_count", 1)
        guests = data.get("adults", 1) + (data.get("children", 0) or 0)

        hotel = await self.repo.get_hotel(hotel_id)
        if not hotel:
            raise ValueError("Hotel not found")

        if hotel.suspended_until and hotel.suspended_until > datetime.now(timezone.utc):
            raise ValueError(f"Hotel is suspended until {hotel.suspended_until.date()}")

        from src.modules.accommodation.repository import AccommodationRepository
        acc_repo = AccommodationRepository(self.repo.db)
        if await acc_repo.is_guest_banned(hotel_id, user_id):
            raise ValueError("You are banned from booking at this property")
        room = await self.repo.get_room_type(room_type_id)
        if not room or room.hotel_id != hotel_id:
            raise ValueError("Room type not found")
        if room.max_guests * room_count < guests:
            raise ValueError("Room capacity insufficient for guest count")
        available = await self.repo.check_availability(room_type_id, check_in, check_out, room_count)
        if not available:
            raise ValueError("Rooms not available for the selected dates")

        nights = (check_out - check_in).days
        price_info = await self.calculate_booking_price(room_type_id, check_in, check_out, room_count)

        booking_data = {
            "hotel_id": hotel_id,
            "room_type_id": room_type_id,
            "user_id": user_id,
            "guest_name": data.get("guest_name"),
            "guest_email": data.get("guest_email"),
            "guest_phone": data.get("guest_phone"),
            "check_in": check_in,
            "check_out": check_out,
            "nights": nights,
            "adults": data.get("adults", 1),
            "children": data.get("children", 0),
            "room_count": room_count,
            "unit_price": room.base_price,
            "total_price": price_info["total"],
            "special_requests": data.get("special_requests"),
        }
        booking = await self.repo.create_booking(booking_data)
        return self._format_booking(booking)

    async def cancel_booking(self, booking_id: int, user_id: int) -> dict:
        booking = await self.repo.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")
        if booking.status in (BookingStatus.CANCELLED, BookingStatus.CHECKED_OUT):
            raise ValueError(f"Booking is already {booking.status.value}")
        booking = await self.repo.update_booking_status(booking_id, BookingStatus.CANCELLED)
        return self._format_booking(booking)

    async def add_review(self, user_id: int, booking_id: int, data: dict) -> dict:
        booking = await self.repo.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")
        if booking.status != BookingStatus.CHECKED_OUT:
            raise ValueError("Can only review after check-out")
        hotel_id = booking.hotel_id
        review = await self.repo.create_review(hotel_id, user_id, booking_id, data)
        await self.repo.update_rating(hotel_id)
        return self._format_review(review)

    # ─── Service Tags (Klik/Tag Sistemi) ────────────────────────

    async def list_service_categories(self) -> list[dict]:
        cats = await self.repo.list_service_categories()
        return [{"id": c.id, "name": c.name, "icon": c.icon} for c in cats]

    async def add_property_service(self, hotel_id: int, category_id: int, name: str, icon: str = None, description: str = None, is_free: bool = True, price: float = None) -> dict:
        ps = await self.repo.add_property_service(hotel_id, category_id, name, icon, description, is_free, price)
        return {
            "id": ps.id, "hotel_id": ps.hotel_id, "category_id": ps.category_id,
            "name": ps.name, "icon": ps.icon, "description": ps.description,
            "is_free": ps.is_free, "price": ps.price,
        }

    async def get_property_services(self, hotel_id: int) -> dict:
        return await self.repo.get_property_services_grouped(hotel_id)

    async def remove_property_service(self, service_id: int) -> bool:
        return await self.repo.remove_property_service(service_id)

    # ─── Missing router helpers ─────────────────────────────────

    async def get_hotel_by_slug(self, slug: str):
        return await self.repo.get_hotel_by_slug(slug)

    async def get_hotel_by_id(self, hotel_id: int):
        return await self.repo.get_hotel(hotel_id)

    async def get_available_rooms(self, hotel_id: int, check_in, check_out, guests: int):
        return await self.check_room_availability(hotel_id, check_in, check_out, guests)

    async def list_hotel_reviews(self, hotel_id: int, page=1, per_page=20):
        reviews, total = await self.repo.list_reviews(hotel_id, page, per_page)
        return [self._format_review(r) for r in reviews], total

    async def calculate_price(self, hotel_id: int, room_type_id: int, check_in, check_out, room_count: int):
        return await self.calculate_booking_price(room_type_id, check_in, check_out, room_count)

    async def get_booking_by_no(self, booking_no: str):
        return await self.repo.get_booking_by_no(booking_no)

    async def get_booking_detail(self, booking_id: int):
        booking = await self.repo.get_booking(booking_id)
        if not booking:
            return None
        return self._format_booking(booking)

    async def list_user_bookings(self, user_id: int, page=1, per_page=20):
        bookings, total = await self.repo.list_user_bookings(user_id, page, per_page)
        return [self._format_booking(b) for b in bookings], total

    async def create_hotel(self, owner_id: int, **kwargs):
        data = {"owner_id": owner_id, **{k: v for k, v in kwargs.items() if v is not None}}
        lat = data.get("lat")
        lng = data.get("lng")
        city = data.get("city")
        address = data.get("address")
        if lat and lng:
            from src.modules.accommodation.repository import AccommodationRepository
            acc_repo = AccommodationRepository(self.repo.db)
            nearby = await acc_repo.find_hotels_near_location(lat, lng)
            if nearby:
                data["requires_location_approval"] = True
                data["original_location_id"] = nearby[0].id
        hotel = await self.repo.create_hotel(data)
        await self.repo.db.flush()
        if data.get("requires_location_approval") and nearby:
            try:
                from src.modules.accommodation.models import LocationRegistrationRequest
                req = LocationRegistrationRequest(
                    hotel_id=hotel.id,
                    existing_hotel_id=nearby[0].id,
                    requester_id=owner_id,
                    reason=f"'{data.get('name', '')}' aynı lokasyonda '{nearby[0].name}' mevcut",
                    status="pending",
                )
                self.repo.db.add(req)
            except Exception:
                pass
        return self._format_hotel(hotel)

    async def update_hotel(self, hotel_id: int, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        hotel = await self.repo.update_hotel(hotel_id, data)
        if not hotel:
            return None
        await self.repo.db.flush()
        return self._format_hotel(hotel)

    async def get_availability_calendar(self, room_type_id: int, start_date, end_date):
        avail = await self.repo.get_availability(room_type_id, start_date, end_date)
        return [{"date": a.date.isoformat() if a.date else None, "available_count": a.available_count, "is_blocked": a.is_blocked, "price_override": a.price_override} for a in avail]

    async def list_hotel_bookings(self, hotel_id: int, status=None, page=1, per_page=20):
        bookings, total = await self.repo.list_hotel_bookings(hotel_id, status, page, per_page)
        return [self._format_booking(b) for b in bookings], total

    async def update_booking_status(self, booking_id: int, status: str):
        s = BookingStatus(status)
        booking = await self.repo.update_booking_status(booking_id, s)
        if not booking:
            return None
        return self._format_booking(booking)

    async def get_booking_by_id(self, booking_id: int):
        return await self.repo.get_booking(booking_id)

    async def list_all_hotels(self, city=None, status=None, min_rating=None, page=1, per_page=20):
        query = select(Hotel)
        if city:
            query = query.where(Hotel.city.ilike(f"%{city}%"))
        if status:
            query = query.where(Hotel.status == status)
        if min_rating is not None:
            query = query.where(Hotel.rating >= min_rating)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.repo.db.execute(count_q)).scalar()
        query = query.order_by(Hotel.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        r = await self.repo.db.execute(query)
        hotels = list(r.scalars().all())
        return [self._format_hotel(h) for h in hotels], total

    async def block_dates(self, room_type_id: int, start_date, end_date):
        await self.repo.block_dates(room_type_id, start_date, end_date)
        return {"ok": True}

    async def unblock_dates(self, room_type_id: int, start_date, end_date):
        await self.repo.unblock_dates(room_type_id, start_date, end_date)
        return {"ok": True}

    async def add_amenity(self, hotel_id: int, name: str, icon: str = None):
        a = await self.repo.add_amenity(hotel_id, name, icon)
        return {"id": a.id, "name": a.name, "icon": a.icon}

    async def add_photo(self, hotel_id: int, url: str, caption: str = None, is_main: bool = False, category: str = "exterior"):
        photo = await self.repo.add_photo(hotel_id, url, caption, is_main, category)
        return {"id": photo.id, "url": photo.url, "caption": photo.caption, "category": category, "is_main": photo.is_main}

    async def set_main_photo(self, hotel_id: int, photo_id: int):
        photo = await self.repo.set_main_photo(photo_id, hotel_id)
        if not photo:
            return None
        return {"id": photo.id, "url": photo.url, "is_main": photo.is_main}

    async def create_room_type(self, hotel_id: int, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        room = await self.repo.create_room_type(hotel_id, data)
        await self.repo.db.flush()
        return self._format_room_type(room)

    async def update_room_type(self, room_type_id: int, **kwargs):
        data = {k: v for k, v in kwargs.items() if v is not None}
        room = await self.repo.update_room_type(room_type_id, data)
        if not room:
            return None
        await self.repo.db.flush()
        return self._format_room_type(room)

    async def list_room_types(self, hotel_id: int):
        rooms = await self.repo.list_room_types(hotel_id)
        return [self._format_room_type(r) for r in rooms]

    async def set_seasonal_price(self, room_type_id: int, name: str = None, start_date=None, end_date=None, price: float = 0):
        sp = await self.repo.set_seasonal_price(room_type_id, name, start_date, end_date, price)
        return {"id": sp.id, "room_type_id": sp.room_type_id, "name": sp.name, "start_date": sp.start_date.isoformat() if sp.start_date else None, "end_date": sp.end_date.isoformat() if sp.end_date else None, "price": sp.price}

    # ─── Photo helpers ───────────────────────────────────────────

    async def add_photo_with_category(self, hotel_id: int, url: str, caption: str = None, category: str = "exterior", is_main: bool = False) -> dict:
        photo = await self.repo.add_photo(hotel_id, url, caption, is_main)
        return {
            "id": photo.id, "url": photo.url, "caption": photo.caption,
            "category": category, "is_main": photo.is_main,
        }

    def _format_hotel(self, hotel) -> dict:
        return {
            "id": hotel.id,
            "owner_id": hotel.owner_id,
            "name": hotel.name,
            "slug": hotel.slug,
            "description": hotel.description,
            "property_type": hotel.property_type.value if hotel.property_type else None,
            "listing_type": hotel.listing_type.value if hotel.listing_type else None,
            "star_rating": hotel.star_rating,
            "address": hotel.address,
            "city": hotel.city,
            "country": hotel.country,
            "lat": hotel.lat,
            "lng": hotel.lng,
            "phone": hotel.phone,
            "email": hotel.email,
            "website": hotel.website,
            "tax_id": hotel.tax_id,
            "company_name": hotel.company_name,
            "company_description": hotel.company_description,
            "check_in_time": hotel.check_in_time,
            "check_out_time": hotel.check_out_time,
            "house_rules": hotel.house_rules,
            "cancellation_policy": hotel.cancellation_policy,
            "status": hotel.status.value if hotel.status else None,
            "rating": hotel.rating,
            "review_count": hotel.review_count,
            "created_at": hotel.created_at.isoformat() if hotel.created_at else None,
        }

    def _format_room_type(self, rt, effective_price: float = None) -> dict:
        return {
            "id": rt.id,
            "hotel_id": rt.hotel_id,
            "name": rt.name,
            "description": rt.description,
            "max_guests": rt.max_guests,
            "bed_type": rt.bed_type,
            "size_sqm": rt.size_sqm,
            "quantity": rt.quantity,
            "base_price": rt.base_price,
            "effective_price": effective_price or rt.base_price,
            "is_active": rt.is_active,
        }

    def _format_booking(self, booking) -> dict:
        return {
            "id": booking.id,
            "booking_no": booking.booking_no,
            "hotel_id": booking.hotel_id,
            "room_type_id": booking.room_type_id,
            "user_id": booking.user_id,
            "guest_name": booking.guest_name,
            "guest_email": booking.guest_email,
            "guest_phone": booking.guest_phone,
            "check_in": booking.check_in.isoformat() if booking.check_in else None,
            "check_out": booking.check_out.isoformat() if booking.check_out else None,
            "nights": booking.nights,
            "adults": booking.adults,
            "children": booking.children,
            "room_count": booking.room_count,
            "unit_price": booking.unit_price,
            "total_price": booking.total_price,
            "status": booking.status.value if booking.status else None,
            "special_requests": booking.special_requests,
            "payment_status": booking.payment_status,
            "cancelled_at": booking.cancelled_at.isoformat() if booking.cancelled_at else None,
            "created_at": booking.created_at.isoformat() if booking.created_at else None,
        }

    def _format_review(self, review) -> dict:
        return {
            "id": review.id,
            "hotel_id": review.hotel_id,
            "user_id": review.user_id,
            "booking_id": review.booking_id,
            "rating": review.rating,
            "comment": review.comment,
            "cleanliness": review.cleanliness,
            "comfort": review.comfort,
            "location_score": review.location_score,
            "staff_score": review.staff_score,
            "value_score": review.value_score,
            "created_at": review.created_at.isoformat() if review.created_at else None,
        }
