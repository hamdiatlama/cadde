from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.vehicle.models import (
    VehicleCategory, VehicleSegment, BodyType, VehicleBrand,
    VehicleModel, VehicleModelBodyType, VehicleCategoryModel,
    VehicleModelYear, FeatureGroup, Feature, VehicleModelFeature,
)


class VehicleRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_brand(self, data: dict) -> VehicleBrand:
        obj = VehicleBrand(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_brands(self) -> list[VehicleBrand]:
        r = await self.session.execute(select(VehicleBrand).order_by(VehicleBrand.name))
        return r.scalars().all()

    async def get_brand(self, brand_id: int) -> VehicleBrand | None:
        r = await self.session.execute(select(VehicleBrand).where(VehicleBrand.id == brand_id))
        return r.scalar_one_or_none()

    async def create_model(self, data: dict) -> VehicleModel:
        obj = VehicleModel(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def list_models(self, brand_id: int = None) -> list[VehicleModel]:
        q = select(VehicleModel)
        if brand_id:
            q = q.where(VehicleModel.brand_id == brand_id)
        r = await self.session.execute(q.order_by(VehicleModel.name))
        return r.scalars().all()

    async def get_model(self, model_id: int) -> VehicleModel | None:
        r = await self.session.execute(select(VehicleModel).where(VehicleModel.id == model_id))
        return r.scalar_one_or_none()

    async def list_categories(self) -> list[VehicleCategory]:
        r = await self.session.execute(select(VehicleCategory).order_by(VehicleCategory.sort_order))
        return r.scalars().all()

    async def list_segments(self) -> list[VehicleSegment]:
        r = await self.session.execute(select(VehicleSegment).order_by(VehicleSegment.name))
        return r.scalars().all()

    async def list_body_types(self) -> list[BodyType]:
        r = await self.session.execute(select(BodyType).order_by(BodyType.name))
        return r.scalars().all()

    async def list_model_years(self, model_id: int) -> list[VehicleModelYear]:
        r = await self.session.execute(
            select(VehicleModelYear).where(VehicleModelYear.model_id == model_id).order_by(VehicleModelYear.year)
        )
        return r.scalars().all()

    async def list_feature_groups(self) -> list[FeatureGroup]:
        r = await self.session.execute(select(FeatureGroup).order_by(FeatureGroup.sort_order))
        return r.scalars().all()

    async def list_features(self, group_id: int = None) -> list[Feature]:
        q = select(Feature)
        if group_id:
            q = q.where(Feature.group_id == group_id)
        r = await self.session.execute(q.order_by(Feature.name))
        return r.scalars().all()
