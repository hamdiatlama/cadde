import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from src.database import Base


class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    slug: Mapped[str] = sa.Column(sa.String, nullable=False, unique=True)
    parent_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_categories.id"))
    sort_order: Mapped[int] = sa.Column(sa.SmallInteger, default=0)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleSegment(Base):
    __tablename__ = "vehicle_segments"
    code: Mapped[str] = sa.Column(sa.String(10), primary_key=True)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    description: Mapped[str | None] = sa.Column(sa.Text)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class BodyType(Base):
    __tablename__ = "body_types"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    slug: Mapped[str] = sa.Column(sa.String, nullable=False, unique=True)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleBrand(Base):
    __tablename__ = "vehicle_brands"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    slug: Mapped[str] = sa.Column(sa.String, nullable=False, unique=True)
    country: Mapped[str | None] = sa.Column(sa.String)
    logo_url: Mapped[str | None] = sa.Column(sa.String)
    is_active: Mapped[bool] = sa.Column(sa.Boolean, default=True)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleModel(Base):
    __tablename__ = "vehicle_models"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    brand_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_brands.id"), nullable=False)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    segment_code: Mapped[str | None] = sa.Column(sa.String(10), sa.ForeignKey("vehicle_segments.code"))
    production_start: Mapped[int | None] = sa.Column(sa.SmallInteger)
    production_end: Mapped[int | None] = sa.Column(sa.SmallInteger)
    is_active: Mapped[bool] = sa.Column(sa.Boolean, default=True)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleModelBodyType(Base):
    __tablename__ = "vehicle_model_body_types"
    model_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_models.id"), primary_key=True)
    body_type_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("body_types.id"), primary_key=True)


class VehicleCategoryModel(Base):
    __tablename__ = "vehicle_category_models"
    category_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_categories.id"), primary_key=True)
    model_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_models.id"), primary_key=True)


class VehicleModelYear(Base):
    __tablename__ = "vehicle_model_years"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    model_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_models.id"), nullable=False)
    year: Mapped[int] = sa.Column(sa.SmallInteger, nullable=False)
    trim_name: Mapped[str | None] = sa.Column(sa.String)
    engine_volume: Mapped[sa.Numeric | None] = sa.Column(sa.Numeric(4, 1))
    horsepower: Mapped[int | None] = sa.Column(sa.SmallInteger)
    fuel_type: Mapped[str | None] = sa.Column(sa.String)
    transmission: Mapped[str | None] = sa.Column(sa.String)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class FeatureGroup(Base):
    __tablename__ = "feature_groups"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    slug: Mapped[str] = sa.Column(sa.String, nullable=False, unique=True)
    sort_order: Mapped[int] = sa.Column(sa.SmallInteger, default=0)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class Feature(Base):
    __tablename__ = "features"
    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    group_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("feature_groups.id"), nullable=False)
    name: Mapped[str] = sa.Column(sa.String, nullable=False)
    slug: Mapped[str] = sa.Column(sa.String, nullable=False, unique=True)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleModelFeature(Base):
    __tablename__ = "vehicle_model_features"
    model_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_models.id"), primary_key=True)
    feature_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("features.id"), primary_key=True)
    is_standard: Mapped[bool] = sa.Column(sa.Boolean, default=False)


# --- Vehicle Listing System (Oto Galeri) ---

