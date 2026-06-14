from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db

router = APIRouter(prefix="/expert", tags=["expert"])


@router.post("/companies", status_code=201)
async def create_company(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.create_company(data)
    await db.commit()
    return obj


@router.get("/companies")
async def list_companies(db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_companies()


@router.post("/experts", status_code=201)
async def create_expert(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.create_expert(data)
    await db.commit()
    return obj


@router.get("/experts")
async def list_experts(company_id: int | None = None, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_experts(company_id)


@router.get("/experts/{expert_id}")
async def get_expert(expert_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.get_expert(expert_id)
    if not obj:
        raise HTTPException(404)
    return obj


@router.post("/packages", status_code=201)
async def create_package(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.create_package(data)
    await db.commit()
    return obj


@router.get("/packages")
async def list_packages(db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_packages()


@router.post("/vehicles", status_code=201)
async def create_vehicle(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.create_vehicle(data)
    await db.commit()
    return obj


@router.get("/vehicles")
async def list_vehicles(
    plate: str | None = Query(None),
    chassis_no: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_vehicles(plate, chassis_no)


@router.post("/reports", status_code=201)
async def create_report(data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    report = await svc.create_report(
        company_id=data["company_id"],
        expert_id=data["expert_id"],
        vehicle_data=data["vehicle"],
        checks_data=data.get("checks"),
    )
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/reports")
async def list_reports(
    company_id: int | None = Query(None),
    expert_id: int | None = Query(None),
    status: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_reports(company_id, expert_id, status)


@router.get("/reports/{report_id}")
async def get_report_detail(report_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    try:
        return await svc.get_report_detail(report_id)
    except ValueError:
        raise HTTPException(404)


@router.put("/reports/{report_id}/status")
async def update_report_status(report_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    try:
        obj = await svc.update_report_status(report_id, data["status"])
        await db.commit()
        return obj
    except ValueError:
        raise HTTPException(404)


@router.put("/reports/{report_id}/approve")
async def approve_report(report_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    try:
        obj = await svc.approve_report(report_id, data["approved_by"])
        await db.commit()
        return obj
    except ValueError:
        raise HTTPException(404)


@router.delete("/reports/{report_id}", status_code=204)
async def delete_report(report_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    try:
        await svc.delete_report(report_id)
        await db.commit()
    except ValueError:
        raise HTTPException(404)


@router.get("/reports/{report_id}/checks")
async def get_checks(report_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.get_checks(report_id)


@router.put("/reports/{report_id}/checks/panel")
async def update_panel_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "panel", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/mechanical")
async def update_mechanical_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "mechanical", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/electronic")
async def update_electronic_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "electronic", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/interior")
async def update_interior_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "interior", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/exterior")
async def update_exterior_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "exterior", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/tire")
async def update_tire_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "tire", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/emission")
async def update_emission_tests(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "emission", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/fluid")
async def update_fluid_tests(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "fluid", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/handbrake")
async def update_handbrake_tests(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "handbrake", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/4wd")
async def update_four_wheel_drive_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "4wd", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/belt")
async def update_belt_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "belt", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/chassis")
async def update_chassis_checks(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "chassis", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/extra-equipment")
async def update_extra_equipment(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "extra_equipment", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/mandatory-equipment")
async def update_mandatory_equipment(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "mandatory_equipment", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/dyno")
async def update_dyno_tests(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "dyno", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/test-drive")
async def update_test_drive(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "test_drive", data)
    await db.commit()
    return {"status": "updated"}


@router.put("/reports/{report_id}/checks/tramer")
async def update_tramer_records(report_id: int, data: list[dict], db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    await svc.update_checks(report_id, "tramer", data)
    await db.commit()
    return {"status": "updated"}


@router.post("/reports/{report_id}/photos", status_code=201)
async def add_photo(report_id: int, data: dict, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    obj = await svc.add_photo(report_id, data)
    await db.commit()
    return obj


@router.get("/reports/{report_id}/photos")
async def list_photos(report_id: int, db: AsyncSession = Depends(get_db)):
    from src.modules.expert.service import ExpertService
    svc = ExpertService(db)
    return await svc.list_photos(report_id)
