from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.modules.vehicle.repository import VehicleRepo
from src.modules.vehicle.models import (
    VehicleModel, VehicleModelBodyType, VehicleModelFeature,
    BodyType, Feature, VehicleModelYear,
)


class VehicleService:
    def __init__(self, repo: VehicleRepo):
        self.repo = repo

    async def search_models(self, brand_id: int = None, segment: str = None, query: str = None) -> list:
        stmt = select(VehicleModel)
        if brand_id:
            stmt = stmt.where(VehicleModel.brand_id == brand_id)
        if segment:
            stmt = stmt.where(VehicleModel.segment_code == segment)
        if query:
            stmt = stmt.where(VehicleModel.name.ilike(f"%{query}%"))
        r = await self.repo.session.execute(stmt.order_by(VehicleModel.name))
        return r.scalars().all()

    async def get_model_detail(self, model_id: int) -> dict:
        model = await self.repo.get_model(model_id)
        if not model:
            return None

        body_r = await self.repo.session.execute(
            select(BodyType).join(VehicleModelBodyType).where(VehicleModelBodyType.model_id == model_id)
        )
        body_types = body_r.scalars().all()

        feature_r = await self.repo.session.execute(
            select(Feature, VehicleModelFeature.is_standard)
            .join(VehicleModelFeature)
            .where(VehicleModelFeature.model_id == model_id)
        )
        features = [{"id": f.id, "name": f.name, "slug": f.slug, "is_standard": s} for f, s in feature_r.all()]

        year_r = await self.repo.session.execute(
            select(VehicleModelYear).where(VehicleModelYear.model_id == model_id).order_by(VehicleModelYear.year)
        )
        years = year_r.scalars().all()

        return {
            "model": model,
            "body_types": body_types,
            "features": features,
            "years": years,
        }