class VehicleListing(Base):
    __tablename__ = "vehicle_listings"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    seller_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("sellers.id"))
    user_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    title: Mapped[str] = sa.Column(sa.String(255), nullable=False)
    description: Mapped[str | None] = sa.Column(sa.Text)
    brand_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_brands.id"))
    model_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_models.id"))
    year: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    body_type_id: Mapped[int | None] = sa.Column(sa.Integer, sa.ForeignKey("body_types.id"))
    segment_code: Mapped[str | None] = sa.Column(sa.String(10))
    mileage: Mapped[int | None] = sa.Column(sa.Integer)
    mileage_unit: Mapped[str | None] = sa.Column(sa.String(10), default="km")
    fuel_type: Mapped[str | None] = sa.Column(sa.String(30))
    transmission: Mapped[str | None] = sa.Column(sa.String(30))
    engine_displacement_cc: Mapped[int | None] = sa.Column(sa.Integer)
    engine_power_hp: Mapped[int | None] = sa.Column(sa.Integer)
    color: Mapped[str | None] = sa.Column(sa.String(50))
    interior_color: Mapped[str | None] = sa.Column(sa.String(50))
    condition: Mapped[str | None] = sa.Column(sa.String(20), default="ikinci_el")
    warranty_months: Mapped[int | None] = sa.Column(sa.Integer)
    city: Mapped[str | None] = sa.Column(sa.String(100))
    district: Mapped[str | None] = sa.Column(sa.String(100))
    latitude: Mapped[float | None] = sa.Column(sa.Float)
    longitude: Mapped[float | None] = sa.Column(sa.Float)
    price: Mapped[float] = sa.Column(sa.Float, nullable=False)
    currency: Mapped[str | None] = sa.Column(sa.String(10), default="TRY")
    is_negotiable: Mapped[bool] = sa.Column(sa.Boolean, default=True)
    status: Mapped[str | None] = sa.Column(sa.String(20), default="draft")
    is_featured: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    is_active: Mapped[bool] = sa.Column(sa.Boolean, default=True)
    view_count: Mapped[int] = sa.Column(sa.Integer, default=0)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleListingPhoto(Base):
    __tablename__ = "vehicle_listing_photos"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    listing_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_listings.id", ondelete="CASCADE"))
    url: Mapped[str] = sa.Column(sa.String(500), nullable=False)
    sort_order: Mapped[int] = sa.Column(sa.Integer, default=0)
    is_cover: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleGalleryCompany(Base):
    __tablename__ = "vehicle_gallery_companies"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    company_name: Mapped[str] = sa.Column(sa.String(255), nullable=False)
    slug: Mapped[str] = sa.Column(sa.String(255), unique=True, nullable=False)
    tax_id: Mapped[str | None] = sa.Column(sa.String(50))
    phone: Mapped[str | None] = sa.Column(sa.String(20))
    email: Mapped[str | None] = sa.Column(sa.String(255))
    city: Mapped[str | None] = sa.Column(sa.String(100))
    district: Mapped[str | None] = sa.Column(sa.String(100))
    address: Mapped[str | None] = sa.Column(sa.Text)
    latitude: Mapped[float | None] = sa.Column(sa.Float)
    longitude: Mapped[float | None] = sa.Column(sa.Float)
    description: Mapped[str | None] = sa.Column(sa.Text)
    logo_url: Mapped[str | None] = sa.Column(sa.String(500))
    cover_url: Mapped[str | None] = sa.Column(sa.String(500))
    is_verified: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    verification_status: Mapped[str | None] = sa.Column(sa.String(20), default="pending")
    certificate_no: Mapped[str | None] = sa.Column(sa.String(100))
    certificate_expiry: Mapped[sa.Date | None] = sa.Column(sa.Date)
    rating: Mapped[float] = sa.Column(sa.Float, default=0)
    review_count: Mapped[int] = sa.Column(sa.Integer, default=0)
    is_active: Mapped[bool] = sa.Column(sa.Boolean, default=True)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleFavoriteListing(Base):
    __tablename__ = "vehicle_favorite_listings"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    listing_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_listings.id", ondelete="CASCADE"))
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())


class VehicleInquiry(Base):
    __tablename__ = "vehicle_inquiries"

    id: Mapped[int] = sa.Column(sa.Integer, primary_key=True, index=True)
    listing_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("vehicle_listings.id", ondelete="CASCADE"))
    sender_id: Mapped[int] = sa.Column(sa.Integer, sa.ForeignKey("users.id"))
    message: Mapped[str] = sa.Column(sa.Text, nullable=False)
    is_read: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    created_at: Mapped[sa.DateTime] = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
