from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db

router = APIRouter(prefix="/vehicles", tags=["vehicles"])


@router.post("/brands", status_code=201)
async def create_brand(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    try:
        brand = await repo.create_brand(data)
        await db.commit()
        return brand
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, str(e))


@router.get("/brands")
async def list_brands(db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_brands()


@router.get("/brands/{brand_id}")
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    brand = await repo.get_brand(brand_id)
    if not brand:
        raise HTTPException(404, "Brand not found")
    return brand


@router.post("/brands/{brand_id}/models", status_code=201)
async def create_model(brand_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    try:
        data["brand_id"] = brand_id
        model = await repo.create_model(data)
        await db.commit()
        return model
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, str(e))


@router.get("/models")
async def list_models(brand_id: int = None, segment: str = None, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.service import VehicleService
    from src.modules.vehicle.repository import VehicleRepo
    svc = VehicleService(VehicleRepo(db))
    try:
        return await svc.search_models(brand_id=brand_id, segment=segment)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.get("/models/{model_id}")
async def get_model_detail(model_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.service import VehicleService
    from src.modules.vehicle.repository import VehicleRepo
    svc = VehicleService(VehicleRepo(db))
    result = await svc.get_model_detail(model_id)
    if not result:
        raise HTTPException(404, "Model not found")
    return result


@router.get("/categories")
async def list_categories(db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_categories()


@router.get("/segments")
async def list_segments(db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_segments()


@router.get("/body-types")
async def list_body_types(db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_body_types()


@router.get("/models/{model_id}/years")
async def list_model_years(model_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_model_years(model_id)


@router.get("/feature-groups")
async def list_feature_groups(db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_feature_groups()


@router.get("/features")
async def list_features(group_id: int = None, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.repository import VehicleRepo
    repo = VehicleRepo(db)
    return await repo.list_features(group_id)


@router.post("/feature-groups", status_code=201)
async def create_feature_group(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.models import FeatureGroup
    obj = FeatureGroup(**data)
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, str(e))


@router.post("/features", status_code=201)
async def create_feature(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.vehicle.models import Feature
    obj = Feature(**data)
    db.add(obj)
    try:
        await db.commit()
        await db.refresh(obj)
        return obj
    except Exception as e:
        await db.rollback()
        raise HTTPException(400, str(e))
