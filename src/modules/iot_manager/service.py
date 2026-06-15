from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.iot_manager.repository import IotRepository
from src.modules.hotel.repository import HotelRepository


class IotService:
    def __init__(self, db: AsyncSession):
        self.repo = IotRepository(db)
        self.hotel_repo = HotelRepository(db)

    # ─── Device Management ────────────────────────────────────────

    async def register_device(self, hotel_id: int, data: dict) -> dict:
        existing = await self.repo.get_device_by_serial(data.get("serial_number", ""))
        if existing:
            raise ValueError("Device with this serial number already exists")
        device_data = {
            "hotel_id": hotel_id,
            "room_type_id": data.get("room_type_id"),
            "room_number": data.get("room_number"),
            "device_type": data.get("device_type"),
            "device_name": data.get("device_name"),
            "manufacturer": data.get("manufacturer"),
            "model": data.get("model"),
            "serial_number": data.get("serial_number"),
            "ip_address": data.get("ip_address"),
            "mac_address": data.get("mac_address"),
            "firmware_version": data.get("firmware_version"),
            "status": data.get("status", "offline"),
        }
        device = await self.repo.create_device(device_data)
        return self._format_device(device)

    async def update_device(self, device_id: int, data: dict) -> dict:
        device = await self.repo.update_device(device_id, data)
        if not device:
            raise ValueError("Device not found")
        return self._format_device(device)

    async def remove_device(self, device_id: int) -> None:
        ok = await self.repo.delete_device(device_id)
        if not ok:
            raise ValueError("Device not found")

    async def list_devices(self, hotel_id: int, device_type: str = None, status: str = None) -> list[dict]:
        devices = await self.repo.list_devices(hotel_id, device_type, status)
        return [self._format_device(d) for d in devices]

    # ─── Commands ─────────────────────────────────────────────────

    async def send_command(self, device_id: int, command_type: str, value: str, user_id: int = None) -> dict:
        device = await self.repo.get_device(device_id)
        if not device:
            raise ValueError("Device not found")
        command_data = {
            "device_id": device_id,
            "command_type": command_type,
            "command_value": value,
            "executed_by": user_id,
            "status": "delivered",
            "executed_at": datetime.now(timezone.utc),
        }
        cmd = await self.repo.create_command(command_data)
        return self._format_command(cmd)

    # ─── Automation ───────────────────────────────────────────────

    async def execute_automation(self, hotel_id: int, trigger_event: str, context: dict = None) -> list[dict]:
        rules = await self.repo.find_matching_rules(hotel_id, trigger_event)
        results = []
        for rule in rules:
            actions = rule.actions or []
            for action in actions:
                command_type = action.get("command_type")
                command_value = action.get("command_value")
                device_id = action.get("device_id")
                if device_id and command_type:
                    cmd = await self.repo.create_command({
                        "device_id": device_id,
                        "command_type": command_type,
                        "command_value": command_value,
                        "status": "sent",
                        "executed_at": datetime.now(timezone.utc),
                    })
                    results.append(self._format_command(cmd))
        return results

    async def trigger_checkin_automation(self, booking_id: int) -> list[dict]:
        booking = await self.hotel_repo.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        context = {"booking_id": booking_id, "room_id": booking.room_type_id}
        devices = await self.repo.list_devices(booking.hotel_id)
        results = []
        for device in devices:
            if device.device_type == "thermostat" and device.room_type_id == booking.room_type_id:
                cmd = await self.repo.create_command({
                    "device_id": device.id,
                    "command_type": "set_temperature",
                    "command_value": "22",
                    "status": "sent",
                    "executed_at": datetime.now(timezone.utc),
                })
                results.append(self._format_command(cmd))
            elif device.device_type == "smart_lock" and device.room_type_id == booking.room_type_id:
                cmd = await self.repo.create_command({
                    "device_id": device.id,
                    "command_type": "unlock",
                    "command_value": "unlock",
                    "status": "sent",
                    "executed_at": datetime.now(timezone.utc),
                })
                results.append(self._format_command(cmd))
        return results

    async def trigger_checkout_automation(self, booking_id: int) -> list[dict]:
        booking = await self.hotel_repo.get_booking(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        devices = await self.repo.list_devices(booking.hotel_id)
        results = []
        for device in devices:
            if device.device_type == "thermostat" and device.room_type_id == booking.room_type_id:
                cmd = await self.repo.create_command({
                    "device_id": device.id,
                    "command_type": "set_temperature",
                    "command_value": "18",
                    "status": "sent",
                    "executed_at": datetime.now(timezone.utc),
                })
                results.append(self._format_command(cmd))
            elif device.device_type == "smart_lock" and device.room_type_id == booking.room_type_id:
                cmd = await self.repo.create_command({
                    "device_id": device.id,
                    "command_type": "lock",
                    "command_value": "lock",
                    "status": "sent",
                    "executed_at": datetime.now(timezone.utc),
                })
                results.append(self._format_command(cmd))
            elif device.device_type == "light" and device.room_type_id == booking.room_type_id:
                cmd = await self.repo.create_command({
                    "device_id": device.id,
                    "command_type": "light_off",
                    "command_value": "off",
                    "status": "sent",
                    "executed_at": datetime.now(timezone.utc),
                })
                results.append(self._format_command(cmd))
        return results

    # ─── Dashboard ────────────────────────────────────────────────

    async def get_device_dashboard(self, hotel_id: int) -> dict:
        counts = await self.repo.get_device_counts(hotel_id)
        recent_commands = await self.repo.list_recent_commands(hotel_id, limit=10)
        latest_env = await self.repo.get_latest_environment(hotel_id)
        return {
            "device_counts": counts,
            "recent_commands": [self._format_command(c) for c in recent_commands],
            "latest_environment": self._format_environment(latest_env) if latest_env else None,
        }

    # ─── Automation Rules ─────────────────────────────────────────

    async def create_rule(self, hotel_id: int, data: dict) -> dict:
        rule_data = {
            "hotel_id": hotel_id,
            "name": data.get("name"),
            "trigger_event": data.get("trigger_event"),
            "conditions": data.get("conditions"),
            "actions": data.get("actions"),
            "is_active": data.get("is_active", True),
        }
        rule = await self.repo.create_rule(rule_data)
        return self._format_rule(rule)

    async def update_rule(self, rule_id: int, data: dict) -> dict:
        rule = await self.repo.update_rule(rule_id, data)
        if not rule:
            raise ValueError("Rule not found")
        return self._format_rule(rule)

    async def delete_rule(self, rule_id: int) -> None:
        ok = await self.repo.delete_rule(rule_id)
        if not ok:
            raise ValueError("Rule not found")

    async def list_rules(self, hotel_id: int) -> list[dict]:
        rules = await self.repo.list_automation_rules(hotel_id)
        return [self._format_rule(r) for r in rules]

    # ─── Environment ──────────────────────────────────────────────

    async def get_environment(self, hotel_id: int, room_number: str = None, date: str = None) -> list[dict]:
        date_from = date_to = None
        if date:
            try:
                date_from = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
                date_to = date_from.replace(hour=23, minute=59, second=59)
            except ValueError:
                pass
        logs = await self.repo.get_room_environment(hotel_id, room_number, date_from, date_to)
        return [self._format_environment(log) for log in logs]

    # ─── Formatters ───────────────────────────────────────────────

    def _format_device(self, d) -> dict:
        return {
            "id": d.id,
            "hotel_id": d.hotel_id,
            "room_type_id": d.room_type_id,
            "room_number": d.room_number,
            "device_type": d.device_type,
            "device_name": d.device_name,
            "manufacturer": d.manufacturer,
            "model": d.model,
            "serial_number": d.serial_number,
            "ip_address": d.ip_address,
            "mac_address": d.mac_address,
            "firmware_version": d.firmware_version,
            "status": d.status,
            "is_active": d.is_active,
            "last_seen_at": d.last_seen_at.isoformat() if d.last_seen_at else None,
            "created_at": d.created_at.isoformat() if d.created_at else None,
            "updated_at": d.updated_at.isoformat() if d.updated_at else None,
        }

    def _format_command(self, c) -> dict:
        return {
            "id": c.id,
            "device_id": c.device_id,
            "command_type": c.command_type,
            "command_value": c.command_value,
            "executed_by": c.executed_by,
            "status": c.status,
            "executed_at": c.executed_at.isoformat() if c.executed_at else None,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }

    def _format_rule(self, r) -> dict:
        return {
            "id": r.id,
            "hotel_id": r.hotel_id,
            "name": r.name,
            "trigger_event": r.trigger_event,
            "conditions": r.conditions,
            "actions": r.actions,
            "is_active": r.is_active,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }

    def _format_environment(self, e) -> dict:
        return {
            "id": e.id,
            "hotel_id": e.hotel_id,
            "room_number": e.room_number,
            "temperature": e.temperature,
            "humidity": e.humidity,
            "light_level": e.light_level,
            "noise_level": e.noise_level,
            "occupancy_detected": e.occupancy_detected,
            "logged_at": e.logged_at.isoformat() if e.logged_at else None,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
