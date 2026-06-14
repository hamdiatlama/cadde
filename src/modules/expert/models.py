from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class ExpertCompany(Base):
    __tablename__ = "expert_companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    address: Mapped[Optional[str]] = mapped_column(Text)
    tax_no: Mapped[Optional[str]] = mapped_column(String)
    tax_office: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Expert(Base):
    __tablename__ = "experts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_companies.id"), nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String)
    email: Mapped[Optional[str]] = mapped_column(String)
    title: Mapped[Optional[str]] = mapped_column(String)
    license_no: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExpertPackage(Base):
    __tablename__ = "expert_packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    checks_included: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExpertVehicle(Base):
    __tablename__ = "expert_vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    plate: Mapped[Optional[str]] = mapped_column(String)
    chassis_no: Mapped[Optional[str]] = mapped_column(String)
    brand: Mapped[Optional[str]] = mapped_column(String)
    model: Mapped[Optional[str]] = mapped_column(String)
    year: Mapped[Optional[int]] = mapped_column(Integer)
    color: Mapped[Optional[str]] = mapped_column(String)
    fuel_type: Mapped[Optional[str]] = mapped_column(String)
    transmission: Mapped[Optional[str]] = mapped_column(String)
    mileage: Mapped[Optional[int]] = mapped_column(Integer)
    engine_no: Mapped[Optional[str]] = mapped_column(String)
    registration_date: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExpertReport(Base):
    __tablename__ = "expert_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_companies.id"), nullable=False)
    expert_id: Mapped[int] = mapped_column(Integer, ForeignKey("experts.id"), nullable=False)
    vehicle_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_vehicles.id"), nullable=False)
    package_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("expert_packages.id"))
    report_no: Mapped[Optional[str]] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="draft")
    notes: Mapped[Optional[str]] = mapped_column(Text)
    result: Mapped[Optional[str]] = mapped_column(String)
    score: Mapped[Optional[float]] = mapped_column(Float)
    approved_by: Mapped[Optional[int]] = mapped_column(Integer)
    approved_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExpertPanelMeasurement(Base):
    __tablename__ = "expert_panel_measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    panel_name: Mapped[str] = mapped_column(String, nullable=False)
    measurement: Mapped[Optional[float]] = mapped_column(Float)
    status: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertInteriorCheck(Base):
    __tablename__ = "expert_interior_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    item: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertExteriorCheck(Base):
    __tablename__ = "expert_exterior_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    item: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertMechanicalCheck(Base):
    __tablename__ = "expert_mechanical_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    component: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertElectronicCheck(Base):
    __tablename__ = "expert_electronic_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    system: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertTireCheck(Base):
    __tablename__ = "expert_tire_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    position: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[Optional[str]] = mapped_column(String)
    size: Mapped[Optional[str]] = mapped_column(String)
    tread_depth: Mapped[Optional[float]] = mapped_column(Float)
    pressure: Mapped[Optional[float]] = mapped_column(Float)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertTramerRecord(Base):
    __tablename__ = "expert_tramer_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    record_type: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    amount: Mapped[Optional[float]] = mapped_column(Float)
    date: Mapped[Optional[str]] = mapped_column(String)


class ExpertTestDrive(Base):
    __tablename__ = "expert_test_drive"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    test_type: Mapped[str] = mapped_column(String, nullable=False)
    result: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertDynoTest(Base):
    __tablename__ = "expert_dyno_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    test_type: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[Optional[float]] = mapped_column(Float)
    unit: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertPhoto(Base):
    __tablename__ = "expert_photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    photo_type: Mapped[str] = mapped_column(String, nullable=False)
    url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ExpertEmissionTest(Base):
    __tablename__ = "expert_emission_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    test_type: Mapped[str] = mapped_column(String, nullable=False)
    co_value: Mapped[Optional[float]] = mapped_column(Float)
    hc_value: Mapped[Optional[float]] = mapped_column(Float)
    lambda_value: Mapped[Optional[float]] = mapped_column(Float)
    result: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertFluidTest(Base):
    __tablename__ = "expert_fluid_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    fluid_type: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[Optional[str]] = mapped_column(String)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertHandbrakeTest(Base):
    __tablename__ = "expert_handbrake_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    test_position: Mapped[str] = mapped_column(String, nullable=False)
    efficiency: Mapped[Optional[float]] = mapped_column(Float)
    result: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertFourWheelDriveCheck(Base):
    __tablename__ = "expert_four_wheel_drive_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    component: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertBeltCheck(Base):
    __tablename__ = "expert_belt_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    belt_name: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertChassisCheck(Base):
    __tablename__ = "expert_chassis_checks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    section: Mapped[str] = mapped_column(String, nullable=False)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertExtraEquipment(Base):
    __tablename__ = "expert_extra_equipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    equipment: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertMandatoryEquipment(Base):
    __tablename__ = "expert_mandatory_equipment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    equipment: Mapped[str] = mapped_column(String, nullable=False)
    present: Mapped[bool] = mapped_column(Boolean, default=False)
    condition: Mapped[Optional[str]] = mapped_column(String)
    notes: Mapped[Optional[str]] = mapped_column(Text)


class ExpertAcceptanceCriterion(Base):
    __tablename__ = "expert_acceptance_criteria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    report_id: Mapped[int] = mapped_column(Integer, ForeignKey("expert_reports.id"), nullable=False)
    criterion: Mapped[str] = mapped_column(String, nullable=False)
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)
