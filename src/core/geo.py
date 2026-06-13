"""OSRM routing client (adapter pattern)."""
from typing import Optional
import httpx

from src.config import OSRM_URL


class RoutingClient:
    def __init__(self, base_url: str = OSRM_URL):
        self._base_url = base_url.rstrip("/")

    async def route(
        self, origin_lat: float, origin_lng: float,
        dest_lat: float, dest_lng: float,
        alternatives: bool = False,
    ) -> Optional[dict]:
        url = f"{self._base_url}/route/v1/driving/{origin_lng},{origin_lat};{dest_lng},{dest_lat}"
        params = {"overview": "full", "geometries": "geojson", "alternatives": str(alternatives).lower()}
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(url, params=params, timeout=10)
                if r.status_code == 200:
                    return r.json()
            except Exception:
                return None
        return None

    async def nearest(self, latitude: float, longitude: float) -> Optional[dict]:
        url = f"{self._base_url}/nearest/v1/driving/{longitude},{latitude}"
        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(url, timeout=5)
                if r.status_code == 200:
                    return r.json()
            except Exception:
                return None
        return None


routing = RoutingClient()
