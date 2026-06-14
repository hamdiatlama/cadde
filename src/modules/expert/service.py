from src.modules.expert.repository import ExpertRepo
from src.modules.expert.models import (
    ExpertCompany, Expert, ExpertPackage, ExpertVehicle, ExpertReport,
    ExpertPanelMeasurement, ExpertInteriorCheck, ExpertExteriorCheck,
    ExpertMechanicalCheck, ExpertElectronicCheck, ExpertTireCheck,
    ExpertTramerRecord, ExpertTestDrive, ExpertDynoTest, ExpertPhoto,
    ExpertEmissionTest, ExpertFluidTest, ExpertHandbrakeTest,
    ExpertFourWheelDriveCheck, ExpertBeltCheck, ExpertChassisCheck,
    ExpertExtraEquipment, ExpertMandatoryEquipment, ExpertAcceptanceCriterion,
)


class ExpertService:
    def __init__(self, db):
        self.repo = ExpertRepo(db)

    async def create_company(self, data: dict) -> ExpertCompany:
        obj = ExpertCompany(**data)
        await self.repo.add(obj)
        return obj

    async def list_companies(self):
        return await self.repo.list_companies()

    async def create_expert(self, data: dict) -> Expert:
        obj = Expert(**data)
        await self.repo.add(obj)
        return obj

    async def list_experts(self, company_id: int | None = None):
        return await self.repo.list_experts(company_id)

    async def get_expert(self, expert_id: int) -> Expert | None:
        return await self.repo.get_expert(expert_id)

    async def create_package(self, data: dict) -> ExpertPackage:
        obj = ExpertPackage(**data)
        await self.repo.add(obj)
        return obj

    async def list_packages(self):
        return await self.repo.list_packages()

    async def create_vehicle(self, data: dict) -> ExpertVehicle:
        obj = ExpertVehicle(**data)
        await self.repo.add(obj)
        return obj

    async def list_vehicles(self, plate: str | None = None, chassis_no: str | None = None):
        return await self.repo.list_vehicles(plate, chassis_no)

    async def create_report(self, company_id: int, expert_id: int, vehicle_data: dict, checks_data: dict | None = None) -> ExpertReport:
        vehicle = ExpertVehicle(**vehicle_data)
        await self.repo.add(vehicle)
        report = ExpertReport(company_id=company_id, expert_id=expert_id, vehicle_id=vehicle.id)
        await self.repo.add(report)
        if checks_data:
            await self._create_checks(report.id, checks_data)
        return report

    async def _create_checks(self, report_id: int, checks: dict):
        for key in ("panel_measurements",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertPanelMeasurement(report_id=report_id, **item))
        for key in ("interior_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertInteriorCheck(report_id=report_id, **item))
        for key in ("exterior_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertExteriorCheck(report_id=report_id, **item))
        for key in ("mechanical_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertMechanicalCheck(report_id=report_id, **item))
        for key in ("electronic_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertElectronicCheck(report_id=report_id, **item))
        for key in ("tire_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertTireCheck(report_id=report_id, **item))
        for key in ("tramer_records",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertTramerRecord(report_id=report_id, **item))
        for key in ("test_drive",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertTestDrive(report_id=report_id, **item))
        for key in ("dyno_tests",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertDynoTest(report_id=report_id, **item))
        for key in ("emission_tests",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertEmissionTest(report_id=report_id, **item))
        for key in ("fluid_tests",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertFluidTest(report_id=report_id, **item))
        for key in ("handbrake_tests",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertHandbrakeTest(report_id=report_id, **item))
        for key in ("four_wheel_drive_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertFourWheelDriveCheck(report_id=report_id, **item))
        for key in ("belt_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertBeltCheck(report_id=report_id, **item))
        for key in ("chassis_checks",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertChassisCheck(report_id=report_id, **item))
        for key in ("extra_equipment",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertExtraEquipment(report_id=report_id, **item))
        for key in ("mandatory_equipment",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertMandatoryEquipment(report_id=report_id, **item))
        for key in ("acceptance_criteria",):
            for item in checks.get(key, []):
                await self.repo.add(ExpertAcceptanceCriterion(report_id=report_id, **item))

    async def get_report_detail(self, report_id: int) -> dict:
        report = await self.repo.get_report(report_id)
        if not report:
            raise ValueError("Report not found")
        return {
            "report": report,
            "vehicle": await self.repo.get_vehicle(report.vehicle_id),
            "company": await self.repo.get_company(report.company_id),
            "expert": await self.repo.get_expert(report.expert_id),
            "panel_measurements": await self.repo.get_panel_measurements(report_id),
            "interior_checks": await self.repo.get_interior_checks(report_id),
            "exterior_checks": await self.repo.get_exterior_checks(report_id),
            "mechanical_checks": await self.repo.get_mechanical_checks(report_id),
            "electronic_checks": await self.repo.get_electronic_checks(report_id),
            "tire_checks": await self.repo.get_tire_checks(report_id),
            "tramer_records": await self.repo.get_tramer_records(report_id),
            "test_drive": await self.repo.get_test_drive(report_id),
            "dyno_tests": await self.repo.get_dyno_tests(report_id),
            "emission_tests": await self.repo.get_emission_tests(report_id),
            "fluid_tests": await self.repo.get_fluid_tests(report_id),
            "handbrake_tests": await self.repo.get_handbrake_tests(report_id),
            "four_wheel_drive_checks": await self.repo.get_four_wheel_drive_checks(report_id),
            "belt_checks": await self.repo.get_belt_checks(report_id),
            "chassis_checks": await self.repo.get_chassis_checks(report_id),
            "extra_equipment": await self.repo.get_extra_equipment(report_id),
            "mandatory_equipment": await self.repo.get_mandatory_equipment(report_id),
            "acceptance_criteria": await self.repo.get_acceptance_criteria(report_id),
            "photos": await self.repo.get_photos(report_id),
        }

    async def list_reports(self, company_id: int | None = None, expert_id: int | None = None, status: str | None = None):
        return await self.repo.list_reports(company_id, expert_id, status)

    async def search_reports(self, plate: str | None = None, chassis_no: str | None = None, status: str | None = None):
        vehicles = await self.repo.list_vehicles(plate, chassis_no)
        vehicle_ids = [v.id for v in vehicles]
        if not vehicle_ids:
            return []
        reports = await self.repo.list_reports(status=status)
        return [r for r in reports if r.vehicle_id in vehicle_ids]

    async def update_report_status(self, report_id: int, status: str):
        report = await self.repo.get_report(report_id)
        if not report:
            raise ValueError("Report not found")
        report.status = status
        return report

    async def approve_report(self, report_id: int, approved_by: int):
        report = await self.repo.get_report(report_id)
        if not report:
            raise ValueError("Report not found")
        report.status = "approved"
        report.approved_by = approved_by
        from datetime import datetime, timezone
        report.approved_at = datetime.now(timezone.utc)
        return report

    async def delete_report(self, report_id: int):
        report = await self.repo.get_report(report_id)
        if not report:
            raise ValueError("Report not found")
        await self.repo.delete_panel_measurements(report_id)
        await self.repo.delete_interior_checks(report_id)
        await self.repo.delete_exterior_checks(report_id)
        await self.repo.delete_mechanical_checks(report_id)
        await self.repo.delete_electronic_checks(report_id)
        await self.repo.delete_tire_checks(report_id)
        await self.repo.delete_tramer_records(report_id)
        await self.repo.delete_test_drive(report_id)
        await self.repo.delete_dyno_tests(report_id)
        await self.repo.delete_emission_tests(report_id)
        await self.repo.delete_fluid_tests(report_id)
        await self.repo.delete_handbrake_tests(report_id)
        await self.repo.delete_four_wheel_drive_checks(report_id)
        await self.repo.delete_belt_checks(report_id)
        await self.repo.delete_chassis_checks(report_id)
        await self.repo.delete_extra_equipment(report_id)
        await self.repo.delete_mandatory_equipment(report_id)
        await self.repo.delete_acceptance_criteria(report_id)
        await self.repo.delete(report)

    async def get_checks(self, report_id: int) -> dict:
        return {
            "panel_measurements": await self.repo.get_panel_measurements(report_id),
            "interior_checks": await self.repo.get_interior_checks(report_id),
            "exterior_checks": await self.repo.get_exterior_checks(report_id),
            "mechanical_checks": await self.repo.get_mechanical_checks(report_id),
            "electronic_checks": await self.repo.get_electronic_checks(report_id),
            "tire_checks": await self.repo.get_tire_checks(report_id),
            "tramer_records": await self.repo.get_tramer_records(report_id),
            "test_drive": await self.repo.get_test_drive(report_id),
            "dyno_tests": await self.repo.get_dyno_tests(report_id),
            "emission_tests": await self.repo.get_emission_tests(report_id),
            "fluid_tests": await self.repo.get_fluid_tests(report_id),
            "handbrake_tests": await self.repo.get_handbrake_tests(report_id),
            "four_wheel_drive_checks": await self.repo.get_four_wheel_drive_checks(report_id),
            "belt_checks": await self.repo.get_belt_checks(report_id),
            "chassis_checks": await self.repo.get_chassis_checks(report_id),
            "extra_equipment": await self.repo.get_extra_equipment(report_id),
            "mandatory_equipment": await self.repo.get_mandatory_equipment(report_id),
            "acceptance_criteria": await self.repo.get_acceptance_criteria(report_id),
        }

    async def update_checks(self, report_id: int, check_type: str, items: list[dict]):
        delete_map = {
            "panel": self.repo.delete_panel_measurements,
            "interior": self.repo.delete_interior_checks,
            "exterior": self.repo.delete_exterior_checks,
            "mechanical": self.repo.delete_mechanical_checks,
            "electronic": self.repo.delete_electronic_checks,
            "tire": self.repo.delete_tire_checks,
            "tramer": self.repo.delete_tramer_records,
            "test_drive": self.repo.delete_test_drive,
            "dyno": self.repo.delete_dyno_tests,
            "emission": self.repo.delete_emission_tests,
            "fluid": self.repo.delete_fluid_tests,
            "handbrake": self.repo.delete_handbrake_tests,
            "4wd": self.repo.delete_four_wheel_drive_checks,
            "belt": self.repo.delete_belt_checks,
            "chassis": self.repo.delete_chassis_checks,
            "extra_equipment": self.repo.delete_extra_equipment,
            "mandatory_equipment": self.repo.delete_mandatory_equipment,
        }
        model_map = {
            "panel": ExpertPanelMeasurement,
            "interior": ExpertInteriorCheck,
            "exterior": ExpertExteriorCheck,
            "mechanical": ExpertMechanicalCheck,
            "electronic": ExpertElectronicCheck,
            "tire": ExpertTireCheck,
            "tramer": ExpertTramerRecord,
            "test_drive": ExpertTestDrive,
            "dyno": ExpertDynoTest,
            "emission": ExpertEmissionTest,
            "fluid": ExpertFluidTest,
            "handbrake": ExpertHandbrakeTest,
            "4wd": ExpertFourWheelDriveCheck,
            "belt": ExpertBeltCheck,
            "chassis": ExpertChassisCheck,
            "extra_equipment": ExpertExtraEquipment,
            "mandatory_equipment": ExpertMandatoryEquipment,
        }
        delete_fn = delete_map.get(check_type)
        model_cls = model_map.get(check_type)
        if not delete_fn or not model_cls:
            raise ValueError(f"Unknown check type: {check_type}")
        await delete_fn(report_id)
        for item in items:
            await self.repo.add(model_cls(report_id=report_id, **item))

    async def add_photo(self, report_id: int, data: dict) -> ExpertPhoto:
        obj = ExpertPhoto(report_id=report_id, **data)
        await self.repo.add(obj)
        return obj

    async def list_photos(self, report_id: int):
        return await self.repo.get_photos(report_id)
