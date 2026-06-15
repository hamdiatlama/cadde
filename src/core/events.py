"""NATS event bus (adapter pattern)."""
import asyncio
import json
from typing import Callable, Awaitable, Optional

from src.config import NATS_URL

try:
    import nats
    from nats.aio.msg import Msg
    _nats_available = True
except ImportError:
    nats = None
    _nats_available = False


class EventBus:
    def __init__(self, url: str = NATS_URL):
        self._conn = None
        self._url = url
        self._subscriptions: list = []

    async def connect(self):
        if self._conn is None and nats:
            try:
                self._conn = await asyncio.wait_for(nats.connect(self._url), timeout=2.0)
            except Exception:
                self._conn = None

    async def close(self):
        for sub in self._subscriptions:
            await sub.unsubscribe()
        if self._conn:
            await self._conn.drain()
            self._conn = None

    async def publish(self, subject: str, data: dict):
        if not self._conn:
            return
        await self._conn.publish(subject, json.dumps(data).encode())

    async def subscribe(self, subject: str, callback: Callable[[str, dict], Awaitable[None]]):
        if not self._conn:
            return

        async def handler(msg: Msg):
            data = json.loads(msg.data.decode())
            await callback(msg.subject, data)

        sub = await self._conn.subscribe(subject, cb=handler)
        self._subscriptions.append(sub)

    async def request(self, subject: str, data: dict, timeout: float = 5.0) -> Optional[dict]:
        if not self._conn:
            return None
        try:
            msg = await self._conn.request(subject, json.dumps(data).encode(), timeout=timeout)
            return json.loads(msg.data.decode())
        except nats.errors.TimeoutError:
            return None


event_bus = EventBus()
