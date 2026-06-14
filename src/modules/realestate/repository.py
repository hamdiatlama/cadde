from sqlalchemy import select, func, and_, or_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.realestate.models import (
    PropertyCategory, PropertyType, ContractorCompany, ContractorReview,
    PropertyListing, PropertyPhoto, PropertyFeature, PropertyListingFeature,
    AuthorizationRequest, PropertyAppraisalRequest, FavoriteListing, PropertyInquiry,
    PropertyLandContent, CompanyMember, CompanyInvitation,
    ListingPriceConfig, ListingPayment,
    ListingDocument, DocumentVerification,
)


class RealEstateRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── Categories ─────────────────────────────────────────

    async def create_category(self, obj: PropertyCategory):
        self.db.add(obj)

    async def list_categories(self):
        r = await self.db.execute(select(PropertyCategory).order_by(PropertyCategory.sort_order))
        return r.scalars().all()

    async def get_category(self, category_id: int):
        r = await self.db.execute(select(PropertyCategory).where(PropertyCategory.id == category_id))
        return r.scalar_one_or_none()

    # ── Types ───────────────────────────────────────────────

    async def create_type(self, obj: PropertyType):
        self.db.add(obj)

    async def list_types(self):
        r = await self.db.execute(select(PropertyType).order_by(PropertyType.sort_order))
        return r.scalars().all()

    async def get_type(self, type_id: int):
        r = await self.db.execute(select(PropertyType).where(PropertyType.id == type_id))
        return r.scalar_one_or_none()

    # ── Listings ────────────────────────────────────────────

    async def create_listing(self, obj: PropertyListing):
        self.db.add(obj)

    async def get_listing(self, listing_id: int) -> PropertyListing | None:
        r = await self.db.execute(
            select(PropertyListing).where(PropertyListing.id == listing_id)
        )
        return r.scalar_one_or_none()

    async def update_listing(self, listing_id: int, data: dict):
        await self.db.execute(
            PropertyListing.__table__.update()
            .where(PropertyListing.id == listing_id)
            .values(**data, updated_at=func.now())
        )

    async def delete_listing(self, listing_id: int):
        await self.db.execute(PropertyListing.__table__.delete().where(PropertyListing.id == listing_id))

    async def list_listings(self, filters: dict = None, page: int = 1, limit: int = 20):
        q = select(PropertyListing)
        conditions = []
        if filters:
            if filters.get("category_id"):
                conditions.append(PropertyListing.category_id == filters["category_id"])
            if filters.get("type_id"):
                conditions.append(PropertyListing.type_id == filters["type_id"])
            if filters.get("city"):
                conditions.append(PropertyListing.city == filters["city"])
            if filters.get("district"):
                conditions.append(PropertyListing.district == filters["district"])
            if filters.get("min_price"):
                conditions.append(PropertyListing.price >= filters["min_price"])
            if filters.get("max_price"):
                conditions.append(PropertyListing.price <= filters["max_price"])
            if filters.get("room_count"):
                conditions.append(PropertyListing.room_count == filters["room_count"])
            if filters.get("status"):
                conditions.append(PropertyListing.status == filters["status"])
            if filters.get("is_for_sale") is not None:
                conditions.append(PropertyListing.is_for_sale == filters["is_for_sale"])
            if filters.get("is_for_rent") is not None:
                conditions.append(PropertyListing.is_for_rent == filters["is_for_rent"])
        if conditions:
            q = q.where(and_(*conditions))

        sort_by = (filters or {}).get("sort_by", "-created_at")
        if sort_by == "price":
            q = q.order_by(PropertyListing.price)
        elif sort_by == "-price":
            q = q.order_by(PropertyListing.price.desc())
        elif sort_by == "created_at":
            q = q.order_by(PropertyListing.created_at)
        elif sort_by == "view_count":
            q = q.order_by(PropertyListing.view_count.desc())
        else:
            q = q.order_by(PropertyListing.created_at.desc())

        offset = (page - 1) * limit
        r = await self.db.execute(q.offset(offset).limit(limit))
        items = r.scalars().all()

        count_q = select(func.count(PropertyListing.id))
        if conditions:
            count_q = count_q.where(and_(*conditions))
        total_r = await self.db.execute(count_q)
        total = total_r.scalar()

        return items, total

    async def increment_view_count(self, listing_id: int):
        await self.db.execute(
            PropertyListing.__table__.update()
            .where(PropertyListing.id == listing_id)
            .values(view_count=PropertyListing.view_count + 1)
        )

    async def search_listings(self, query: str, filters: dict = None, page: int = 1, limit: int = 20):
        q = select(PropertyListing)
        conditions = [
            or_(
                PropertyListing.title.ilike(f"%{query}%"),
                PropertyListing.description.ilike(f"%{query}%"),
                PropertyListing.city.ilike(f"%{query}%"),
                PropertyListing.district.ilike(f"%{query}%"),
                PropertyListing.neighborhood.ilike(f"%{query}%"),
            )
        ]
        if filters:
            if filters.get("category_id"):
                conditions.append(PropertyListing.category_id == filters["category_id"])
            if filters.get("type_id"):
                conditions.append(PropertyListing.type_id == filters["type_id"])
            if filters.get("city"):
                conditions.append(PropertyListing.city == filters["city"])
            if filters.get("min_price"):
                conditions.append(PropertyListing.price >= filters["min_price"])
            if filters.get("max_price"):
                conditions.append(PropertyListing.price <= filters["max_price"])
            if filters.get("room_count"):
                conditions.append(PropertyListing.room_count == filters["room_count"])
            if filters.get("status"):
                conditions.append(PropertyListing.status == filters["status"])

        q = q.where(and_(*conditions)).order_by(PropertyListing.created_at.desc())
        offset = (page - 1) * limit
        r = await self.db.execute(q.offset(offset).limit(limit))
        items = r.scalars().all()

        count_q = select(func.count(PropertyListing.id)).where(and_(*conditions))
        total_r = await self.db.execute(count_q)
        total = total_r.scalar()

        return items, total

    # ── Photos ──────────────────────────────────────────────

    async def add_photo(self, obj: PropertyPhoto):
        self.db.add(obj)

    async def list_photos(self, listing_id: int):
        r = await self.db.execute(
            select(PropertyPhoto)
            .where(PropertyPhoto.listing_id == listing_id)
            .order_by(PropertyPhoto.sort_order)
        )
        return r.scalars().all()

    async def get_photo(self, photo_id: int) -> PropertyPhoto | None:
        r = await self.db.execute(select(PropertyPhoto).where(PropertyPhoto.id == photo_id))
        return r.scalar_one_or_none()

    async def delete_photo(self, photo_id: int):
        await self.db.execute(PropertyPhoto.__table__.delete().where(PropertyPhoto.id == photo_id))

    async def set_cover_photo(self, photo_id: int, listing_id: int):
        await self.db.execute(
            PropertyPhoto.__table__.update()
            .where(PropertyPhoto.listing_id == listing_id)
            .values(is_cover=False)
        )
        await self.db.execute(
            PropertyPhoto.__table__.update()
            .where(PropertyPhoto.id == photo_id)
            .values(is_cover=True)
        )

    # ── Features ────────────────────────────────────────────

    async def create_feature(self, obj: PropertyFeature):
        self.db.add(obj)

    async def list_features(self, category: str = None):
        q = select(PropertyFeature)
        if category:
            q = q.where(PropertyFeature.category == category)
        q = q.order_by(PropertyFeature.sort_order)
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_feature(self, feature_id: int) -> PropertyFeature | None:
        r = await self.db.execute(select(PropertyFeature).where(PropertyFeature.id == feature_id))
        return r.scalar_one_or_none()

    async def add_listing_features(self, listing_id: int, features: list[dict]):
        for f in features:
            obj = PropertyListingFeature(
                listing_id=listing_id,
                feature_id=f["feature_id"],
                value=f.get("value"),
            )
            self.db.add(obj)

    async def get_listing_features(self, listing_id: int):
        r = await self.db.execute(
            select(PropertyListingFeature)
            .where(PropertyListingFeature.listing_id == listing_id)
        )
        return r.scalars().all()

    async def remove_listing_feature(self, listing_id: int, feature_id: int):
        await self.db.execute(
            PropertyListingFeature.__table__.delete()
            .where(
                PropertyListingFeature.listing_id == listing_id,
                PropertyListingFeature.feature_id == feature_id,
            )
        )

    # ── Contractors ─────────────────────────────────────────

    async def create_company(self, obj: ContractorCompany):
        self.db.add(obj)

    async def get_company(self, company_id: int) -> ContractorCompany | None:
        r = await self.db.execute(select(ContractorCompany).where(ContractorCompany.id == company_id))
        return r.scalar_one_or_none()

    async def list_companies(self, query: str = None, is_verified: bool = None):
        q = select(ContractorCompany)
        conditions = []
        if query:
            conditions.append(ContractorCompany.name.ilike(f"%{query}%"))
        if is_verified is not None:
            conditions.append(ContractorCompany.is_verified == is_verified)
        conditions.append(ContractorCompany.is_active == True)
        if conditions:
            q = q.where(and_(*conditions))
        q = q.order_by(ContractorCompany.rating.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    # ── Contractor Reviews ──────────────────────────────────

    async def create_review(self, obj: ContractorReview):
        self.db.add(obj)

    async def list_reviews(self, company_id: int):
        r = await self.db.execute(
            select(ContractorReview)
            .where(ContractorReview.company_id == company_id)
            .order_by(ContractorReview.created_at.desc())
        )
        return r.scalars().all()

    async def update_company_rating(self, company_id: int):
        r = await self.db.execute(
            select(
                func.coalesce(func.round(func.avg(ContractorReview.rating), 1), 0),
                func.count(ContractorReview.id),
            ).where(ContractorReview.company_id == company_id)
        )
        avg_rating, review_count = r.one()
        await self.db.execute(
            ContractorCompany.__table__.update()
            .where(ContractorCompany.id == company_id)
            .values(rating=avg_rating, review_count=review_count)
        )

    # ── Authorizations ──────────────────────────────────────

    async def create_authorization(self, obj: AuthorizationRequest):
        self.db.add(obj)

    async def list_authorizations(self, owner_id: int = None, company_id: int = None, status: str = None):
        q = select(AuthorizationRequest)
        conditions = []
        if owner_id:
            conditions.append(AuthorizationRequest.owner_id == owner_id)
        if company_id:
            conditions.append(AuthorizationRequest.company_id == company_id)
        if status:
            conditions.append(AuthorizationRequest.status == status)
        if conditions:
            q = q.where(and_(*conditions))
        q = q.order_by(AuthorizationRequest.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_authorization(self, auth_id: int) -> AuthorizationRequest | None:
        r = await self.db.execute(select(AuthorizationRequest).where(AuthorizationRequest.id == auth_id))
        return r.scalar_one_or_none()

    async def update_authorization_status(self, auth_id: int, status: str):
        await self.db.execute(
            AuthorizationRequest.__table__.update()
            .where(AuthorizationRequest.id == auth_id)
            .values(status=status, updated_at=func.now())
        )

    # ── Appraisal ───────────────────────────────────────────

    async def create_appraisal_request(self, obj: PropertyAppraisalRequest):
        self.db.add(obj)

    async def get_appraisal_request(self, appraisal_id: int) -> PropertyAppraisalRequest | None:
        r = await self.db.execute(
            select(PropertyAppraisalRequest).where(PropertyAppraisalRequest.id == appraisal_id)
        )
        return r.scalar_one_or_none()

    async def list_appraisal_requests(self, user_id: int = None, status: str = None):
        q = select(PropertyAppraisalRequest)
        conditions = []
        if user_id:
            conditions.append(PropertyAppraisalRequest.user_id == user_id)
        if status:
            conditions.append(PropertyAppraisalRequest.status == status)
        if conditions:
            q = q.where(and_(*conditions))
        q = q.order_by(PropertyAppraisalRequest.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def update_appraisal_status(self, appraisal_id: int, status: str, report_data: dict = None):
        values = {"status": status, "updated_at": func.now()}
        if report_data is not None:
            values["report_data"] = report_data
        if status == "completed":
            values["completed_date"] = func.now()
        await self.db.execute(
            PropertyAppraisalRequest.__table__.update()
            .where(PropertyAppraisalRequest.id == appraisal_id)
            .values(**values)
        )

    # ── Favorites ───────────────────────────────────────────

    async def add_favorite(self, user_id: int, listing_id: int):
        obj = FavoriteListing(user_id=user_id, listing_id=listing_id)
        self.db.add(obj)

    async def remove_favorite(self, user_id: int, listing_id: int):
        await self.db.execute(
            FavoriteListing.__table__.delete().where(
                FavoriteListing.user_id == user_id,
                FavoriteListing.listing_id == listing_id,
            )
        )

    async def list_favorites(self, user_id: int):
        r = await self.db.execute(
            select(PropertyListing)
            .join(FavoriteListing, PropertyListing.id == FavoriteListing.listing_id)
            .where(FavoriteListing.user_id == user_id)
            .order_by(PropertyListing.created_at.desc())
        )
        return r.scalars().all()

    async def is_favorite(self, user_id: int, listing_id: int) -> bool:
        r = await self.db.execute(
            select(FavoriteListing).where(
                FavoriteListing.user_id == user_id,
                FavoriteListing.listing_id == listing_id,
            )
        )
        return r.scalar_one_or_none() is not None

    # ── Inquiries ───────────────────────────────────────────

    async def send_inquiry(self, obj: PropertyInquiry):
        self.db.add(obj)

    async def list_inquiries(self, listing_id: int = None, user_id: int = None, is_incoming: bool = None):
        q = select(PropertyInquiry)
        conditions = []
        if listing_id:
            conditions.append(PropertyInquiry.listing_id == listing_id)
        if user_id is not None and is_incoming is not None:
            if is_incoming:
                conditions.append(PropertyInquiry.to_user_id == user_id)
            else:
                conditions.append(PropertyInquiry.from_user_id == user_id)
        elif user_id is not None:
            conditions.append(
                or_(PropertyInquiry.from_user_id == user_id, PropertyInquiry.to_user_id == user_id)
            )
        if conditions:
            q = q.where(and_(*conditions))
        q = q.order_by(PropertyInquiry.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_inquiry(self, inquiry_id: int) -> PropertyInquiry | None:
        r = await self.db.execute(select(PropertyInquiry).where(PropertyInquiry.id == inquiry_id))
        return r.scalar_one_or_none()

    async def mark_as_read(self, inquiry_id: int):
        await self.db.execute(
            PropertyInquiry.__table__.update()
            .where(PropertyInquiry.id == inquiry_id)
            .values(is_read=True)
        )

    async def mark_thread_read(self, listing_id: int, to_user_id: int):
        await self.db.execute(
            PropertyInquiry.__table__.update()
            .where(
                PropertyInquiry.listing_id == listing_id,
                PropertyInquiry.to_user_id == to_user_id,
                PropertyInquiry.is_read == False,
            )
            .values(is_read=True)
        )

    # ── Land Contents ──────────────────────────────────────────

    async def list_land_contents(self, listing_id: int):
        r = await self.db.execute(
            select(PropertyLandContent).where(PropertyLandContent.listing_id == listing_id).order_by(PropertyLandContent.sort_order)
        )
        return r.scalars().all()

    async def create_land_content(self, obj: PropertyLandContent):
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def update_land_content(self, content_id: int, data: dict):
        await self.db.execute(
            PropertyLandContent.__table__.update().where(PropertyLandContent.id == content_id).values(**data)
        )

    async def delete_land_content(self, content_id: int):
        await self.db.execute(delete(PropertyLandContent).where(PropertyLandContent.id == content_id))

    # ── Company Members ─────────────────────────────────────

    async def create_member(self, company_id: int, user_id: int, role: str = "agent", title: str = None):
        obj = CompanyMember(company_id=company_id, user_id=user_id, role=role, title=title)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def list_members(self, company_id: int):
        r = await self.db.execute(
            select(CompanyMember).where(CompanyMember.company_id == company_id).order_by(CompanyMember.joined_at)
        )
        return r.scalars().all()

    async def get_member(self, company_id: int, user_id: int):
        r = await self.db.execute(
            select(CompanyMember).where(
                CompanyMember.company_id == company_id,
                CompanyMember.user_id == user_id,
            )
        )
        return r.scalar_one_or_none()

    async def update_member_role(self, member_id: int, role: str = None, title: str = None):
        values = {k: v for k, v in {"role": role, "title": title, "updated_at": func.now()}.items() if v is not None}
        await self.db.execute(
            CompanyMember.__table__.update().where(CompanyMember.id == member_id).values(**values)
        )

    async def remove_member(self, member_id: int):
        await self.db.execute(CompanyMember.__table__.delete().where(CompanyMember.id == member_id))

    async def get_member_by_id(self, member_id: int):
        r = await self.db.execute(select(CompanyMember).where(CompanyMember.id == member_id))
        return r.scalar_one_or_none()

    async def list_user_companies(self, user_id: int):
        from src.modules.realestate.models import ContractorCompany
        r = await self.db.execute(
            select(ContractorCompany)
            .join(CompanyMember, ContractorCompany.id == CompanyMember.company_id)
            .where(CompanyMember.user_id == user_id, CompanyMember.is_active == True)
        )
        return r.scalars().all()

    # ── Company Invitations ──────────────────────────────────

    async def create_invitation(self, **data):
        obj = CompanyInvitation(**data)
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def list_invitations(self, company_id: int, status: str = None):
        q = select(CompanyInvitation).where(CompanyInvitation.company_id == company_id)
        if status:
            q = q.where(CompanyInvitation.status == status)
        q = q.order_by(CompanyInvitation.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    async def get_invitation(self, invitation_id: int):
        r = await self.db.execute(select(CompanyInvitation).where(CompanyInvitation.id == invitation_id))
        return r.scalar_one_or_none()

    async def update_invitation_status(self, invitation_id: int, status: str):
        await self.db.execute(
            CompanyInvitation.__table__.update()
            .where(CompanyInvitation.id == invitation_id)
            .values(status=status, updated_at=func.now())
        )

    # ── Listing Pricing / Payments ──────────────────────────────

    async def get_listing_price(self, domain: str, user_role: str = 'company') -> ListingPriceConfig | None:
        r = await self.db.execute(
            select(ListingPriceConfig).where(
                ListingPriceConfig.domain == domain,
                ListingPriceConfig.user_role == user_role,
                ListingPriceConfig.is_active == True,
            )
        )
        return r.scalar_one_or_none()

    async def create_payment(self, obj: ListingPayment):
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_payment_by_listing(self, domain: str, listing_id: int) -> ListingPayment | None:
        r = await self.db.execute(
            select(ListingPayment).where(
                ListingPayment.domain == domain,
                ListingPayment.listing_id == listing_id,
            ).order_by(ListingPayment.created_at.desc())
        )
        return r.scalar_one_or_none()

    async def update_payment_status(self, payment_id: int, status: str):
        values = {"status": status, "updated_at": func.now()}
        if status == "completed":
            values["paid_at"] = func.now()
        await self.db.execute(
            ListingPayment.__table__.update()
            .where(ListingPayment.id == payment_id)
            .values(**values)
        )

    async def list_user_payments(self, user_id: int, domain: str = None):
        q = select(ListingPayment).where(ListingPayment.user_id == user_id)
        if domain:
            q = q.where(ListingPayment.domain == domain)
        q = q.order_by(ListingPayment.created_at.desc())
        r = await self.db.execute(q)
        return r.scalars().all()

    # ── Documents ──────────────────────────────────────────────

    async def create_document(self, obj: ListingDocument):
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_document(self, doc_id: int) -> ListingDocument | None:
        r = await self.db.execute(select(ListingDocument).where(ListingDocument.id == doc_id))
        return r.scalar_one_or_none()

    async def list_documents(self, domain: str, listing_id: int):
        r = await self.db.execute(
            select(ListingDocument)
            .where(
                ListingDocument.domain == domain,
                ListingDocument.listing_id == listing_id,
            )
            .order_by(ListingDocument.created_at.desc())
        )
        return r.scalars().all()

    async def list_user_documents(self, user_id, domain: str):
        r = await self.db.execute(
            select(ListingDocument)
            .where(
                ListingDocument.user_id == user_id,
                ListingDocument.domain == domain,
            )
            .order_by(ListingDocument.created_at.desc())
        )
        return r.scalars().all()

    async def update_document_status(self, doc_id: int, status: str, rejection_reason: str = None, verified_by=None):
        values = {"status": status, "updated_at": func.now()}
        if rejection_reason is not None:
            values["rejection_reason"] = rejection_reason
        if verified_by is not None:
            values["verified_by"] = verified_by
        if status in ("verified", "rejected"):
            values["verified_at"] = func.now()
        await self.db.execute(
            ListingDocument.__table__.update()
            .where(ListingDocument.id == doc_id)
            .values(**values)
        )

    async def create_verification_record(self, doc_id: int, verified_by, action: str, reason: str = None):
        obj = DocumentVerification(
            document_id=doc_id,
            verified_by=verified_by,
            action=action,
            reason=reason,
        )
        self.db.add(obj)
        await self.db.flush()
        return obj

    async def get_listing_documents_by_status(self, listing_id: int, status: str):
        r = await self.db.execute(
            select(ListingDocument)
            .where(
                ListingDocument.listing_id == listing_id,
                ListingDocument.status == status,
            )
        )
        return r.scalars().all()

    async def count_documents_by_status(self, listing_id: int, domain: str, status: str) -> int:
        r = await self.db.execute(
            select(func.count(ListingDocument.id))
            .where(
                ListingDocument.listing_id == listing_id,
                ListingDocument.domain == domain,
                ListingDocument.status == status,
            )
        )
        return r.scalar() or 0

    # ── Company Documents ───────────────────────────────────────

    async def create_company_document(self, company_id: int, user_id, data: dict) -> ListingDocument:
        doc = ListingDocument(
            company_id=company_id,
            user_id=user_id,
            domain=data.get("domain", "realestate"),
            document_type=data.get("document_type"),
            document_number=data.get("document_number"),
            file_path=data.get("file_path"),
            file_name=data.get("file_name"),
            file_size=data.get("file_size"),
            mime_type=data.get("mime_type"),
            description=data.get("description"),
            is_company_doc=True,
            status="pending",
        )
        self.db.add(doc)
        await self.db.flush()
        return doc

    async def list_company_documents(self, company_id: int):
        r = await self.db.execute(
            select(ListingDocument)
            .where(
                ListingDocument.company_id == company_id,
                ListingDocument.is_company_doc == True,
            )
            .order_by(ListingDocument.created_at.desc())
        )
        return r.scalars().all()

    async def count_company_verified_documents(self, company_id: int) -> int:
        r = await self.db.execute(
            select(func.count(ListingDocument.id))
            .where(
                ListingDocument.company_id == company_id,
                ListingDocument.is_company_doc == True,
                ListingDocument.status == "verified",
            )
        )
        return r.scalar() or 0

    # ── Company Verification ─────────────────────────────────────

    async def update_company_verification(self, company_id: int, status: str, note: str = None, verified_by=None):
        values = {"verification_status": status, "updated_at": func.now()}
        if note is not None:
            values["verification_note"] = note
        if verified_by is not None:
            values["verified_by"] = verified_by
        if status in ("verified", "rejected"):
            values["verified_at"] = func.now()
        if status == "verified":
            values["is_verified"] = True
        elif status == "rejected":
            values["is_verified"] = False
            values["is_active"] = False
        await self.db.execute(
            ContractorCompany.__table__.update()
            .where(ContractorCompany.id == company_id)
            .values(**values)
        )

    async def list_companies_by_verification(self, status: str):
        r = await self.db.execute(
            select(ContractorCompany)
            .where(ContractorCompany.verification_status == status)
            .order_by(ContractorCompany.created_at.desc())
        )
        return r.scalars().all()

    async def get_pending_verification_companies(self):
        return await self.list_companies_by_verification("pending")
