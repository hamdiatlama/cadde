from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, func, JSON
from src.database import Base


class IotDevice(Base):
    __tablename__ = "iot_devices"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_type_id = Column(Integer, ForeignKey("room_types.id"), nullable=True)
    room_number = Column(String(20))
    device_type = Column(String(50), nullable=False)
    device_name = Column(String(200))
    manufacturer = Column(String(100))
    model = Column(String(100))
    serial_number = Column(String(200), unique=True, nullable=False)
    ip_address = Column(String(50))
    mac_address = Column(String(50))
    firmware_version = Column(String(50))
    status = Column(String(20), default="offline")
    is_active = Column(Boolean, default=True)
    last_seen_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class IotDeviceCommand(Base):
    __tablename__ = "iot_device_commands"
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("iot_devices.id"), nullable=False)
    command_type = Column(String(50), nullable=False)
    command_value = Column(String(200))
    executed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="sent")
    executed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IotAutomationRule(Base):
    __tablename__ = "iot_automation_rules"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    name = Column(String(200), nullable=False)
    trigger_event = Column(String(50), nullable=False)
    conditions = Column(JSON)
    actions = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class RoomEnvironmentLog(Base):
    __tablename__ = "room_environment_logs"
    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hotels.id"), nullable=False)
    room_number = Column(String(20))
    temperature = Column(Float)
    humidity = Column(Float)
    light_level = Column(Float)
    noise_level = Column(Float)
    occupancy_detected = Column(Boolean)
    logged_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
