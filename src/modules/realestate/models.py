import uuid
from sqlalchemy import Column, Integer, BigInteger, SmallInteger, String, Boolean, DateTime, Text, Float, Numeric, ForeignKey, UniqueConstraint, PrimaryKeyConstraint, Index, JSON, Date, func
from sqlalchemy.dialects.postgresql import UUID
from src.database import Base


class PropertyCategory(Base):
    __tablename__ = "property_categories"
    id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    sort_order = Column(SmallInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyType(Base):
    __tablename__ = "property_types"
    id = Column(SmallInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(200))
    sort_order = Column(SmallInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ContractorCompany(Base):
    __tablename__ = "contractor_companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    tax_no = Column(String(20))
    tax_office = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    website = Column(String(200))
    logo_url = Column(Text)
    description = Column(Text)
    rating = Column(Numeric(2, 1), default=0)
    review_count = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    verification_status = Column(String(20), default='pending')
    verification_note = Column(Text)
    verified_at = Column(DateTime(timezone=True))
    certificate_no = Column(String(100))
    certificate_expiry = Column(Date)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def location_str(self):
        if self.latitude and self.longitude:
            return f"{self.latitude},{self.longitude}"
        return None


class ContractorReview(Base):
    __tablename__ = "contractor_reviews"
    __table_args__ = (
        UniqueConstraint("company_id", "user_id", name="uq_company_user_review"),
    )
    id = Column(BigInteger, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("contractor_companies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyListing(Base):
    __tablename__ = "property_listings"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(SmallInteger, ForeignKey("property_categories.id"))
    type_id = Column(SmallInteger, ForeignKey("property_types.id"))
    contractor_id = Column(Integer, ForeignKey("contractor_companies.id"))
    title = Column(String(300), nullable=False)
    description = Column(Text)
    price = Column(Numeric(14, 2), nullable=False)
    currency = Column(String(3), default="TRY")
    is_for_sale = Column(Boolean, default=True)
    is_for_rent = Column(Boolean, default=False)
    rent_deposit = Column(Numeric(10, 2))
    dues = Column(Numeric(10, 2))
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    country = Column(String(100), default="Türkiye")
    city = Column(String(100))
    district = Column(String(100))
    neighborhood = Column(String(100))
    address = Column(Text)
    map_address = Column(Text)
    building_name = Column(String(200))
    block = Column(String(50))
    floor = Column(String(20))
    door_number = Column(String(20))
    construction_year = Column(Integer)
    building_age = Column(Integer)
    floor_count = Column(Integer)
    total_apartments = Column(Integer)
    contractor_name_history = Column(Text)
    land_area = Column(Numeric(10, 2))
    building_area = Column(Numeric(10, 2))
    zoning_status = Column(String(50))
    land_use_type = Column(String(50))
    density_value = Column(String(50))
    parcel_no = Column(String(50))
    island_no = Column(String(50))
    room_count = Column(String(20))
    bathroom_count = Column(Integer)
    net_area = Column(Numeric(8, 2))
    gross_area = Column(Numeric(8, 2))
    heating_type = Column(String(50))
    furnishing = Column(String(50))
    facade = Column(String(50))
    balcony_count = Column(Integer)
    status = Column(String(20), default="active")
    view_count = Column(Integer, default=0)
    is_highlighted = Column(Boolean, default=False)
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def location_str(self):
        if self.latitude and self.longitude:
            return f"{self.latitude},{self.longitude}"
        return None


class PropertyPhoto(Base):
    __tablename__ = "property_photos"
    id = Column(BigInteger, primary_key=True, index=True)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    file_path = Column(Text, nullable=False)
    category = Column(String(50), default="genel")
    description = Column(String(500))
    is_cover = Column(Boolean, default=False)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyFeature(Base):
    __tablename__ = "property_features"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    icon = Column(String(200))
    category = Column(String(50))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyListingFeature(Base):
    __tablename__ = "property_listing_features"
    __table_args__ = (
        PrimaryKeyConstraint("listing_id", "feature_id", name="pk_listing_feature"),
    )
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    feature_id = Column(Integer, ForeignKey("property_features.id"), nullable=False)
    value = Column(String(500))


class AuthorizationRequest(Base):
    __tablename__ = "authorization_requests"
    id = Column(BigInteger, primary_key=True, index=True)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("contractor_companies.id"), nullable=False)
    auth_type = Column(String(20), default="sell")
    commission_rate = Column(Numeric(5, 2))
    commission_fixed = Column(Numeric(10, 2))
    valid_from = Column(DateTime(timezone=True))
    valid_until = Column(DateTime(timezone=True))
    status = Column(String(20), default="pending")
    owner_note = Column(Text)
    company_note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyAppraisalRequest(Base):
    __tablename__ = "property_appraisal_requests"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"))
    company_id = Column(Integer, ForeignKey("contractor_companies.id"))
    expert_id = Column(Integer, ForeignKey("users.id"))
    city = Column(String(100))
    district = Column(String(100))
    neighborhood = Column(String(100))
    address = Column(Text)
    latitude = Column(Numeric(10, 7))
    longitude = Column(Numeric(10, 7))
    property_type_id = Column(SmallInteger, ForeignKey("property_types.id"))
    land_area = Column(Numeric(10, 2))
    building_area = Column(Numeric(10, 2))
    room_count = Column(String(20))
    construction_year = Column(Integer)
    status = Column(String(20), default="pending")
    notes = Column(Text)
    report_data = Column(JSON)
    report_file_url = Column(Text)
    requested_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def location_str(self):
        if self.latitude and self.longitude:
            return f"{self.latitude},{self.longitude}"
        return None


class FavoriteListing(Base):
    __tablename__ = "favorite_listings"
    __table_args__ = (
        PrimaryKeyConstraint("user_id", "listing_id", name="pk_favorite"),
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)


class PropertyInquiry(Base):
    __tablename__ = "property_inquiries"
    id = Column(BigInteger, primary_key=True, index=True)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    from_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    parent_id = Column(BigInteger, ForeignKey("property_inquiries.id"))
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class PropertyLandContent(Base):
    __tablename__ = "property_land_contents"
    id = Column(BigInteger, primary_key=True, index=True)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    content_type = Column(String(50), nullable=False)
    content_name = Column(String(200), nullable=False)
    quantity = Column(Numeric(10, 2))
    unit = Column(String(20))
    description = Column(Text)
    sort_order = Column(SmallInteger, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyMember(Base):
    __tablename__ = "company_members"
    __table_args__ = (
        UniqueConstraint("company_id", "user_id", name="uq_company_member"),
    )
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("contractor_companies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="agent")
    title = Column(String)
    is_active = Column(Boolean, default=True)
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class CompanyInvitation(Base):
    __tablename__ = "company_invitations"
    id = Column(BigInteger, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("contractor_companies.id"), nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invitee_id = Column(Integer, ForeignKey("users.id"))
    invitee_email = Column(String(200))
    role = Column(String, default="agent")
    status = Column(String, default="pending")
    message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class ListingPriceConfig(Base):
    __tablename__ = "listing_price_config"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(100), unique=True, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="TRY")
    user_role = Column(String(20), nullable=False, default='company')
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class ListingPayment(Base):
    __tablename__ = "listing_payments"
    id = Column(BigInteger, primary_key=True, index=True)
    domain = Column(String(100), nullable=False)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="TRY")
    payment_method = Column(String(50))
    payment_ref = Column(String(200))
    status = Column(String(20), default="pending")
    paid_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class ListingDocument(Base):
    __tablename__ = "listing_documents"
    id = Column(BigInteger, primary_key=True, index=True)
    domain = Column(String(100), nullable=False)
    listing_id = Column(BigInteger, ForeignKey("property_listings.id"), nullable=False)
    company_id = Column(Integer, ForeignKey("contractor_companies.id"))
    is_company_doc = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    document_type = Column(String(50), nullable=False)
    document_number = Column(String(100))
    file_path = Column(Text)
    file_name = Column(String(255))
    file_size = Column(BigInteger)
    mime_type = Column(String(50))
    description = Column(Text)
    status = Column(String(20), default="pending")
    rejection_reason = Column(Text)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    verified_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now())


class DocumentVerification(Base):
    __tablename__ = "document_verifications"
    id = Column(BigInteger, primary_key=True, index=True)
    document_id = Column(BigInteger, ForeignKey("listing_documents.id"), nullable=False)
    verified_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    action = Column(String(20), nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
