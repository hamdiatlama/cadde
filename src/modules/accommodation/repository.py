import random
import string
from datetime import datetime, timezone
from sqlalchemy import select, func, update, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from src.modules.hotel.models import Hotel, HotelStatus
from src.config import IS_SQLITE
from src.modules.accommodation.models import (
    AccommodationSatisfactionSurvey, AccommodationReviewPhoto,
    GuestComplaint, ComplaintResolution, GuestPreference,
    HousekeepingLog, PropertyFumigationLog,
    HotelKitchen, HotelMenuItem, InRoomDiningOrder, HotelKitchenReview,
    NearbyPlace,
    PropertyBuildingInfo, FireSafetySystem, PropertySecuritySystem,
    PropertyInspection, SafetyCertificate,
    TourismAssociation, PropertyAssociationMember,
    PropertyDocument, HotelSuspension, ComplaintAction, LocationRegistrationRequest, GuestBan,
)


def _generate_order_no() -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"RMS-{suffix}"


class AccommodationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Satisfaction Surveys ────────────────────────────────────

    async def create_survey(self, data: dict) -> AccommodationSatisfactionSurvey:
        s = AccommodationSatisfactionSurvey(**data)
        self.db.add(s)
        return s

    async def get_survey(self, survey_id: int) -> AccommodationSatisfactionSurvey | None:
        r = await self.db.execute(
            select(AccommodationSatisfactionSurvey).where(AccommodationSatisfactionSurvey.id == survey_id)
        )
        return r.scalar_one_or_none()

    async def get_survey_by_booking(self, booking_id: int) -> AccommodationSatisfactionSurvey | None:
        r = await self.db.execute(
            select(AccommodationSatisfactionSurvey).where(
                AccommodationSatisfactionSurvey.booking_id == booking_id
            )
        )
        return r.scalar_one_or_none()

    async def list_hotel_surveys(self, hotel_id: int, page=1, per_page=20):
        query = select(AccommodationSatisfactionSurvey).where(
            AccommodationSatisfactionSurvey.hotel_id == hotel_id
        )
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(AccommodationSatisfactionSurvey.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def get_hotel_satisfaction_stats(self, hotel_id: int) -> dict:
        r = await self.db.execute(
            select(
                func.avg(AccommodationSatisfactionSurvey.overall_score),
                func.avg(AccommodationSatisfactionSurvey.cleanliness_score),
                func.avg(AccommodationSatisfactionSurvey.service_score),
                func.avg(AccommodationSatisfactionSurvey.view_score),
                func.avg(AccommodationSatisfactionSurvey.food_score),
                func.avg(AccommodationSatisfactionSurvey.checkin_experience),
                func.avg(AccommodationSatisfactionSurvey.noise_score),
                func.avg(AccommodationSatisfactionSurvey.bed_comfort),
                func.count(AccommodationSatisfactionSurvey.id),
                func.sum(AccommodationSatisfactionSurvey.would_recommend.cast(
                    __import__("sqlalchemy").Integer
                )),
            ).where(AccommodationSatisfactionSurvey.hotel_id == hotel_id)
        )
        row = r.one()
        total = row[8] or 0
        return {
            "overall": round(float(row[0]), 2) if row[0] else 0,
            "cleanliness": round(float(row[1]), 2) if row[1] else 0,
            "service": round(float(row[2]), 2) if row[2] else 0,
            "view": round(float(row[3]), 2) if row[3] else 0,
            "food": round(float(row[4]), 2) if row[4] else 0,
            "checkin": round(float(row[5]), 2) if row[5] else 0,
            "noise": round(float(row[6]), 2) if row[6] else 0,
            "bed_comfort": round(float(row[7]), 2) if row[7] else 0,
            "total_surveys": total,
            "would_recommend_pct": round((row[9] or 0) / total * 100, 1) if total > 0 else 0,
        }

    # ─── Review Photos ───────────────────────────────────────────

    async def add_review_photo(self, review_id: int, url: str, caption: str = None) -> AccommodationReviewPhoto:
        p = AccommodationReviewPhoto(review_id=review_id, url=url, caption=caption)
        self.db.add(p)
        return p

    async def list_review_photos(self, review_id: int) -> list[AccommodationReviewPhoto]:
        r = await self.db.execute(
            select(AccommodationReviewPhoto).where(
                AccommodationReviewPhoto.review_id == review_id
            ).order_by(AccommodationReviewPhoto.sort_order)
        )
        return list(r.scalars().all())

    # ─── Guest Complaints ────────────────────────────────────────

    async def create_complaint(self, data: dict) -> GuestComplaint:
        c = GuestComplaint(**data)
        self.db.add(c)
        return c

    async def get_complaint(self, complaint_id: int) -> GuestComplaint | None:
        r = await self.db.execute(
            select(GuestComplaint).where(GuestComplaint.id == complaint_id)
        )
        return r.scalar_one_or_none()

    async def list_hotel_complaints(self, hotel_id: int, status=None, page=1, per_page=20):
        query = select(GuestComplaint).where(GuestComplaint.hotel_id == hotel_id)
        if status:
            query = query.where(GuestComplaint.status == status)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(GuestComplaint.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def list_user_complaints(self, user_id: int, page=1, per_page=20):
        query = select(GuestComplaint).where(GuestComplaint.user_id == user_id)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(GuestComplaint.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def update_complaint_status(self, complaint_id: int, status: str) -> GuestComplaint | None:
        c = await self.get_complaint(complaint_id)
        if not c:
            return None
        c.status = status
        self.db.add(c)
        return c

    async def resolve_complaint(self, complaint_id: int, resolved_by: int, notes: str = None, compensation: str = None) -> ComplaintResolution:
        r = ComplaintResolution(
            complaint_id=complaint_id, resolved_by=resolved_by,
            resolution_notes=notes, compensation=compensation,
        )
        self.db.add(r)
        await self.update_complaint_status(complaint_id, "resolved")
        return r

    async def get_complaint_resolution(self, complaint_id: int) -> ComplaintResolution | None:
        r = await self.db.execute(
            select(ComplaintResolution).where(
                ComplaintResolution.complaint_id == complaint_id
            )
        )
        return r.scalar_one_or_none()

    async def get_complaint_stats(self, hotel_id: int) -> dict:
        total_q = select(func.count(GuestComplaint.id)).where(
            GuestComplaint.hotel_id == hotel_id
        )
        open_q = select(func.count(GuestComplaint.id)).where(
            GuestComplaint.hotel_id == hotel_id,
            GuestComplaint.status == "open",
        )
        resolved_q = select(func.count(GuestComplaint.id)).where(
            GuestComplaint.hotel_id == hotel_id,
            GuestComplaint.status == "resolved",
        )
        total = (await self.db.execute(total_q)).scalar() or 0
        open_count = (await self.db.execute(open_q)).scalar() or 0
        resolved_count = (await self.db.execute(resolved_q)).scalar() or 0
        return {
            "total": total,
            "open": open_count,
            "resolved": resolved_count,
            "resolution_rate": round(resolved_count / total * 100, 1) if total > 0 else 0,
        }

    # ─── Guest Preferences ───────────────────────────────────────

    async def get_guest_preference(self, user_id: int) -> GuestPreference | None:
        r = await self.db.execute(
            select(GuestPreference).where(GuestPreference.user_id == user_id)
        )
        return r.scalar_one_or_none()

    async def upsert_guest_preference(self, user_id: int, data: dict) -> GuestPreference:
        existing = await self.get_guest_preference(user_id)
        if existing:
            for field, val in data.items():
                setattr(existing, field, val)
            self.db.add(existing)
            return existing
        pref = GuestPreference(user_id=user_id, **data)
        self.db.add(pref)
        return pref

    # ─── Housekeeping ────────────────────────────────────────────

    async def create_housekeeping_log(self, data: dict) -> HousekeepingLog:
        h = HousekeepingLog(**data)
        self.db.add(h)
        return h

    async def list_housekeeping_logs(self, hotel_id: int, page=1, per_page=20):
        query = select(HousekeepingLog).where(HousekeepingLog.hotel_id == hotel_id)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(HousekeepingLog.cleaning_date.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    # ─── Fumigation / Pest Control ───────────────────────────────

    async def create_fumigation_log(self, data: dict) -> PropertyFumigationLog:
        f = PropertyFumigationLog(**data)
        self.db.add(f)
        return f

    async def get_fumigation_log(self, log_id: int) -> PropertyFumigationLog | None:
        r = await self.db.execute(
            select(PropertyFumigationLog).where(PropertyFumigationLog.id == log_id)
        )
        return r.scalar_one_or_none()

    async def list_fumigation_logs(self, hotel_id: int, status=None, page=1, per_page=20):
        query = select(PropertyFumigationLog).where(PropertyFumigationLog.hotel_id == hotel_id)
        if status:
            query = query.where(PropertyFumigationLog.status == status)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(PropertyFumigationLog.scheduled_date.desc().nullslast())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def get_upcoming_fumigations(self, hotel_id: int) -> list[PropertyFumigationLog]:
        r = await self.db.execute(
            select(PropertyFumigationLog).where(
                PropertyFumigationLog.hotel_id == hotel_id,
                PropertyFumigationLog.status == "scheduled",
                PropertyFumigationLog.scheduled_date >= datetime.now(timezone.utc),
            ).order_by(PropertyFumigationLog.scheduled_date)
        )
        return list(r.scalars().all())

    async def update_fumigation_log(self, log_id: int, data: dict) -> PropertyFumigationLog | None:
        f = await self.get_fumigation_log(log_id)
        if not f:
            return None
        for field, val in data.items():
            setattr(f, field, val)
        self.db.add(f)
        return f

    async def get_fumigation_stats(self, hotel_id: int) -> dict:
        total_q = select(func.count(PropertyFumigationLog.id)).where(
            PropertyFumigationLog.hotel_id == hotel_id
        )
        scheduled_q = select(func.count(PropertyFumigationLog.id)).where(
            PropertyFumigationLog.hotel_id == hotel_id,
            PropertyFumigationLog.status == "scheduled",
        )
        completed_q = select(func.count(PropertyFumigationLog.id)).where(
            PropertyFumigationLog.hotel_id == hotel_id,
            PropertyFumigationLog.status == "completed",
        )
        last_q = select(PropertyFumigationLog.fumigation_date).where(
            PropertyFumigationLog.hotel_id == hotel_id,
            PropertyFumigationLog.status == "completed",
        ).order_by(PropertyFumigationLog.fumigation_date.desc()).limit(1)
        total = (await self.db.execute(total_q)).scalar() or 0
        scheduled = (await self.db.execute(scheduled_q)).scalar() or 0
        completed = (await self.db.execute(completed_q)).scalar() or 0
        last_r = await self.db.execute(last_q)
        last = last_r.scalar_one_or_none()
        return {
            "total": total, "scheduled": scheduled, "completed": completed,
            "last_fumigation": last.isoformat() if last else None,
        }

    # ─── Hotel Kitchen ───────────────────────────────────────────

    async def create_kitchen(self, data: dict) -> HotelKitchen:
        k = HotelKitchen(**data)
        self.db.add(k)
        return k

    async def get_kitchen(self, kitchen_id: int) -> HotelKitchen | None:
        r = await self.db.execute(
            select(HotelKitchen).where(HotelKitchen.id == kitchen_id)
        )
        return r.scalar_one_or_none()

    async def list_hotel_kitchens(self, hotel_id: int) -> list[HotelKitchen]:
        r = await self.db.execute(
            select(HotelKitchen).where(HotelKitchen.hotel_id == hotel_id)
        )
        return list(r.scalars().all())

    async def update_kitchen(self, kitchen_id: int, data: dict) -> HotelKitchen | None:
        k = await self.get_kitchen(kitchen_id)
        if not k:
            return None
        for field, val in data.items():
            setattr(k, field, val)
        self.db.add(k)
        return k

    # ─── Hotel Menu Items ────────────────────────────────────────

    async def create_menu_item(self, data: dict) -> HotelMenuItem:
        m = HotelMenuItem(**data)
        self.db.add(m)
        return m

    async def get_menu_item(self, item_id: int) -> HotelMenuItem | None:
        r = await self.db.execute(
            select(HotelMenuItem).where(HotelMenuItem.id == item_id)
        )
        return r.scalar_one_or_none()

    async def list_kitchen_menu(self, kitchen_id: int) -> list[HotelMenuItem]:
        r = await self.db.execute(
            select(HotelMenuItem).where(
                HotelMenuItem.kitchen_id == kitchen_id,
                HotelMenuItem.is_available == True,
            ).order_by(HotelMenuItem.sort_order)
        )
        return list(r.scalars().all())

    async def update_menu_item(self, item_id: int, data: dict) -> HotelMenuItem | None:
        m = await self.get_menu_item(item_id)
        if not m:
            return None
        for field, val in data.items():
            setattr(m, field, val)
        self.db.add(m)
        return m

    # ─── In-Room Dining Orders ───────────────────────────────────

    async def create_dining_order(self, data: dict) -> InRoomDiningOrder:
        order = InRoomDiningOrder(order_no=_generate_order_no(), **data)
        self.db.add(order)
        return order

    async def get_dining_order(self, order_id: int) -> InRoomDiningOrder | None:
        r = await self.db.execute(
            select(InRoomDiningOrder).where(InRoomDiningOrder.id == order_id)
        )
        return r.scalar_one_or_none()

    async def get_dining_order_by_no(self, order_no: str) -> InRoomDiningOrder | None:
        r = await self.db.execute(
            select(InRoomDiningOrder).where(InRoomDiningOrder.order_no == order_no)
        )
        return r.scalar_one_or_none()

    async def list_kitchen_orders(self, kitchen_id: int, status=None, page=1, per_page=20):
        query = select(InRoomDiningOrder).where(InRoomDiningOrder.kitchen_id == kitchen_id)
        if status:
            query = query.where(InRoomDiningOrder.status == status)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(InRoomDiningOrder.ordered_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def list_booking_dining_orders(self, booking_id: int) -> list[InRoomDiningOrder]:
        r = await self.db.execute(
            select(InRoomDiningOrder).where(InRoomDiningOrder.booking_id == booking_id)
            .order_by(InRoomDiningOrder.ordered_at.desc())
        )
        return list(r.scalars().all())

    async def update_dining_order_status(self, order_id: int, status: str) -> InRoomDiningOrder | None:
        order = await self.get_dining_order(order_id)
        if not order:
            return None
        now = datetime.now(timezone.utc)
        order.status = status
        if status == "prepared":
            order.prepared_at = now
        elif status == "delivered":
            order.delivered_at = now
        elif status == "cancelled":
            order.cancelled_at = now
        self.db.add(order)
        return order

    # ─── Kitchen Reviews ─────────────────────────────────────────

    async def create_kitchen_review(self, data: dict) -> HotelKitchenReview:
        r = HotelKitchenReview(**data)
        self.db.add(r)
        return r

    async def list_kitchen_reviews(self, kitchen_id: int, page=1, per_page=20):
        query = select(HotelKitchenReview).where(
            HotelKitchenReview.kitchen_id == kitchen_id
        )
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(HotelKitchenReview.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def get_kitchen_rating(self, kitchen_id: int) -> dict:
        r = await self.db.execute(
            select(
                func.avg(HotelKitchenReview.food_quality),
                func.avg(HotelKitchenReview.presentation),
                func.avg(HotelKitchenReview.delivery_speed),
                func.avg(HotelKitchenReview.temperature),
                func.count(HotelKitchenReview.id),
            ).where(HotelKitchenReview.kitchen_id == kitchen_id)
        )
        fq, pres, speed, temp, cnt = r.one()
        return {
            "food_quality": round(float(fq), 2) if fq else 0,
            "presentation": round(float(pres), 2) if pres else 0,
            "delivery_speed": round(float(speed), 2) if speed else 0,
            "temperature": round(float(temp), 2) if temp else 0,
            "total_reviews": cnt or 0,
        }

    # ─── Nearby Places ───────────────────────────────────────────

    async def add_nearby_place(self, data: dict) -> NearbyPlace:
        p = NearbyPlace(**data)
        self.db.add(p)
        return p

    async def list_nearby_places(self, hotel_id: int, category: str = None) -> list[NearbyPlace]:
        query = select(NearbyPlace).where(
            NearbyPlace.hotel_id == hotel_id, NearbyPlace.is_active == True
        )
        if category:
            query = query.where(NearbyPlace.category == category)
        query = query.order_by(NearbyPlace.distance_km)
        r = await self.db.execute(query)
        return list(r.scalars().all())

    # ─── Building Info ──────────────────────────────────────────

    async def upsert_building_info(self, hotel_id: int, data: dict) -> PropertyBuildingInfo:
        r = await self.db.execute(
            select(PropertyBuildingInfo).where(PropertyBuildingInfo.hotel_id == hotel_id)
        )
        info = r.scalar_one_or_none()
        if info:
            for field, val in data.items():
                setattr(info, field, val)
            self.db.add(info)
            return info
        info = PropertyBuildingInfo(hotel_id=hotel_id, **data)
        self.db.add(info)
        return info

    async def get_building_info(self, hotel_id: int) -> PropertyBuildingInfo | None:
        r = await self.db.execute(
            select(PropertyBuildingInfo).where(PropertyBuildingInfo.hotel_id == hotel_id)
        )
        return r.scalar_one_or_none()

    # ─── Fire Safety ────────────────────────────────────────────

    async def upsert_fire_safety(self, hotel_id: int, data: dict) -> FireSafetySystem:
        r = await self.db.execute(
            select(FireSafetySystem).where(FireSafetySystem.hotel_id == hotel_id)
        )
        fs = r.scalar_one_or_none()
        if fs:
            for field, val in data.items():
                setattr(fs, field, val)
            self.db.add(fs)
            return fs
        fs = FireSafetySystem(hotel_id=hotel_id, **data)
        self.db.add(fs)
        return fs

    async def get_fire_safety(self, hotel_id: int) -> FireSafetySystem | None:
        r = await self.db.execute(
            select(FireSafetySystem).where(FireSafetySystem.hotel_id == hotel_id)
        )
        return r.scalar_one_or_none()

    # ─── Security Systems ───────────────────────────────────────

    async def upsert_security_system(self, hotel_id: int, data: dict) -> PropertySecuritySystem:
        r = await self.db.execute(
            select(PropertySecuritySystem).where(PropertySecuritySystem.hotel_id == hotel_id)
        )
        ss = r.scalar_one_or_none()
        if ss:
            for field, val in data.items():
                setattr(ss, field, val)
            self.db.add(ss)
            return ss
        ss = PropertySecuritySystem(hotel_id=hotel_id, **data)
        self.db.add(ss)
        return ss

    async def get_security_system(self, hotel_id: int) -> PropertySecuritySystem | None:
        r = await self.db.execute(
            select(PropertySecuritySystem).where(PropertySecuritySystem.hotel_id == hotel_id)
        )
        return r.scalar_one_or_none()

    # ─── Inspections ────────────────────────────────────────────

    async def create_inspection(self, data: dict) -> PropertyInspection:
        insp = PropertyInspection(**data)
        self.db.add(insp)
        return insp

    async def list_inspections(self, hotel_id: int) -> list[PropertyInspection]:
        r = await self.db.execute(
            select(PropertyInspection).where(PropertyInspection.hotel_id == hotel_id)
            .order_by(PropertyInspection.inspection_date.desc())
        )
        return list(r.scalars().all())

    async def get_latest_inspection(self, hotel_id: int) -> PropertyInspection | None:
        r = await self.db.execute(
            select(PropertyInspection).where(PropertyInspection.hotel_id == hotel_id)
            .order_by(PropertyInspection.inspection_date.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    # ─── Certificates ───────────────────────────────────────────

    async def create_certificate(self, data: dict) -> SafetyCertificate:
        cert = SafetyCertificate(**data)
        self.db.add(cert)
        return cert

    async def list_certificates(self, hotel_id: int) -> list[SafetyCertificate]:
        r = await self.db.execute(
            select(SafetyCertificate).where(SafetyCertificate.hotel_id == hotel_id)
            .order_by(SafetyCertificate.issue_date.desc())
        )
        return list(r.scalars().all())

    # ─── Tourism Associations ───────────────────────────────────

    async def list_associations(self) -> list[TourismAssociation]:
        r = await self.db.execute(
            select(TourismAssociation).where(TourismAssociation.is_active == True)
            .order_by(TourismAssociation.name)
        )
        return list(r.scalars().all())

    async def create_association(self, data: dict) -> TourismAssociation:
        a = TourismAssociation(**data)
        self.db.add(a)
        return a

    async def add_property_membership(self, hotel_id: int, association_id: int, membership_number: str = None) -> PropertyAssociationMember:
        m = PropertyAssociationMember(
            hotel_id=hotel_id, association_id=association_id,
            membership_number=membership_number,
        )
        self.db.add(m)
        return m

    async def list_property_memberships(self, hotel_id: int) -> list[dict]:
        r = await self.db.execute(
            select(PropertyAssociationMember, TourismAssociation)
            .join(TourismAssociation, PropertyAssociationMember.association_id == TourismAssociation.id)
            .where(
                PropertyAssociationMember.hotel_id == hotel_id,
                PropertyAssociationMember.is_active == True,
            )
        )
        rows = r.all()
        return [
            {
                "membership_id": pm.id,
                "association_id": ta.id,
                "association_name": ta.name,
                "association_type": ta.association_type,
                "membership_number": pm.membership_number,
                "member_since": pm.member_since.isoformat() if pm.member_since else None,
                "valid_until": pm.valid_until.isoformat() if pm.valid_until else None,
            }
            for pm, ta in rows
        ]

    async def remove_membership(self, membership_id: int) -> bool:
        r = await self.db.execute(
            select(PropertyAssociationMember).where(PropertyAssociationMember.id == membership_id)
        )
        pm = r.scalar_one_or_none()
        if not pm:
            return False
        pm.is_active = False
        self.db.add(pm)
        return True

    # ─── Property Documents (İzin Belgeleri) ────────────────────

    async def add_document(self, hotel_id: int, data: dict) -> PropertyDocument:
        d = PropertyDocument(hotel_id=hotel_id, **data)
        self.db.add(d)
        return d

    async def get_document(self, doc_id: int) -> PropertyDocument | None:
        r = await self.db.execute(
            select(PropertyDocument).where(PropertyDocument.id == doc_id)
        )
        return r.scalar_one_or_none()

    async def list_documents(self, hotel_id: int) -> list[PropertyDocument]:
        r = await self.db.execute(
            select(PropertyDocument).where(PropertyDocument.hotel_id == hotel_id)
            .order_by(PropertyDocument.created_at.desc())
        )
        return list(r.scalars().all())

    async def verify_document(self, doc_id: int, verified_by: int) -> PropertyDocument | None:
        d = await self.get_document(doc_id)
        if not d:
            return None
        d.is_verified = True
        d.verified_by = verified_by
        d.verified_at = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
        self.db.add(d)
        return d

    async def get_document_stats(self, hotel_id: int) -> dict:
        total_q = select(func.count(PropertyDocument.id)).where(
            PropertyDocument.hotel_id == hotel_id
        )
        verified_q = select(func.count(PropertyDocument.id)).where(
            PropertyDocument.hotel_id == hotel_id,
            PropertyDocument.is_verified == True,
        )
        total = (await self.db.execute(total_q)).scalar() or 0
        verified = (await self.db.execute(verified_q)).scalar() or 0
        return {"total": total, "verified": verified, "pending": total - verified}

    # ─── Location Duplicate Detection ─────────────────────────

    async def find_hotels_near_location(self, lat: float, lng: float, threshold_km: float = 0.5) -> list:
        from sqlalchemy import text
        if IS_SQLITE:
            r = await self.db.execute(
                select(Hotel).where(
                    Hotel.lat.isnot(None),
                    Hotel.lng.isnot(None),
                    Hotel.status == HotelStatus.ACTIVE,
                )
            )
            hotels = r.scalars().all()
            nearby = []
            for h in hotels:
                dlat = h.lat - lat
                dlng = h.lng - lng
                dist = (dlat ** 2 + dlng ** 2) ** 0.5 * 111
                if dist <= threshold_km:
                    nearby.append(h)
            return nearby
        else:
            r = await self.db.execute(
                select(Hotel).where(
                    Hotel.lat.isnot(None),
                    Hotel.lng.isnot(None),
                    Hotel.status == HotelStatus.ACTIVE,
                    text(
                        f"earth_distance(ll_to_earth(lat, lng), ll_to_earth({lat}, {lng})) < {threshold_km * 1000}"
                    ),
                )
            )
            return list(r.scalars().all())

    async def find_hotels_by_address(self, city: str, address: str) -> list:
        r = await self.db.execute(
            select(Hotel).where(
                Hotel.city.ilike(city),
                Hotel.address.ilike(f"%{address}%"),
            )
        )
        return list(r.scalars().all())

    # ─── Location Registration Requests ────────────────────────

    async def create_location_request(self, data: dict) -> LocationRegistrationRequest:
        req = LocationRegistrationRequest(**data)
        self.db.add(req)
        return req

    async def approve_location_request(self, request_id: int, approved_by: int) -> LocationRegistrationRequest | None:
        r = await self.db.execute(
            select(LocationRegistrationRequest).where(LocationRegistrationRequest.id == request_id)
        )
        req = r.scalar_one_or_none()
        if not req:
            return None
        req.status = "approved"
        req.approved_by = approved_by
        req.approved_at = datetime.now(timezone.utc)
        self.db.add(req)
        hotel = await self.db.execute(
            select(Hotel).where(Hotel.id == req.hotel_id)
        )
        hotel = hotel.scalar_one_or_none()
        if hotel:
            hotel.requires_location_approval = False
            hotel.location_approved_by = approved_by
            self.db.add(hotel)
        return req

    # ─── Hotel Suspensions ─────────────────────────────────────

    async def get_active_suspension(self, hotel_id: int) -> HotelSuspension | None:
        r = await self.db.execute(
            select(HotelSuspension).where(
                HotelSuspension.hotel_id == hotel_id,
                HotelSuspension.resolved == False,
                HotelSuspension.end_date > datetime.now(timezone.utc),
            ).order_by(HotelSuspension.end_date.desc()).limit(1)
        )
        return r.scalar_one_or_none()

    async def count_past_suspensions(self, hotel_id: int) -> int:
        r = await self.db.execute(
            select(func.count(HotelSuspension.id)).where(
                HotelSuspension.hotel_id == hotel_id,
            )
        )
        return r.scalar() or 0

    async def create_suspension(self, hotel_id: int, complaint_id: int, reason: str) -> HotelSuspension:
        past_count = await self.count_past_suspensions(hotel_id)
        suspension_number = past_count + 1
        if suspension_number == 1:
            duration = 3
        elif suspension_number == 2:
            duration = 7
        elif suspension_number == 3:
            duration = 14
        elif suspension_number == 4:
            duration = 30
        else:
            duration = 60
        now = datetime.now(timezone.utc)
        start = now
        end = now + timedelta(days=duration)
        suspension = HotelSuspension(
            hotel_id=hotel_id,
            suspension_number=suspension_number,
            reason=reason,
            duration_days=duration,
            start_date=start,
            end_date=end,
            triggered_by_complaint_id=complaint_id,
        )
        self.db.add(suspension)
        hotel = await self.db.execute(select(Hotel).where(Hotel.id == hotel_id))
        hotel = hotel.scalar_one_or_none()
        if hotel:
            hotel.suspended_until = end
            hotel.suspension_reason = f"Askı #{suspension_number}: {reason}"
            self.db.add(hotel)
        return suspension

    async def resolve_suspension(self, suspension_id: int) -> HotelSuspension | None:
        r = await self.db.execute(
            select(HotelSuspension).where(HotelSuspension.id == suspension_id)
        )
        s = r.scalar_one_or_none()
        if not s:
            return None
        s.resolved = True
        s.resolved_at = datetime.now(timezone.utc)
        self.db.add(s)
        return s

    # ─── Complaint Escalation (24h rule) ───────────────────────

    async def create_complaint_action(self, complaint_id: int, action_type: str, description: str = None, performed_by: int = None) -> ComplaintAction:
        deadline = datetime.now(timezone.utc) + timedelta(hours=24)
        action = ComplaintAction(
            complaint_id=complaint_id,
            action_type=action_type,
            description=description,
            performed_by=performed_by,
            deadline=deadline,
        )
        self.db.add(action)
        return action

    async def get_overdue_complaints(self) -> list[GuestComplaint]:
        r = await self.db.execute(
            select(GuestComplaint).where(
                GuestComplaint.status == "open",
                GuestComplaint.created_at < datetime.now(timezone.utc) - timedelta(hours=24),
            )
        )
        return list(r.scalars().all())

    async def check_and_escalate_complaints(self) -> list[dict]:
        overdue = await self.get_overdue_complaints()
        escalated = []
        for complaint in overdue:
            existing_action = await self.db.execute(
                select(ComplaintAction).where(
                    ComplaintAction.complaint_id == complaint.id,
                    ComplaintAction.action_type == "escalation",
                )
            )
            if existing_action.scalar_one_or_none():
                continue
            suspension = await self.create_suspension(
                hotel_id=complaint.hotel_id,
                complaint_id=complaint.id,
                reason=f"24 saat içinde çözülmeyen şikayet: {complaint.category} - {complaint.description[:200]}",
            )
            action = await self.create_complaint_action(
                complaint_id=complaint.id,
                action_type="escalation",
                description=f"Otomatik askı #{suspension.suspension_number} - {suspension.duration_days} gün",
            )
            escalated.append({
                "complaint_id": complaint.id,
                "hotel_id": complaint.hotel_id,
                "suspension_id": suspension.id,
                "duration_days": suspension.duration_days,
            })
        return escalated

    # ─── Guest Bans (Müşteri Men Etme) ─────────────────────────

    async def ban_guest(self, data: dict) -> GuestBan:
        ban = GuestBan(**data)
        self.db.add(ban)
        return ban

    async def get_active_ban(self, hotel_id: int, user_id: int) -> GuestBan | None:
        r = await self.db.execute(
            select(GuestBan).where(
                GuestBan.hotel_id == hotel_id,
                GuestBan.user_id == user_id,
                GuestBan.revoked_at.is_(None),
            )
        )
        return r.scalar_one_or_none()

    async def list_hotel_bans(self, hotel_id: int, page=1, per_page=20):
        query = select(GuestBan).where(GuestBan.hotel_id == hotel_id)
        count_q = select(func.count()).select_from(query.subquery())
        total = (await self.db.execute(count_q)).scalar()
        query = query.order_by(GuestBan.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        r = await self.db.execute(query)
        return list(r.scalars().all()), total

    async def is_guest_banned(self, hotel_id: int, user_id: int) -> bool:
        ban = await self.get_active_ban(hotel_id, user_id)
        return ban is not None

    async def revoke_ban(self, ban_id: int, revoked_by: int) -> GuestBan | None:
        r = await self.db.execute(select(GuestBan).where(GuestBan.id == ban_id))
        ban = r.scalar_one_or_none()
        if not ban:
            return None
        ban.revoked_at = datetime.now(timezone.utc)
        ban.revoked_by = revoked_by
        self.db.add(ban)
        return ban

    async def get_safety_compliance_summary(self, hotel_id: int) -> dict:
        building = await self.get_building_info(hotel_id)
        fire = await self.get_fire_safety(hotel_id)
        security = await self.get_security_system(hotel_id)
        inspections = await self.list_inspections(hotel_id)
        certificates = await self.list_certificates(hotel_id)
        latest_insp = await self.get_latest_inspection(hotel_id)
        return {
            "building_info": {
                "year_built": building.year_built if building else None,
                "contractor": building.contractor if building else None,
                "construction_company": building.construction_company if building else None,
                "architect": building.architect if building else None,
                "number_of_floors": building.number_of_floors if building else None,
            } if building else None,
            "fire_safety": {
                "has_sprinkler": fire.has_sprinkler if fire else False,
                "has_fire_alarm": fire.has_fire_alarm if fire else False,
                "has_fire_extinguisher": fire.has_fire_extinguisher if fire else False,
                "has_fire_escape": fire.has_fire_escape if fire else False,
                "installation_company": fire.installation_company if fire else None,
                "last_service_date": fire.last_service_date.isoformat() if fire and fire.last_service_date else None,
                "next_service_date": fire.next_service_date.isoformat() if fire and fire.next_service_date else None,
            } if fire else None,
            "security_systems": {
                "has_cctv": security.has_cctv if security else False,
                "has_alarm": security.has_alarm if security else False,
                "has_security_personnel": security.has_security_personnel if security else False,
                "has_room_safe": security.has_room_safe if security else False,
                "has_smoke_detector": security.has_smoke_detector if security else False,
                "verification_company": security.verification_company if security else None,
                "verification_date": security.verification_date.isoformat() if security and security.verification_date else None,
            } if security else None,
            "inspections": [
                {
                    "type": i.inspection_type, "inspector": i.inspector_name,
                    "organization": i.inspector_organization,
                    "date": i.inspection_date.isoformat() if i.inspection_date else None,
                    "result": i.result, "valid_until": i.valid_until.isoformat() if i.valid_until else None,
                } for i in inspections
            ],
            "certificates": [
                {
                    "type": c.certificate_type, "number": c.certificate_number,
                    "authority": c.issuing_authority,
                    "issue_date": c.issue_date.isoformat() if c.issue_date else None,
                    "expiry_date": c.expiry_date.isoformat() if c.expiry_date else None,
                    "is_valid": c.is_valid,
                } for c in certificates
            ],
            "latest_inspection": {
                "date": latest_insp.inspection_date.isoformat() if latest_insp and latest_insp.inspection_date else None,
                "result": latest_insp.result if latest_insp else None,
                "organization": latest_insp.inspector_organization if latest_insp else None,
            } if latest_insp else None,
        }

    async def remove_nearby_place(self, place_id: int) -> bool:
        r = await self.db.execute(
            select(NearbyPlace).where(NearbyPlace.id == place_id)
        )
        p = r.scalar_one_or_none()
        if not p:
            return False
        p.is_active = False
        self.db.add(p)
        return True
