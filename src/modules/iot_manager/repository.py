from datetime import datetime, timezone
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.iot_manager.models import (
    IotDevice, IotDeviceCommand, IotAutomationRule, RoomEnvironmentLog,
)


class IotRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ─── Devices ──────────────────────────────────────────────────

    async def create_device(self, data: dict) -> IotDevice:
        d = IotDevice(**data)
        self.db.add(d)
        return d

    async def get_device(self, device_id: int) -> IotDevice | None:
        r = await self.db.execute(select(IotDevice).where(IotDevice.id == device_id))
        return r.scalar_one_or_none()

    async def get_device_by_serial(self, serial: str) -> IotDevice | None:
        r = await self.db.execute(
            select(IotDevice).where(IotDevice.serial_number == serial)
        )
        return r.scalar_one_or_none()

    async def list_devices(self, hotel_id: int, device_type: str = None, status: str = None):
        query = select(IotDevice).where(IotDevice.hotel_id == hotel_id)
        if device_type:
            query = query.where(IotDevice.device_type == device_type)
        if status:
            query = query.where(IotDevice.status == status)
        query = query.order_by(IotDevice.created_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def update_device(self, device_id: int, data: dict) -> IotDevice | None:
        d = await self.get_device(device_id)
        if not d:
            return None
        for field, val in data.items():
            setattr(d, field, val)
        self.db.add(d)
        return d

    async def delete_device(self, device_id: int) -> bool:
        d = await self.get_device(device_id)
        if not d:
            return False
        await self.db.delete(d)
        return True

    async def get_device_counts(self, hotel_id: int) -> dict:
        total_q = select(func.count(IotDevice.id)).where(IotDevice.hotel_id == hotel_id)
        online_q = select(func.count(IotDevice.id)).where(
            IotDevice.hotel_id == hotel_id, IotDevice.status == "online"
        )
        offline_q = select(func.count(IotDevice.id)).where(
            IotDevice.hotel_id == hotel_id, IotDevice.status == "offline"
        )
        error_q = select(func.count(IotDevice.id)).where(
            IotDevice.hotel_id == hotel_id, IotDevice.status == "error"
        )
        total = (await self.db.execute(total_q)).scalar() or 0
        online = (await self.db.execute(online_q)).scalar() or 0
        offline = (await self.db.execute(offline_q)).scalar() or 0
        error = (await self.db.execute(error_q)).scalar() or 0
        return {"total": total, "online": online, "offline": offline, "error": error}

    # ─── Commands ─────────────────────────────────────────────────

    async def create_command(self, data: dict) -> IotDeviceCommand:
        c = IotDeviceCommand(**data)
        self.db.add(c)
        return c

    async def list_commands(self, device_id: int, limit: int = 50):
        r = await self.db.execute(
            select(IotDeviceCommand)
            .where(IotDeviceCommand.device_id == device_id)
            .order_by(IotDeviceCommand.created_at.desc())
            .limit(limit)
        )
        return list(r.scalars().all())

    async def list_recent_commands(self, hotel_id: int, limit: int = 20):
        r = await self.db.execute(
            select(IotDeviceCommand)
            .join(IotDevice, IotDeviceCommand.device_id == IotDevice.id)
            .where(IotDevice.hotel_id == hotel_id)
            .order_by(IotDeviceCommand.created_at.desc())
            .limit(limit)
        )
        return list(r.scalars().all())

    # ─── Automation Rules ─────────────────────────────────────────

    async def create_rule(self, data: dict) -> IotAutomationRule:
        rule = IotAutomationRule(**data)
        self.db.add(rule)
        return rule

    async def get_rule(self, rule_id: int) -> IotAutomationRule | None:
        r = await self.db.execute(
            select(IotAutomationRule).where(IotAutomationRule.id == rule_id)
        )
        return r.scalar_one_or_none()

    async def list_automation_rules(self, hotel_id: int):
        r = await self.db.execute(
            select(IotAutomationRule)
            .where(IotAutomationRule.hotel_id == hotel_id)
            .order_by(IotAutomationRule.created_at.desc())
        )
        return list(r.scalars().all())

    async def update_rule(self, rule_id: int, data: dict) -> IotAutomationRule | None:
        rule = await self.get_rule(rule_id)
        if not rule:
            return None
        for field, val in data.items():
            setattr(rule, field, val)
        self.db.add(rule)
        return rule

    async def delete_rule(self, rule_id: int) -> bool:
        rule = await self.get_rule(rule_id)
        if not rule:
            return False
        await self.db.delete(rule)
        return True

    async def find_matching_rules(self, hotel_id: int, trigger_event: str):
        r = await self.db.execute(
            select(IotAutomationRule).where(
                IotAutomationRule.hotel_id == hotel_id,
                IotAutomationRule.trigger_event == trigger_event,
                IotAutomationRule.is_active == True,
            )
        )
        return list(r.scalars().all())

    # ─── Environment Logs ─────────────────────────────────────────

    async def create_environment_log(self, data: dict) -> RoomEnvironmentLog:
        log = RoomEnvironmentLog(**data)
        self.db.add(log)
        return log

    async def get_room_environment(self, hotel_id: int, room_number: str = None, date_from: datetime = None, date_to: datetime = None):
        query = select(RoomEnvironmentLog).where(RoomEnvironmentLog.hotel_id == hotel_id)
        if room_number:
            query = query.where(RoomEnvironmentLog.room_number == room_number)
        if date_from:
            query = query.where(RoomEnvironmentLog.logged_at >= date_from)
        if date_to:
            query = query.where(RoomEnvironmentLog.logged_at <= date_to)
        query = query.order_by(RoomEnvironmentLog.logged_at.desc())
        r = await self.db.execute(query)
        return list(r.scalars().all())

    async def get_latest_environment(self, hotel_id: int, room_number: str = None):
        query = select(RoomEnvironmentLog).where(RoomEnvironmentLog.hotel_id == hotel_id)
        if room_number:
            query = query.where(RoomEnvironmentLog.room_number == room_number)
        query = query.order_by(RoomEnvironmentLog.logged_at.desc()).limit(1)
        r = await self.db.execute(query)
        return r.scalar_one_or_none()
