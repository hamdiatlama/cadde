from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, JSON, func, ForeignKey
from src.database import Base


class EnergyMeter(Base):
    __tablename__ = "energy_meters"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    meter_type = Column(String(20), nullable=False)
    meter_name = Column(String(200), nullable=False)
    location = Column(String(200))
    unit = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EnergyReading(Base):
    __tablename__ = "energy_readings"
    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(Integer, ForeignKey("energy_meters.id"), nullable=False)
    reading_value = Column(Float, nullable=False)
    unit = Column(String(20), nullable=False)
    reading_date = Column(DateTime(timezone=True), nullable=False)
    source = Column(String(20), default="manual")
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EnergyConsumptionReport(Base):
    __tablename__ = "energy_consumption_reports"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    report_date = Column(Date, nullable=False)
    total_electricity_kwh = Column(Float, default=0)
    total_water_m3 = Column(Float, default=0)
    total_gas_m3 = Column(Float, default=0)
    total_cost = Column(Float, default=0)
    electricity_cost = Column(Float, default=0)
    water_cost = Column(Float, default=0)
    gas_cost = Column(Float, default=0)
    occupancy_rate = Column(Float, default=0)
    cost_per_occupied_room = Column(Float, default=0)
    report_data = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class EnergySavingRule(Base):
    __tablename__ = "energy_saving_rules"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    rule_name = Column(String(200), nullable=False)
    trigger_type = Column(String(50), nullable=False)
    conditions = Column(JSON)
    actions = Column(JSON)
    estimated_savings_percent = Column(Float, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SustainabilityCertification(Base):
    __tablename__ = "sustainability_certifications"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    certification_name = Column(String(200), nullable=False)
    issuing_body = Column(String(200))
    certificate_number = Column(String(100))
    awarded_date = Column(Date)
    expiry_date = Column(Date)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
