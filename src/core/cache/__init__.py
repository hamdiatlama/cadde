"""Redis cache client wrapper (adapter pattern)."""
import asyncio
import json
from typing import Optional, Any

from src.config import REDIS_URL

try:
    import redis.asyncio as aioredis
    _redis_available = True
except ImportError:
    aioredis = None
    _redis_available = False


class CacheClient:
    def __init__(self, url: str = REDIS_URL):
        self._client = None
        self._url = url

    async def connect(self):
        if self._client is None and aioredis:
            try:
                self._client = await asyncio.wait_for(aioredis.from_url(self._url, decode_responses=True), timeout=2.0)
            except Exception:
                self._client = None

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def get(self, key: str) -> Optional[str]:
        if not self._client:
            return None
        return await self._client.get(key)

    async def set(self, key: str, value: Any, ttl: int = 300):
        if not self._client:
            return
        if not isinstance(value, str):
            value = json.dumps(value)
        await self._client.set(key, value, ex=ttl)

    async def delete(self, key: str):
        if not self._client:
            return
        await self._client.delete(key)

    async def geoadd(self, key: str, longitude: float, latitude: float, member: str):
        if not self._client:
            return
        await self._client.geoadd(key, (longitude, latitude, member))

    async def georadius(
        self, key: str, longitude: float, latitude: float, radius: float, unit: str = "km"
    ) -> list[dict]:
        if not self._client:
            return []
        results = await self._client.geosearch(
            key,
            longitude=longitude,
            latitude=latitude,
            radius=radius,
            unit=unit,
            withdist=True,
            withcoord=True,
        )
        return [
            {"member": r[0], "distance_km": r[1], "latitude": r[2][0], "longitude": r[2][1]}
            for r in results
        ]

    async def geopos(self, key: str, *members: str) -> list[Optional[dict]]:
        if not self._client:
            return []
        positions = await self._client.geopos(key, *members)
        return [
            {"longitude": p[0], "latitude": p[1]} if p else None for p in positions
        ]


cache = CacheClient()
