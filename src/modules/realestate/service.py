from datetime import datetime, timezone
from sqlalchemy import select
from src.modules.realestate.repository import RealEstateRepo
from src.modules.realestate.models import (
    PropertyCategory, PropertyType, ContractorCompany, ContractorReview,
    PropertyListing, PropertyPhoto, PropertyFeature, PropertyListingFeature,
    AuthorizationRequest, PropertyAppraisalRequest, FavoriteListing, PropertyInquiry,
    CompanyMember, CompanyInvitation,
    ListingPriceConfig, ListingPayment,
    ListingDocument, DocumentVerification,
)


class RealEstateService:
    def __init__(self, db):
        self.repo = RealEstateRepo(db)

    # ── Categories ──────────────────────────────────────────

    async def create_category(self, data) -> dict:
        obj = PropertyCategory(**data.dict())
        await self.repo.create_category(obj)
        await self.repo.db.flush()
        return {"id": obj.id, "name": obj.name, "slug": obj.slug}

    async def list_categories(self) -> list[dict]:
        categories = await self.repo.list_categories()
        return [{"id": c.id, "name": c.name, "slug": c.slug, "sort_order": c.sort_order} for c in categories]

    # ── Types ───────────────────────────────────────────────

    async def create_type(self, data) -> dict:
        obj = PropertyType(**data.dict())
        await self.repo.create_type(obj)
        await self.repo.db.flush()
        return {"id": obj.id, "name": obj.name, "slug": obj.slug}

    async def list_types(self) -> list[dict]:
        types = await self.repo.list_types()
        return [{"id": t.id, "name": t.name, "slug": t.slug, "icon": t.icon, "sort_order": t.sort_order} for t in types]

    # ── Listings ────────────────────────────────────────────

    async def create_listing(self, user_id: int, data) -> dict:
        payload = data.dict(exclude_unset=True)
        if "status" not in payload:
            payload["status"] = "draft"
        listing = PropertyListing(user_id=user_id, **payload)
        await self.repo.create_listing(listing)
        await self.repo.db.flush()
        return {"id": listing.id, "title": listing.title, "status": listing.status}

    async def get_listing(self, listing_id: int):
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            return None
        photos = await self.repo.list_photos(listing_id)
        features = await self.repo.get_listing_features(listing_id)
        return {
            "id": listing.id,
            "user_id": listing.user_id,
            "category_id": listing.category_id,
            "type_id": listing.type_id,
            "contractor_id": listing.contractor_id,
            "title": listing.title,
            "description": listing.description,
            "price": str(listing.price),
            "currency": listing.currency,
            "is_for_sale": listing.is_for_sale,
            "is_for_rent": listing.is_for_rent,
            "city": listing.city,
            "district": listing.district,
            "neighborhood": listing.neighborhood,
            "address": listing.address,
            "latitude": str(listing.latitude) if listing.latitude else None,
            "longitude": str(listing.longitude) if listing.longitude else None,
            "room_count": listing.room_count,
            "net_area": str(listing.net_area) if listing.net_area else None,
            "gross_area": str(listing.gross_area) if listing.gross_area else None,
            "heating_type": listing.heating_type,
            "furnishing": listing.furnishing,
            "status": listing.status,
            "view_count": listing.view_count,
            "is_highlighted": listing.is_highlighted,
            "created_at": listing.created_at.isoformat() if listing.created_at else None,
            "updated_at": listing.updated_at.isoformat() if listing.updated_at else None,
            "photos": [{"id": p.id, "file_path": p.file_path, "category": p.category,
                        "is_cover": p.is_cover, "sort_order": p.sort_order} for p in photos],
            "features": [{"feature_id": f.feature_id, "value": f.value} for f in features],
        }

    async def update_listing(self, listing_id: int, user_id: int, data) -> dict:
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            raise ValueError("Listing not found")
        if listing.user_id != user_id:
            raise ValueError("Not authorized")
        await self.repo.update_listing(listing_id, data.dict(exclude_unset=True))
        return {"status": "updated"}

    async def delete_listing(self, listing_id: int, user_id: int):
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            raise ValueError("Listing not found")
        if listing.user_id != user_id:
            raise ValueError("Not authorized")
        await self.repo.delete_listing(listing_id)

    async def list_listings(self, filters: dict = None, page: int = 1, limit: int = 20) -> dict:
        items, total = await self.repo.list_listings(filters, page, limit)
        return {
            "items": [self._listing_brief(l) for l in items],
            "total": total,
            "page": page,
            "limit": limit,
        }

    async def search_listings(self, query: str, filters: dict = None, page: int = 1, limit: int = 20) -> dict:
        items, total = await self.repo.search_listings(query, filters, page, limit)
        return {
            "items": [self._listing_brief(l) for l in items],
            "total": total,
            "page": page,
            "limit": limit,
        }

    def _listing_brief(self, l: PropertyListing) -> dict:
        return {
            "id": l.id,
            "title": l.title,
            "price": str(l.price),
            "currency": l.currency,
            "city": l.city,
            "district": l.district,
            "room_count": l.room_count,
            "net_area": str(l.net_area) if l.net_area else None,
            "status": l.status,
            "is_for_sale": l.is_for_sale,
            "is_for_rent": l.is_for_rent,
            "view_count": l.view_count,
            "is_highlighted": l.is_highlighted,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }

    async def increment_view_count(self, listing_id: int):
        await self.repo.increment_view_count(listing_id)

    async def get_listing_detail(self, listing_id: int, current_user_id: int = None) -> dict | None:
        detail = await self.get_listing(listing_id)
        if not detail:
            return None
        if current_user_id:
            detail["is_favorite"] = await self.repo.is_favorite(current_user_id, listing_id)
        benchmark = await self.calculate_region_benchmark(listing_id)
        if benchmark and "error" not in benchmark:
            detail["region_benchmark"] = benchmark
        return detail

    # ── Photos ──────────────────────────────────────────────

    async def add_photo(self, listing_id: int, data) -> dict:
        photo = PropertyPhoto(listing_id=listing_id, **data.dict(exclude_unset=True))
        await self.repo.add_photo(photo)
        await self.repo.db.flush()
        return {"id": photo.id, "file_path": photo.file_path, "is_cover": photo.is_cover}

    async def list_photos(self, listing_id: int) -> list[dict]:
        photos = await self.repo.list_photos(listing_id)
        return [{"id": p.id, "file_path": p.file_path, "category": p.category,
                 "description": p.description, "is_cover": p.is_cover,
                 "sort_order": p.sort_order} for p in photos]

    async def delete_photo(self, photo_id: int):
        photo = await self.repo.get_photo(photo_id)
        if not photo:
            raise ValueError("Photo not found")
        await self.repo.delete_photo(photo_id)

    async def set_cover_photo(self, photo_id: int):
        photo = await self.repo.get_photo(photo_id)
        if not photo:
            raise ValueError("Photo not found")
        await self.repo.set_cover_photo(photo_id, photo.listing_id)

    # ── Features ────────────────────────────────────────────

    async def create_feature(self, data) -> dict:
        feature = PropertyFeature(**data.dict())
        await self.repo.create_feature(feature)
        await self.repo.db.flush()
        return {"id": feature.id, "name": feature.name, "slug": feature.slug}

    async def list_features(self, category: str = None) -> list[dict]:
        features = await self.repo.list_features(category)
        return [{"id": f.id, "name": f.name, "slug": f.slug, "icon": f.icon,
                 "category": f.category, "sort_order": f.sort_order} for f in features]

    async def add_listing_features(self, listing_id: int, features: list[dict]) -> dict:
        await self.repo.add_listing_features(listing_id, features)
        return {"status": "features_added", "count": len(features)}

    async def get_listing_features(self, listing_id: int) -> list[dict]:
        features = await self.repo.get_listing_features(listing_id)
        return [{"listing_id": f.listing_id, "feature_id": f.feature_id, "value": f.value} for f in features]

    async def remove_listing_feature(self, listing_id: int, feature_id: int):
        await self.repo.remove_listing_feature(listing_id, feature_id)

    # ── Contractors ─────────────────────────────────────────

    async def create_company(self, data) -> dict:
        company = ContractorCompany(**data.dict())
        await self.repo.create_company(company)
        await self.repo.db.flush()
        return {"id": company.id, "name": company.name, "slug": company.slug}

    async def get_company(self, company_id: int) -> dict | None:
        company = await self.repo.get_company(company_id)
        if not company:
            return None
        return {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "tax_no": company.tax_no,
            "phone": company.phone,
            "email": company.email,
            "address": company.address,
            "website": company.website,
            "logo_url": company.logo_url,
            "description": company.description,
            "rating": str(company.rating),
            "review_count": company.review_count,
            "is_verified": company.is_verified,
            "is_active": company.is_active,
            "created_at": company.created_at.isoformat() if company.created_at else None,
        }

    async def list_companies(self, query: str = None, is_verified: bool = None) -> list[dict]:
        companies = await self.repo.list_companies(query, is_verified)
        return [{"id": c.id, "name": c.name, "slug": c.slug, "rating": str(c.rating),
                 "review_count": c.review_count, "is_verified": c.is_verified,
                 "logo_url": c.logo_url} for c in companies]

    # ── Contractor Reviews ──────────────────────────────────

    async def create_review(self, company_id: int, user_id: int, data) -> dict:
        review = ContractorReview(company_id=company_id, user_id=user_id, **data.dict(exclude_unset=True))
        await self.repo.create_review(review)
        await self.repo.db.flush()
        await self.repo.update_company_rating(company_id)
        return {"id": review.id, "rating": review.rating, "status": "created"}

    async def list_reviews(self, company_id: int) -> list[dict]:
        reviews = await self.repo.list_reviews(company_id)
        return [{"id": r.id, "user_id": r.user_id, "rating": r.rating,
                 "comment": r.comment, "created_at": r.created_at.isoformat() if r.created_at else None}
                for r in reviews]

    # ── Authorizations ──────────────────────────────────────

    async def create_authorization(self, data) -> dict:
        auth = AuthorizationRequest(**data.dict())
        await self.repo.create_authorization(auth)
        await self.repo.db.flush()
        return {"id": auth.id, "status": auth.status}

    async def list_authorizations(self, owner_id: int = None, company_id: int = None, status: str = None) -> list[dict]:
        auths = await self.repo.list_authorizations(owner_id, company_id, status)
        return [{"id": a.id, "listing_id": a.listing_id, "owner_id": a.owner_id,
                 "company_id": a.company_id, "auth_type": a.auth_type,
                 "status": a.status, "created_at": a.created_at.isoformat() if a.created_at else None}
                for a in auths]

    async def update_authorization_status(self, auth_id: int, status: str) -> dict:
        auth = await self.repo.get_authorization(auth_id)
        if not auth:
            raise ValueError("Authorization not found")
        await self.repo.update_authorization_status(auth_id, status)
        return {"id": auth_id, "status": status}

    # ── Appraisal ───────────────────────────────────────────

    async def create_appraisal_request(self, user_id: int, data) -> dict:
        req = PropertyAppraisalRequest(user_id=user_id, **data.dict(exclude_unset=True))
        await self.repo.create_appraisal_request(req)
        await self.repo.db.flush()
        return {"id": req.id, "status": req.status}

    async def get_appraisal_request(self, appraisal_id: int) -> dict | None:
        req = await self.repo.get_appraisal_request(appraisal_id)
        if not req:
            return None
        return {
            "id": req.id,
            "user_id": req.user_id,
            "listing_id": req.listing_id,
            "company_id": req.company_id,
            "city": req.city,
            "district": req.district,
            "status": req.status,
            "notes": req.notes,
            "report_data": req.report_data,
            "report_file_url": req.report_file_url,
            "requested_date": req.requested_date.isoformat() if req.requested_date else None,
            "completed_date": req.completed_date.isoformat() if req.completed_date else None,
            "created_at": req.created_at.isoformat() if req.created_at else None,
        }

    async def list_appraisal_requests(self, user_id: int = None, status: str = None) -> list[dict]:
        reqs = await self.repo.list_appraisal_requests(user_id, status)
        return [{"id": r.id, "city": r.city, "district": r.district, "status": r.status,
                 "created_at": r.created_at.isoformat() if r.created_at else None} for r in reqs]

    async def update_appraisal_status(self, appraisal_id: int, status: str, report_data: dict = None) -> dict:
        req = await self.repo.get_appraisal_request(appraisal_id)
        if not req:
            raise ValueError("Appraisal request not found")
        await self.repo.update_appraisal_status(appraisal_id, status, report_data)
        return {"id": appraisal_id, "status": status}

    # ── Favorites ───────────────────────────────────────────

    async def add_favorite(self, user_id: int, listing_id: int) -> dict:
        existing = await self.repo.is_favorite(user_id, listing_id)
        if existing:
            return {"status": "already_favorite"}
        await self.repo.add_favorite(user_id, listing_id)
        return {"status": "added"}

    async def remove_favorite(self, user_id: int, listing_id: int):
        await self.repo.remove_favorite(user_id, listing_id)

    async def list_favorites(self, user_id: int) -> list[dict]:
        listings = await self.repo.list_favorites(user_id)
        return [self._listing_brief(l) for l in listings]

    # ── Inquiries ───────────────────────────────────────────

    async def send_inquiry(self, data) -> dict:
        inquiry = PropertyInquiry(**data.dict())
        await self.repo.send_inquiry(inquiry)
        await self.repo.db.flush()
        return {"id": inquiry.id, "status": "sent"}

    async def list_inquiries(self, listing_id: int = None, user_id: int = None,
                            is_incoming: bool = None) -> list[dict]:
        inquiries = await self.repo.list_inquiries(listing_id, user_id, is_incoming)
        return [{"id": q.id, "listing_id": q.listing_id, "from_user_id": q.from_user_id,
                 "to_user_id": q.to_user_id, "message": q.message, "is_read": q.is_read,
                 "parent_id": q.parent_id,
                 "created_at": q.created_at.isoformat() if q.created_at else None} for q in inquiries]

    async def mark_as_read(self, inquiry_id: int):
        await self.repo.mark_as_read(inquiry_id)

    async def mark_thread_read(self, listing_id: int, to_user_id: int):
        await self.repo.mark_thread_read(listing_id, to_user_id)

    # ── Combined ────────────────────────────────────────────

    async def search_with_filters(self, query: str = None, filters: dict = None,
                                  page: int = 1, limit: int = 20) -> dict:
        if query:
            return await self.search_listings(query, filters, page, limit)
        return await self.list_listings(filters, page, limit)

    async def create_full_listing(self, user_id: int, listing_data, photo_data: list = None,
                                  feature_ids: list[dict] = None) -> dict:
        listing = PropertyListing(user_id=user_id, **listing_data.dict(exclude_unset=True))
        await self.repo.create_listing(listing)
        await self.repo.db.flush()

        if photo_data:
            for p in photo_data:
                photo = PropertyPhoto(listing_id=listing.id, **p.dict() if hasattr(p, 'dict') else p)
                await self.repo.add_photo(photo)

        if feature_ids:
            await self.repo.add_listing_features(listing.id, feature_ids)

        await self.repo.db.flush()
        return {"id": listing.id, "title": listing.title, "status": "created"}

    async def request_appraisal(self, user_id: int, data) -> dict:
        req = PropertyAppraisalRequest(user_id=user_id, **data.dict(exclude_unset=True))
        await self.repo.create_appraisal_request(req)
        await self.repo.db.flush()
        return {"id": req.id, "status": req.status, "message": "Appraisal request submitted"}

    # ── Company Members ─────────────────────────────────────

    async def create_member(self, company_id: int, admin_user_id: int, data) -> dict:
        admin = await self.repo.get_member(company_id, admin_user_id)
        if not admin or admin.role not in ("admin", "owner"):
            raise ValueError("Only company admins can add members")
        member = await self.repo.create_member(
            company_id=company_id,
            user_id=data.get("user_id"),
            role=data.get("role", "agent"),
            title=data.get("title"),
        )
        return {"id": member.id, "user_id": member.user_id, "role": member.role, "title": member.title}

    async def list_members(self, company_id: int) -> list[dict]:
        members = await self.repo.list_members(company_id)
        return [{
            "id": m.id, "company_id": m.company_id, "user_id": m.user_id,
            "role": m.role, "title": m.title, "is_active": m.is_active,
            "joined_at": m.joined_at.isoformat() if m.joined_at else None,
        } for m in members]

    async def update_member_role(self, member_id: int, data) -> dict:
        member = await self.repo.get_member_by_id(member_id)
        if not member:
            raise ValueError("Member not found")
        await self.repo.update_member_role(
            member_id,
            role=data.get("role"),
            title=data.get("title"),
        )
        return {"id": member_id, "status": "updated"}

    async def remove_member(self, member_id: int):
        member = await self.repo.get_member_by_id(member_id)
        if not member:
            raise ValueError("Member not found")
        await self.repo.remove_member(member_id)

    # ── Company Invitations ──────────────────────────────────

    async def create_invitation(self, company_id: int, inviter_id: int, data) -> dict:
        invitation = await self.repo.create_invitation(
            company_id=company_id,
            inviter_id=inviter_id,
            invitee_id=data.get("invitee_id"),
            invitee_email=data.get("invitee_email"),
            role=data.get("role", "agent"),
            message=data.get("message"),
        )
        return {
            "id": invitation.id, "company_id": invitation.company_id,
            "invitee_email": invitation.invitee_email, "role": invitation.role,
            "status": invitation.status,
        }

    async def list_invitations(self, company_id: int) -> list[dict]:
        invitations = await self.repo.list_invitations(company_id)
        return [{
            "id": i.id, "company_id": i.company_id, "inviter_id": i.inviter_id,
            "invitee_id": i.invitee_id, "invitee_email": i.invitee_email,
            "role": i.role, "status": i.status, "message": i.message,
            "created_at": i.created_at.isoformat() if i.created_at else None,
        } for i in invitations]

    async def respond_to_invitation(self, invitation_id: int, invitee_id: int, accept: bool) -> dict:
        invitation = await self.repo.get_invitation(invitation_id)
        if not invitation:
            raise ValueError("Invitation not found")
        if invitation.invitee_id != invitee_id:
            raise ValueError("This invitation is not for you")
        if invitation.status != "pending":
            raise ValueError("Invitation is not pending")
        if accept:
            await self.repo.create_member(
                company_id=invitation.company_id,
                user_id=invitee_id,
                role=invitation.role,
            )
            await self.repo.update_invitation_status(invitation_id, "accepted")
            return {"status": "accepted", "company_id": invitation.company_id}
        else:
            await self.repo.update_invitation_status(invitation_id, "rejected")
            return {"status": "rejected"}

    async def get_user_companies(self, user_id: int) -> list[dict]:
        companies = await self.repo.list_user_companies(user_id)
        return [{
            "id": c.id, "name": c.name, "slug": c.slug,
            "logo_url": c.logo_url, "is_verified": c.is_verified,
        } for c in companies]

    # ── Listing Pricing / Payments ──────────────────────────────

    async def get_listing_price(self, domain: str, user_role: str = 'company') -> dict | None:
        cfg = await self.repo.get_listing_price(domain, user_role)
        if not cfg:
            return None
        return {
            "id": cfg.id,
            "domain": cfg.domain,
            "price": str(cfg.price),
            "currency": cfg.currency,
            "user_role": cfg.user_role,
            "description": cfg.description,
            "is_active": cfg.is_active,
        }

    async def pay_for_listing(self, domain: str, listing_id: int, user_id: int, payment_method: str, user_role: str = 'company') -> dict:
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            raise ValueError("Listing not found")
        if listing.user_id != user_id:
            raise ValueError("Not authorized")
        if listing.status != "pending_payment":
            raise ValueError("Listing is not in pending_payment status")

        cfg = await self.repo.get_listing_price(domain, user_role)
        if not cfg or not cfg.is_active:
            raise ValueError("No active price config for this domain")

        payment = ListingPayment(
            domain=domain,
            listing_id=listing_id,
            user_id=user_id,
            amount=cfg.price,
            currency=cfg.currency,
            payment_method=payment_method,
            status="completed",
            paid_at=datetime.now(timezone.utc),
        )
        payment = await self.repo.create_payment(payment)

        await self.repo.update_listing(listing_id, {"status": "active"})

        return {
            "id": payment.id,
            "amount": str(payment.amount),
            "currency": payment.currency,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
        }

    async def calculate_region_benchmark(self, listing_id: int) -> dict | None:
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            return None
        if not listing.city or not listing.district or not listing.type_id:
            return {"error": "Listing missing city, district, or property type"}

        from sqlalchemy import func as sa_func

        district_stmt = select(
            sa_func.avg(PropertyListing.price / sa_func.nullif(PropertyListing.net_area, 0)),
            sa_func.min(PropertyListing.price),
            sa_func.max(PropertyListing.price),
            sa_func.count(PropertyListing.id),
        ).where(
            PropertyListing.city == listing.city,
            PropertyListing.district == listing.district,
            PropertyListing.type_id == listing.type_id,
            PropertyListing.status == 'active',
            PropertyListing.id != listing_id,
            PropertyListing.net_area.isnot(None),
            PropertyListing.net_area > 0,
        )
        district_result = await self.repo.db.execute(district_stmt)
        district_avg, district_min, district_max, district_count = district_result.one()

        city_stmt = select(
            sa_func.avg(PropertyListing.price / sa_func.nullif(PropertyListing.net_area, 0)),
        ).where(
            PropertyListing.city == listing.city,
            PropertyListing.type_id == listing.type_id,
            PropertyListing.status == 'active',
            PropertyListing.id != listing_id,
            PropertyListing.net_area.isnot(None),
            PropertyListing.net_area > 0,
        )
        city_result = await self.repo.db.execute(city_stmt)
        city_avg = city_result.scalar()

        listing_price_per_m2 = None
        if listing.net_area and float(listing.net_area) > 0:
            listing_price_per_m2 = float(listing.price) / float(listing.net_area)

        district_diff = None
        if district_avg and listing_price_per_m2:
            district_diff = ((listing_price_per_m2 - float(district_avg)) / float(district_avg)) * 100

        city_diff = None
        if city_avg and listing_price_per_m2:
            city_diff = ((listing_price_per_m2 - float(city_avg)) / float(city_avg)) * 100

        return {
            "listing_id": listing_id,
            "listing_price": str(listing.price),
            "listing_area": str(listing.net_area),
            "listing_price_per_m2": round(listing_price_per_m2, 2) if listing_price_per_m2 else None,
            "district": {
                "name": listing.district,
                "avg_price_per_m2": round(float(district_avg), 2) if district_avg else None,
                "min_price": str(district_min) if district_min else None,
                "max_price": str(district_max) if district_max else None,
                "comparable_count": district_count,
            },
            "city": {
                "name": listing.city,
                "avg_price_per_m2": round(float(city_avg), 2) if city_avg else None,
            },
            "percentage_diff_from_district": round(district_diff, 2) if district_diff is not None else None,
            "percentage_diff_from_city": round(city_diff, 2) if city_diff is not None else None,
        }

    async def check_listing_paid(self, domain: str, listing_id: int) -> bool:
        payment = await self.repo.get_payment_by_listing(domain, listing_id)
        return payment is not None and payment.status == "completed"

    # ── Documents ──────────────────────────────────────────────

    async def upload_document(self, domain: str, listing_id: int, user_id, data: dict) -> dict:
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            raise ValueError("Listing not found")
        if listing.user_id != user_id:
            raise ValueError("Not authorized")

        doc = ListingDocument(
            domain=domain,
            listing_id=listing_id,
            user_id=user_id,
            document_type=data.get("document_type"),
            document_number=data.get("document_number"),
            file_path=data.get("file_path"),
            file_name=data.get("file_name"),
            file_size=data.get("file_size"),
            mime_type=data.get("mime_type"),
            description=data.get("description"),
            status="pending",
        )
        doc = await self.repo.create_document(doc)
        return {
            "id": doc.id,
            "document_type": doc.document_type,
            "document_number": doc.document_number,
            "file_path": doc.file_path,
            "file_name": doc.file_name,
            "status": doc.status,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
        }

    async def submit_for_verification(self, domain: str, listing_id: int, user_id):
        listing = await self.repo.get_listing(listing_id)
        if not listing:
            raise ValueError("Listing not found")
        if listing.user_id != user_id:
            raise ValueError("Not authorized")
        if listing.status != "draft":
            raise ValueError("Listing must be in draft status to submit for verification")

        docs = await self.repo.list_documents(domain, listing_id)
        if not docs:
            raise ValueError("No documents uploaded. Upload at least one document first.")

        await self.repo.update_listing(listing_id, {"status": "pending_verification"})
        return {"status": "pending_verification", "listing_id": listing_id}

    async def verify_document(self, doc_id: int, admin_id, action: str, reason: str = None) -> dict:
        doc = await self.repo.get_document(doc_id)
        if not doc:
            raise ValueError("Document not found")
        if doc.status != "pending":
            raise ValueError(f"Document is already {doc.status}")

        if action == "verify":
            new_status = "verified"
        elif action == "reject":
            new_status = "rejected"
        else:
            raise ValueError("Action must be 'verify' or 'reject'")

        await self.repo.update_document_status(doc_id, new_status, rejection_reason=reason, verified_by=admin_id)
        await self.repo.create_verification_record(doc_id, admin_id, action, reason)

        if new_status == "verified":
            verified_count = await self.repo.count_documents_by_status(doc.listing_id, doc.domain, "verified")
            pending_count = await self.repo.count_documents_by_status(doc.listing_id, doc.domain, "pending")
            total_docs = len(await self.repo.list_documents(doc.domain, doc.listing_id))
            if verified_count == total_docs and pending_count == 0:
                await self.repo.update_listing(doc.listing_id, {"status": "pending_payment"})
                return {"status": new_status, "listing_status": "pending_payment", "listing_id": doc.listing_id}

        return {"status": new_status, "listing_id": doc.listing_id}

    async def get_listing_documents(self, domain: str, listing_id: int) -> list[dict]:
        docs = await self.repo.list_documents(domain, listing_id)
        return [{
            "id": d.id,
            "listing_id": d.listing_id,
            "document_type": d.document_type,
            "document_number": d.document_number,
            "file_path": d.file_path,
            "file_name": d.file_name,
            "file_size": d.file_size,
            "mime_type": d.mime_type,
            "description": d.description,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        } for d in docs]

    async def get_user_documents(self, user_id, domain: str) -> list[dict]:
        docs = await self.repo.list_user_documents(user_id, domain)
        return [{
            "id": d.id,
            "listing_id": d.listing_id,
            "document_type": d.document_type,
            "document_number": d.document_number,
            "file_path": d.file_path,
            "file_name": d.file_name,
            "file_size": d.file_size,
            "mime_type": d.mime_type,
            "description": d.description,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        } for d in docs]

    # ── Company Documents ───────────────────────────────────────

    async def upload_company_document(self, company_id: int, user_id, data: dict) -> dict:
        company = await self.repo.get_company(company_id)
        if not company:
            raise ValueError("Company not found")
        doc = await self.repo.create_company_document(company_id, user_id, data)
        return {
            "id": doc.id,
            "company_id": doc.company_id,
            "document_type": doc.document_type,
            "document_number": doc.document_number,
            "file_path": doc.file_path,
            "file_name": doc.file_name,
            "status": doc.status,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
        }

    async def list_company_documents(self, company_id: int) -> list[dict]:
        docs = await self.repo.list_company_documents(company_id)
        return [{
            "id": d.id,
            "company_id": d.company_id,
            "document_type": d.document_type,
            "document_number": d.document_number,
            "file_path": d.file_path,
            "file_name": d.file_name,
            "file_size": d.file_size,
            "mime_type": d.mime_type,
            "description": d.description,
            "status": d.status,
            "rejection_reason": d.rejection_reason,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        } for d in docs]

    # ── Company Verification ────────────────────────────────────

    async def submit_company_for_verification(self, company_id: int, user_id) -> dict:
        company = await self.repo.get_company(company_id)
        if not company:
            raise ValueError("Company not found")
        if company.verification_status != "pending":
            raise ValueError(f"Company verification is already {company.verification_status}")
        docs = await self.repo.list_company_documents(company_id)
        if not docs:
            raise ValueError("Upload at least one document before submitting for verification")
        await self.repo.update_company_verification(company_id, "documents_uploaded")
        return {"status": "documents_uploaded", "company_id": company_id}

    async def verify_company(self, company_id: int, admin_id, action: str, reason: str = None) -> dict:
        company = await self.repo.get_company(company_id)
        if not company:
            raise ValueError("Company not found")
        if company.verification_status not in ("pending", "documents_uploaded"):
            raise ValueError(f"Cannot verify company with status: {company.verification_status}")
        if action == "verify":
            new_status = "verified"
        elif action == "reject":
            new_status = "rejected"
        else:
            raise ValueError("Action must be 'verify' or 'reject'")
        await self.repo.update_company_verification(company_id, new_status, note=reason, verified_by=admin_id)
        return {
            "company_id": company_id,
            "verification_status": new_status,
            "is_verified": new_status == "verified",
            "is_active": new_status != "rejected",
        }

    async def get_company_verification_status(self, company_id: int) -> dict | None:
        company = await self.repo.get_company(company_id)
        if not company:
            return None
        return {
            "company_id": company.id,
            "verification_status": company.verification_status,
            "verification_note": company.verification_note,
            "verified_at": company.verified_at.isoformat() if company.verified_at else None,
            "certificate_no": company.certificate_no,
            "certificate_expiry": company.certificate_expiry.isoformat() if company.certificate_expiry else None,
            "is_verified": company.is_verified,
            "is_active": company.is_active,
        }
