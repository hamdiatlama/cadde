from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.expert.models import (
    ExpertCompany, Expert, ExpertPackage, ExpertVehicle, ExpertReport,
    ExpertPanelMeasurement, ExpertInteriorCheck, ExpertExteriorCheck,
    ExpertMechanicalCheck, ExpertElectronicCheck, ExpertTireCheck,
    ExpertTramerRecord, ExpertTestDrive, ExpertDynoTest, ExpertPhoto,
    ExpertEmissionTest, ExpertFluidTest, ExpertHandbrakeTest,
    ExpertFourWheelDriveCheck, ExpertBeltCheck, ExpertChassisCheck,
    ExpertExtraEquipment, ExpertMandatoryEquipment, ExpertAcceptanceCriterion,
)


class ExpertRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, obj):
        self.db.add(obj)

    async def delete(self, obj):
        await self.db.delete(obj)

    async def get_company(self, company_id: int) -> ExpertCompany | None:
        r = await self.db.execute(select(ExpertCompany).where(ExpertCompany.id == company_id))
        return r.scalar_one_or_none()

    async def list_companies(self):
        r = await self.db.execute(select(ExpertCompany).order_by(ExpertCompany.name))
        return r.scalars().all()

    async def get_expert(self, expert_id: int) -> Expert | None:
        r = await self.db.execute(select(Expert).where(Expert.id == expert_id))
        return r.scalar_one_or_none()

    async def list_experts(self, company_id: int | None = None):
        q = select(Expert)
        if company_id:
            q = q.where(Expert.company_id == company_id)
        r = await self.db.execute(q.order_by(Expert.name))
        return r.scalars().all()

    async def get_package(self, package_id: int) -> ExpertPackage | None:
        r = await self.db.execute(select(ExpertPackage).where(ExpertPackage.id == package_id))
        return r.scalar_one_or_none()

    async def list_packages(self):
        r = await self.db.execute(select(ExpertPackage).order_by(ExpertPackage.name))
        return r.scalars().all()

    async def get_vehicle(self, vehicle_id: int) -> ExpertVehicle | None:
        r = await self.db.execute(select(ExpertVehicle).where(ExpertVehicle.id == vehicle_id))
        return r.scalar_one_or_none()

    async def list_vehicles(self, plate: str | None = None, chassis_no: str | None = None):
        q = select(ExpertVehicle)
        if plate:
            q = q.where(ExpertVehicle.plate.ilike(f"%{plate}%"))
        if chassis_no:
            q = q.where(ExpertVehicle.chassis_no.ilike(f"%{chassis_no}%"))
        r = await self.db.execute(q.order_by(ExpertVehicle.id.desc()))
        return r.scalars().all()

    async def get_report(self, report_id: int) -> ExpertReport | None:
        r = await self.db.execute(select(ExpertReport).where(ExpertReport.id == report_id))
        return r.scalar_one_or_none()

    async def list_reports(self, company_id: int | None = None, expert_id: int | None = None, status: str | None = None):
        q = select(ExpertReport)
        if company_id:
            q = q.where(ExpertReport.company_id == company_id)
        if expert_id:
            q = q.where(ExpertReport.expert_id == expert_id)
        if status:
            q = q.where(ExpertReport.status == status)
        r = await self.db.execute(q.order_by(ExpertReport.id.desc()))
        return r.scalars().all()

    async def get_panel_measurements(self, report_id: int):
        r = await self.db.execute(select(ExpertPanelMeasurement).where(ExpertPanelMeasurement.report_id == report_id))
        return r.scalars().all()

    async def get_interior_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertInteriorCheck).where(ExpertInteriorCheck.report_id == report_id))
        return r.scalars().all()

    async def get_exterior_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertExteriorCheck).where(ExpertExteriorCheck.report_id == report_id))
        return r.scalars().all()

    async def get_mechanical_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertMechanicalCheck).where(ExpertMechanicalCheck.report_id == report_id))
        return r.scalars().all()

    async def get_electronic_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertElectronicCheck).where(ExpertElectronicCheck.report_id == report_id))
        return r.scalars().all()

    async def get_tire_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertTireCheck).where(ExpertTireCheck.report_id == report_id))
        return r.scalars().all()

    async def get_tramer_records(self, report_id: int):
        r = await self.db.execute(select(ExpertTramerRecord).where(ExpertTramerRecord.report_id == report_id))
        return r.scalars().all()

    async def get_test_drive(self, report_id: int):
        r = await self.db.execute(select(ExpertTestDrive).where(ExpertTestDrive.report_id == report_id))
        return r.scalars().all()

    async def get_dyno_tests(self, report_id: int):
        r = await self.db.execute(select(ExpertDynoTest).where(ExpertDynoTest.report_id == report_id))
        return r.scalars().all()

    async def get_photos(self, report_id: int):
        r = await self.db.execute(select(ExpertPhoto).where(ExpertPhoto.report_id == report_id))
        return r.scalars().all()

    async def get_emission_tests(self, report_id: int):
        r = await self.db.execute(select(ExpertEmissionTest).where(ExpertEmissionTest.report_id == report_id))
        return r.scalars().all()

    async def get_fluid_tests(self, report_id: int):
        r = await self.db.execute(select(ExpertFluidTest).where(ExpertFluidTest.report_id == report_id))
        return r.scalars().all()

    async def get_handbrake_tests(self, report_id: int):
        r = await self.db.execute(select(ExpertHandbrakeTest).where(ExpertHandbrakeTest.report_id == report_id))
        return r.scalars().all()

    async def get_four_wheel_drive_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertFourWheelDriveCheck).where(ExpertFourWheelDriveCheck.report_id == report_id))
        return r.scalars().all()

    async def get_belt_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertBeltCheck).where(ExpertBeltCheck.report_id == report_id))
        return r.scalars().all()

    async def get_chassis_checks(self, report_id: int):
        r = await self.db.execute(select(ExpertChassisCheck).where(ExpertChassisCheck.report_id == report_id))
        return r.scalars().all()

    async def get_extra_equipment(self, report_id: int):
        r = await self.db.execute(select(ExpertExtraEquipment).where(ExpertExtraEquipment.report_id == report_id))
        return r.scalars().all()

    async def get_mandatory_equipment(self, report_id: int):
        r = await self.db.execute(select(ExpertMandatoryEquipment).where(ExpertMandatoryEquipment.report_id == report_id))
        return r.scalars().all()

    async def get_acceptance_criteria(self, report_id: int):
        r = await self.db.execute(select(ExpertAcceptanceCriterion).where(ExpertAcceptanceCriterion.report_id == report_id))
        return r.scalars().all()

    async def delete_panel_measurements(self, report_id: int):
        await self.db.execute(delete(ExpertPanelMeasurement).where(ExpertPanelMeasurement.report_id == report_id))

    async def delete_interior_checks(self, report_id: int):
        await self.db.execute(delete(ExpertInteriorCheck).where(ExpertInteriorCheck.report_id == report_id))

    async def delete_exterior_checks(self, report_id: int):
        await self.db.execute(delete(ExpertExteriorCheck).where(ExpertExteriorCheck.report_id == report_id))

    async def delete_mechanical_checks(self, report_id: int):
        await self.db.execute(delete(ExpertMechanicalCheck).where(ExpertMechanicalCheck.report_id == report_id))

    async def delete_electronic_checks(self, report_id: int):
        await self.db.execute(delete(ExpertElectronicCheck).where(ExpertElectronicCheck.report_id == report_id))

    async def delete_tire_checks(self, report_id: int):
        await self.db.execute(delete(ExpertTireCheck).where(ExpertTireCheck.report_id == report_id))

    async def delete_tramer_records(self, report_id: int):
        await self.db.execute(delete(ExpertTramerRecord).where(ExpertTramerRecord.report_id == report_id))

    async def delete_test_drive(self, report_id: int):
        await self.db.execute(delete(ExpertTestDrive).where(ExpertTestDrive.report_id == report_id))

    async def delete_dyno_tests(self, report_id: int):
        await self.db.execute(delete(ExpertDynoTest).where(ExpertDynoTest.report_id == report_id))

    async def delete_emission_tests(self, report_id: int):
        await self.db.execute(delete(ExpertEmissionTest).where(ExpertEmissionTest.report_id == report_id))

    async def delete_fluid_tests(self, report_id: int):
        await self.db.execute(delete(ExpertFluidTest).where(ExpertFluidTest.report_id == report_id))

    async def delete_handbrake_tests(self, report_id: int):
        await self.db.execute(delete(ExpertHandbrakeTest).where(ExpertHandbrakeTest.report_id == report_id))

    async def delete_four_wheel_drive_checks(self, report_id: int):
        await self.db.execute(delete(ExpertFourWheelDriveCheck).where(ExpertFourWheelDriveCheck.report_id == report_id))

    async def delete_belt_checks(self, report_id: int):
        await self.db.execute(delete(ExpertBeltCheck).where(ExpertBeltCheck.report_id == report_id))

    async def delete_chassis_checks(self, report_id: int):
        await self.db.execute(delete(ExpertChassisCheck).where(ExpertChassisCheck.report_id == report_id))

    async def delete_extra_equipment(self, report_id: int):
        await self.db.execute(delete(ExpertExtraEquipment).where(ExpertExtraEquipment.report_id == report_id))

    async def delete_mandatory_equipment(self, report_id: int):
        await self.db.execute(delete(ExpertMandatoryEquipment).where(ExpertMandatoryEquipment.report_id == report_id))

    async def delete_acceptance_criteria(self, report_id: int):
        await self.db.execute(delete(ExpertAcceptanceCriterion).where(ExpertAcceptanceCriterion.report_id == report_id))
