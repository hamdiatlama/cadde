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
