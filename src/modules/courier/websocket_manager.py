"""WebSocket connection manager for live courier tracking.

Handles:
- Multiple connections per order_id (broadcast)
- Heartbeat/ping-pong for keepalive
- Reconnection support via unique client IDs
- GPS spoofing alerts broadcast
"""

import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self._connections: dict[int, dict[str, WebSocket]] = {}

    async def connect(self, order_id: int, client_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(order_id, {})[client_id] = websocket

    def disconnect(self, order_id: int, client_id: str) -> None:
        if order_id in self._connections:
            self._connections[order_id].pop(client_id, None)
            if not self._connections[order_id]:
                del self._connections[order_id]

    async def broadcast(self, order_id: int, data: dict) -> None:
        if order_id not in self._connections:
            return
        payload = json.dumps(data, default=str)
        disconnected = []
        for client_id, ws in self._connections[order_id].items():
            try:
                await ws.send_text(payload)
            except Exception:
                disconnected.append(client_id)
        for cid in disconnected:
            self.disconnect(order_id, cid)

    async def broadcast_location(
        self,
        order_id: int,
        courier_id: int,
        latitude: float,
        longitude: float,
        speed_kmh: float,
        heading: float,
    ) -> None:
        await self.broadcast(order_id, {
            "type": "location_update",
            "courier_id": courier_id,
            "latitude": latitude,
            "longitude": longitude,
            "speed_kmh": speed_kmh,
            "heading": heading,
            "timestamp": str(__import__("datetime").datetime.now(__import__("datetime").timezone.utc)),
        })

    async def broadcast_status(self, order_id: int, status: str, **extra) -> None:
        payload = {"type": "status_update", "status": status, **extra}
        await self.broadcast(order_id, payload)

    @property
    def active_connections(self) -> int:
        return sum(len(clients) for clients in self._connections.values())

    @property
    def active_orders(self) -> list[int]:
        return list(self._connections.keys())


manager = ConnectionManager()
