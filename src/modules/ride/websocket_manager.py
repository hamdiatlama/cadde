import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[int, dict[str, WebSocket]] = {}

    async def connect(self, ride_id: int, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(ride_id, {})[client_id] = websocket

    def disconnect(self, ride_id: int, client_id: str) -> None:
        if ride_id in self._connections:
            self._connections[ride_id].pop(client_id, None)
            if not self._connections[ride_id]:
                del self._connections[ride_id]

    async def broadcast(self, ride_id: int, data: dict) -> None:
        if ride_id not in self._connections:
            return
        payload = json.dumps(data, default=str)
        disconnected = []
        for client_id, ws in self._connections[ride_id].items():
            try:
                await ws.send_text(payload)
            except Exception:
                disconnected.append(client_id)
        for cid in disconnected:
            self.disconnect(ride_id, cid)

    async def broadcast_location(
        self,
        ride_id: int,
        driver_id: int,
        latitude: float,
        longitude: float,
        speed_kmh: float,
        heading: float,
    ) -> None:
        await self.broadcast(ride_id, {
            "type": "driver_location_update",
            "driver_id": driver_id,
            "latitude": latitude,
            "longitude": longitude,
            "speed_kmh": speed_kmh,
            "heading": heading,
            "timestamp": str(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
        })

    async def broadcast_status(self, ride_id: int, status: str, **extra) -> None:
        payload = {"type": "status_update", "status": status, **extra}
        await self.broadcast(ride_id, payload)

    @property
    def active_connections(self) -> int:
        return sum(len(clients) for clients in self._connections.values())

    @property
    def active_rides(self) -> list[int]:
        return list(self._connections.keys())


manager = ConnectionManager()
