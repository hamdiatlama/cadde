from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.accommodation.repository import AccommodationRepository
from src.modules.hotel.repository import HotelRepository
from src.modules.hotel.models import BookingStatus


class AccommodationService:
    def __init__(self, db: AsyncSession):
        self.repo = AccommodationRepository(db)
        self.hotel_repo = HotelRepository(db)

    # ─── Satisfaction Surveys ────────────────────────────────────

    async def submit_survey(self, user_id: int, data: dict) -> dict:
        booking = await self.hotel_repo.get_booking(data.get("booking_id"))
        if not booking:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")
        existing = await self.repo.get_survey_by_booking(booking.id)
        if existing:
            raise ValueError("Survey already submitted for this booking")
        survey_data = {
            "booking_id": booking.id,
            "hotel_id": booking.hotel_id,
            "user_id": user_id,
            "overall_score": data.get("overall_score"),
            "would_recommend": data.get("would_recommend"),
            "checkin_experience": data.get("checkin_experience"),
            "cleanliness_score": data.get("cleanliness_score"),
            "service_score": data.get("service_score"),
            "view_score": data.get("view_score"),
            "food_score": data.get("food_score"),
            "value_score": data.get("value_score"),
            "noise_score": data.get("noise_score"),
            "bed_comfort": data.get("bed_comfort"),
            "comments": data.get("comments"),
        }
        survey = await self.repo.create_survey(survey_data)
        return self._format_survey(survey)

    async def get_hotel_satisfaction(self, hotel_id: int) -> dict:
        stats = await self.repo.get_hotel_satisfaction_stats(hotel_id)
        surveys, total = await self.repo.list_hotel_surveys(hotel_id, page=1, per_page=5)
        return {
            "stats": stats,
            "recent_surveys": [self._format_survey(s) for s in surveys],
        }

    # ─── Guest Complaints ────────────────────────────────────────

    async def file_complaint(self, user_id: int, data: dict) -> dict:
        booking = await self.hotel_repo.get_booking(data.get("booking_id"))
        if not booking:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")
        complaint_data = {
            "booking_id": booking.id,
            "hotel_id": booking.hotel_id,
            "user_id": user_id,
            "category": data.get("category", "other"),
            "priority": data.get("priority", "normal"),
            "description": data.get("description", ""),
        }
        complaint = await self.repo.create_complaint(complaint_data)
        return self._format_complaint(complaint)

    async def resolve_complaint(self, complaint_id: int, resolved_by: int, data: dict) -> dict:
        complaint = await self.repo.get_complaint(complaint_id)
        if not complaint:
            raise ValueError("Complaint not found")
        resolution = await self.repo.resolve_complaint(
            complaint_id=complaint_id,
            resolved_by=resolved_by,
            notes=data.get("resolution_notes"),
            compensation=data.get("compensation"),
        )
        return {
            "complaint": self._format_complaint(complaint),
            "resolution": {
                "id": resolution.id,
                "notes": resolution.resolution_notes,
                "compensation": resolution.compensation,
                "resolved_at": resolution.resolved_at.isoformat() if resolution.resolved_at else None,
            },
        }

    async def get_complaint_stats(self, hotel_id: int) -> dict:
        return await self.repo.get_complaint_stats(hotel_id)

    # ─── Guest Preferences ───────────────────────────────────────

    async def save_preferences(self, user_id: int, data: dict) -> dict:
        pref = await self.repo.upsert_guest_preference(user_id, data)
        return {
            "id": pref.id,
            "user_id": pref.user_id,
            "preferred_room_type": pref.preferred_room_type,
            "dietary_restrictions": pref.dietary_restrictions,
            "special_needs": pref.special_needs,
            "preferred_floor": pref.preferred_floor,
            "smoking_preference": pref.smoking_preference,
        }

    async def get_preferences(self, user_id: int) -> dict | None:
        pref = await self.repo.get_guest_preference(user_id)
        if not pref:
            return None
        return {
            "id": pref.id,
            "user_id": pref.user_id,
            "preferred_room_type": pref.preferred_room_type,
            "dietary_restrictions": pref.dietary_restrictions,
            "special_needs": pref.special_needs,
            "preferred_floor": pref.preferred_floor,
            "smoking_preference": pref.smoking_preference,
        }

    # ─── Housekeeping ────────────────────────────────────────────

    async def log_housekeeping(self, hotel_id: int, data: dict) -> dict:
        log_data = {
            "hotel_id": hotel_id,
            "room_type_id": data.get("room_type_id"),
            "room_number": data.get("room_number"),
            "cleaning_date": data.get("cleaning_date", datetime.now(timezone.utc)),
            "cleaner_name": data.get("cleaner_name"),
            "checklist_items": data.get("checklist_items"),
            "status": data.get("status", "completed"),
            "notes": data.get("notes"),
        }
        log = await self.repo.create_housekeeping_log(log_data)
        return self._format_housekeeping(log)

    # ─── Fumigation / Pest Control ───────────────────────────────

    async def schedule_fumigation(self, hotel_id: int, data: dict) -> dict:
        log_data = {
            "hotel_id": hotel_id,
            "scheduled_date": data.get("scheduled_date"),
            "chemical_used": data.get("chemical_used"),
            "company_name": data.get("company_name"),
            "technician_name": data.get("technician_name"),
            "target_pests": data.get("target_pests"),
            "areas_treated": data.get("areas_treated"),
            "status": data.get("status", "scheduled"),
            "notes": data.get("notes"),
        }
        log = await self.repo.create_fumigation_log(log_data)
        return self._format_fumigation(log)

    async def complete_fumigation(self, log_id: int, data: dict) -> dict:
        update_data = {
            "status": "completed",
            "fumigation_date": data.get("fumigation_date", datetime.now(timezone.utc)),
            "next_fumigation_date": data.get("next_fumigation_date"),
            "chemical_used": data.get("chemical_used"),
            "notes": data.get("notes"),
        }
        log = await self.repo.update_fumigation_log(log_id, update_data)
        if not log:
            raise ValueError("Fumigation log not found")
        return self._format_fumigation(log)

    async def get_fumigation_status(self, hotel_id: int) -> dict:
        upcoming = await self.repo.get_upcoming_fumigations(hotel_id)
        stats = await self.repo.get_fumigation_stats(hotel_id)
        return {
            "upcoming": [self._format_fumigation(f) for f in upcoming],
            "stats": stats,
        }

    # ─── Hotel Kitchen ───────────────────────────────────────────

    async def create_kitchen(self, hotel_id: int, data: dict) -> dict:
        kitchen_data = {
            "hotel_id": hotel_id,
            **data,
        }
        kitchen = await self.repo.create_kitchen(kitchen_data)
        return self._format_kitchen(kitchen)

    async def add_menu_item(self, hotel_id: int, kitchen_id: int, data: dict) -> dict:
        item_data = {
            "hotel_id": hotel_id,
            "kitchen_id": kitchen_id,
            **data,
        }
        item = await self.repo.create_menu_item(item_data)
        return self._format_menu_item(item)

    async def get_kitchen_menu(self, kitchen_id: int) -> list[dict]:
        items = await self.repo.list_kitchen_menu(kitchen_id)
        return [self._format_menu_item(i) for i in items]

    # ─── In-Room Dining ──────────────────────────────────────────

    async def place_dining_order(self, user_id: int, data: dict) -> dict:
        booking = await self.hotel_repo.get_booking(data.get("booking_id"))
        if not booking:
            raise ValueError("Booking not found")
        if booking.user_id != user_id:
            raise ValueError("Booking does not belong to this user")
        order_data = {
            "booking_id": booking.id,
            "hotel_id": booking.hotel_id,
            "kitchen_id": data.get("kitchen_id"),
            "user_id": user_id,
            "room_number": data.get("room_number"),
            "items": data.get("items", []),
            "total_price": data.get("total_price", 0),
            "special_instructions": data.get("special_instructions"),
        }
        order = await self.repo.create_dining_order(order_data)
        return self._format_dining_order(order)

    async def update_dining_status(self, order_id: int, status: str) -> dict:
        order = await self.repo.update_dining_order_status(order_id, status)
        if not order:
            raise ValueError("Order not found")
        return self._format_dining_order(order)

    # ─── Kitchen Reviews ─────────────────────────────────────────

    async def review_kitchen(self, user_id: int, data: dict) -> dict:
        order = await self.repo.get_dining_order(data.get("order_id"))
        if not order:
            raise ValueError("Order not found")
        if order.user_id != user_id:
            raise ValueError("Order does not belong to this user")
        review_data = {
            "hotel_id": order.hotel_id,
            "kitchen_id": order.kitchen_id,
            "order_id": order.id,
            "user_id": user_id,
            "food_quality": data.get("food_quality"),
            "presentation": data.get("presentation"),
            "delivery_speed": data.get("delivery_speed"),
            "temperature": data.get("temperature"),
            "comment": data.get("comment"),
        }
        review = await self.repo.create_kitchen_review(review_data)
        return self._format_kitchen_review(review)

    # ─── Safety & Compliance ────────────────────────────────────

    async def save_building_info(self, hotel_id: int, data: dict) -> dict:
        info = await self.repo.upsert_building_info(hotel_id, data)
        return {
            "year_built": info.year_built, "architect": info.architect,
            "contractor": info.contractor, "construction_company": info.construction_company,
            "building_type": info.building_type, "number_of_floors": info.number_of_floors,
            "has_elevator": info.has_elevator, "has_generator": info.has_generator,
            "has_parking": info.has_parking,
        }

    async def save_fire_safety(self, hotel_id: int, data: dict) -> dict:
        fs = await self.repo.upsert_fire_safety(hotel_id, data)
        return {
            "has_sprinkler": fs.has_sprinkler, "has_fire_alarm": fs.has_fire_alarm,
            "has_fire_extinguisher": fs.has_fire_extinguisher, "has_fire_escape": fs.has_fire_escape,
            "installation_company": fs.installation_company,
            "last_service_date": fs.last_service_date.isoformat() if fs.last_service_date else None,
            "next_service_date": fs.next_service_date.isoformat() if fs.next_service_date else None,
            "certificate_number": fs.certificate_number,
        }

    async def save_security_system(self, hotel_id: int, data: dict) -> dict:
        ss = await self.repo.upsert_security_system(hotel_id, data)
        return {
            "has_cctv": ss.has_cctv, "has_alarm": ss.has_alarm,
            "has_security_personnel": ss.has_security_personnel,
            "has_room_safe": ss.has_room_safe, "has_smoke_detector": ss.has_smoke_detector,
            "installation_company": ss.installation_company,
            "verification_company": ss.verification_company,
            "verification_date": ss.verification_date.isoformat() if ss.verification_date else None,
        }

    async def add_inspection(self, hotel_id: int, data: dict) -> dict:
        insp = await self.repo.create_inspection({"hotel_id": hotel_id, **data})
        return {
            "id": insp.id, "inspection_type": insp.inspection_type,
            "inspector_name": insp.inspector_name,
            "inspector_organization": insp.inspector_organization,
            "inspection_date": insp.inspection_date.isoformat() if insp.inspection_date else None,
            "result": insp.result, "valid_until": insp.valid_until.isoformat() if insp.valid_until else None,
            "findings": insp.findings,
        }

    # ─── Location Duplicate Detection ──────────────────────────

    async def check_location_duplicate(self, lat: float, lng: float, city: str = None, address: str = None) -> dict:
        nearby = await self.repo.find_hotels_near_location(lat, lng)
        address_matches = []
        if city and address:
            address_matches = await self.repo.find_hotels_by_address(city, address)
        duplicates = []
        seen = set()
        for h in nearby:
            if h.id not in seen:
                seen.add(h.id)
                duplicates.append({"id": h.id, "name": h.name, "slug": h.slug, "distance": "nearby"})
        for h in address_matches:
            if h.id not in seen:
                seen.add(h.id)
                duplicates.append({"id": h.id, "name": h.name, "slug": h.slug, "distance": "same_address"})
        return {"has_duplicate": len(duplicates) > 0, "duplicates": duplicates}

    async def request_location_reopen(self, hotel_id: int, existing_hotel_id: int, requester_id: int, reason: str = None) -> dict:
        req = await self.repo.create_location_request({
            "hotel_id": hotel_id, "existing_hotel_id": existing_hotel_id,
            "requester_id": requester_id, "reason": reason,
        })
        return {"id": req.id, "status": req.status, "created_at": req.created_at.isoformat() if req.created_at else None}

    async def approve_location_reopen(self, request_id: int, approved_by: int) -> dict:
        req = await self.repo.approve_location_request(request_id, approved_by)
        if not req:
            raise ValueError("Request not found")
        return {"id": req.id, "status": req.status, "approved_by": approved_by}

    # ─── Suspension & Complaint Escalation ─────────────────────

    async def check_and_suspend_overdue_complaints(self) -> list[dict]:
        return await self.repo.check_and_escalate_complaints()

    async def get_hotel_suspension_status(self, hotel_id: int) -> dict:
        active = await self.repo.get_active_suspension(hotel_id)
        past_count = await self.repo.count_past_suspensions(hotel_id)
        return {
            "is_suspended": active is not None,
            "active_suspension": {
                "id": active.id, "reason": active.reason,
                "duration_days": active.duration_days,
                "end_date": active.end_date.isoformat() if active.end_date else None,
            } if active else None,
            "total_suspensions": past_count,
            "suspended_until": active.end_date.isoformat() if active and active.end_date else None,
        }

    # ─── Guest Bans (Müşteri Men Etme) ─────────────────────────

    async def ban_guest(self, hotel_id: int, user_id: int, issued_by: int, data: dict) -> dict:
        existing = await self.repo.get_active_ban(hotel_id, user_id)
        if existing:
            raise ValueError(f"Guest already banned on {existing.created_at}")
        ban = await self.repo.ban_guest({
            "hotel_id": hotel_id,
            "user_id": user_id,
            "issued_by": issued_by,
            "reason_category": data.get("reason_category", "other"),
            "description": data.get("description"),
            "is_permanent": data.get("is_permanent", True),
            "expires_at": data.get("expires_at"),
        })
        return {"id": ban.id, "reason_category": ban.reason_category, "description": ban.description, "created_at": ban.created_at.isoformat() if ban.created_at else None}

    async def revoke_ban(self, ban_id: int, revoked_by: int) -> dict:
        ban = await self.repo.revoke_ban(ban_id, revoked_by)
        if not ban:
            raise ValueError("Ban not found")
        return {"id": ban.id, "revoked_at": ban.revoked_at.isoformat() if ban.revoked_at else None}

    async def check_guest_banned(self, hotel_id: int, user_id: int) -> dict:
        banned = await self.repo.is_guest_banned(hotel_id, user_id)
        ban = await self.repo.get_active_ban(hotel_id, user_id) if banned else None
        return {
            "is_banned": banned,
            "ban": {
                "id": ban.id, "reason_category": ban.reason_category,
                "description": ban.description, "is_permanent": ban.is_permanent,
                "expires_at": ban.expires_at.isoformat() if ban.expires_at else None,
            } if ban else None,
        }

    # ─── Documents ──────────────────────────────────────────────

    async def upload_document(self, hotel_id: int, data: dict) -> dict:
        doc = await self.repo.add_document(hotel_id, data)
        return {
            "id": doc.id, "document_type": doc.document_type,
            "document_name": doc.document_name, "file_url": doc.file_url,
            "reference_number": doc.reference_number,
            "issuing_authority": doc.issuing_authority,
            "issue_date": doc.issue_date.isoformat() if doc.issue_date else None,
            "expiry_date": doc.expiry_date.isoformat() if doc.expiry_date else None,
        }

    async def verify_document(self, doc_id: int, verified_by: int) -> dict:
        doc = await self.repo.verify_document(doc_id, verified_by)
        if not doc:
            raise ValueError("Document not found")
        return {"id": doc.id, "is_verified": doc.is_verified, "verified_at": doc.verified_at.isoformat() if doc.verified_at else None}

    async def get_document_stats(self, hotel_id: int) -> dict:
        return await self.repo.get_document_stats(hotel_id)

    # ─── Tourism Associations ───────────────────────────────────

    async def join_association(self, hotel_id: int, association_id: int, membership_number: str = None) -> dict:
        m = await self.repo.add_property_membership(hotel_id, association_id, membership_number)
        return {"id": m.id, "association_id": m.association_id, "membership_number": m.membership_number}

    async def get_property_associations(self, hotel_id: int) -> list[dict]:
        return await self.repo.list_property_memberships(hotel_id)

    async def get_safety_compliance(self, hotel_id: int) -> dict:
        return await self.repo.get_safety_compliance_summary(hotel_id)

    # ─── Nearby Places ───────────────────────────────────────────

    async def add_nearby_place(self, hotel_id: int, data: dict) -> dict:
        place = await self.repo.add_nearby_place({"hotel_id": hotel_id, **data})
        return self._format_nearby_place(place)

    # ─── Formatters ──────────────────────────────────────────────

    def _format_survey(self, s) -> dict:
        return {
            "id": s.id, "booking_id": s.booking_id, "hotel_id": s.hotel_id,
            "user_id": s.user_id, "overall_score": s.overall_score,
            "would_recommend": s.would_recommend,
            "checkin_experience": s.checkin_experience,
            "cleanliness_score": s.cleanliness_score,
            "service_score": s.service_score, "view_score": s.view_score,
            "food_score": s.food_score, "value_score": s.value_score,
            "noise_score": s.noise_score, "bed_comfort": s.bed_comfort,
            "comments": s.comments,
            "created_at": s.created_at.isoformat() if s.created_at else None,
        }

    def _format_complaint(self, c) -> dict:
        return {
            "id": c.id, "booking_id": c.booking_id, "hotel_id": c.hotel_id,
            "user_id": c.user_id, "category": c.category, "priority": c.priority,
            "description": c.description, "status": c.status,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }

    def _format_housekeeping(self, h) -> dict:
        return {
            "id": h.id, "hotel_id": h.hotel_id, "room_type_id": h.room_type_id,
            "room_number": h.room_number,
            "cleaning_date": h.cleaning_date.isoformat() if h.cleaning_date else None,
            "cleaner_name": h.cleaner_name, "checklist_items": h.checklist_items,
            "status": h.status, "notes": h.notes,
            "created_at": h.created_at.isoformat() if h.created_at else None,
        }

    def _format_fumigation(self, f) -> dict:
        return {
            "id": f.id, "hotel_id": f.hotel_id,
            "scheduled_date": f.scheduled_date.isoformat() if f.scheduled_date else None,
            "fumigation_date": f.fumigation_date.isoformat() if f.fumigation_date else None,
            "next_fumigation_date": f.next_fumigation_date.isoformat() if f.next_fumigation_date else None,
            "chemical_used": f.chemical_used, "company_name": f.company_name,
            "technician_name": f.technician_name, "target_pests": f.target_pests,
            "areas_treated": f.areas_treated, "status": f.status, "notes": f.notes,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }

    def _format_kitchen(self, k) -> dict:
        return {
            "id": k.id, "hotel_id": k.hotel_id, "name": k.name,
            "cuisine_type": k.cuisine_type, "is_open": k.is_open,
            "opening_time": k.opening_time, "closing_time": k.closing_time,
            "min_order_amount": k.min_order_amount,
            "preparation_time_min": k.preparation_time_min,
            "phone": k.phone, "description": k.description,
            "created_at": k.created_at.isoformat() if k.created_at else None,
        }

    def _format_menu_item(self, m) -> dict:
        return {
            "id": m.id, "hotel_id": m.hotel_id, "kitchen_id": m.kitchen_id,
            "name": m.name, "description": m.description,
            "category": m.category, "price": m.price,
            "compare_price": m.compare_price, "is_available": m.is_available,
            "is_vegetarian": m.is_vegetarian, "is_vegan": m.is_vegan,
            "is_gluten_free": m.is_gluten_free, "image_url": m.image_url,
            "sort_order": m.sort_order,
            "created_at": m.created_at.isoformat() if m.created_at else None,
        }

    def _format_dining_order(self, o) -> dict:
        return {
            "id": o.id, "order_no": o.order_no, "booking_id": o.booking_id,
            "hotel_id": o.hotel_id, "kitchen_id": o.kitchen_id,
            "user_id": o.user_id, "room_number": o.room_number,
            "items": o.items, "total_price": o.total_price,
            "status": o.status, "special_instructions": o.special_instructions,
            "ordered_at": o.ordered_at.isoformat() if o.ordered_at else None,
            "prepared_at": o.prepared_at.isoformat() if o.prepared_at else None,
            "delivered_at": o.delivered_at.isoformat() if o.delivered_at else None,
        }

    def _format_kitchen_review(self, r) -> dict:
        return {
            "id": r.id, "hotel_id": r.hotel_id, "kitchen_id": r.kitchen_id,
            "order_id": r.order_id, "user_id": r.user_id,
            "food_quality": r.food_quality, "presentation": r.presentation,
            "delivery_speed": r.delivery_speed, "temperature": r.temperature,
            "comment": r.comment,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }

    def _format_nearby_place(self, p) -> dict:
        return {
            "id": p.id, "hotel_id": p.hotel_id, "name": p.name,
            "category": p.category, "distance_km": p.distance_km,
            "lat": p.lat, "lng": p.lng, "description": p.description,
        }
