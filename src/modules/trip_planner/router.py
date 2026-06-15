from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.modules.trip_planner.models import TripSegment, TransportMode, SegmentType
from src.modules.trip_planner.repository import TripPlannerRepository, get_trip_repo
from src.modules.transport.models import TransportStation, TransportSchedule, TransportCompany
from src.modules.hotel.models import Hotel
from src.modules.tourism.models import TourismExperience
from fastapi import APIRouter, Depends, HTTPException
import math

router = APIRouter(prefix=\"/trip-planner\", tags=[\"trip-planner\"])


def haversine(lat1, lng1, lat2, lng2):
    if not all([lat1, lng1, lat2, lng2]): return None
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))


async def suggest_transport_between(repo, origin_lat, origin_lng, dest_lat, dest_lng, city=None):
    \"\"\"Akilli rota onerisi: yakin istasyonlari bul, uygun modlari oner\"\"\"
    suggestions = []
    dist = haversine(origin_lat, origin_lng, dest_lat, dest_lng)
    if dist is None: return suggestions

    if dist < 2:
        suggestions.append({\"mode\": \"walking\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 15), \"cost\": 0})
        suggestions.append({\"mode\": \"taxi\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 5), \"cost\": round(dist * 15)})
    elif dist < 50:
        suggestions.append({\"mode\": \"taxi\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 3), \"cost\": round(dist * 12)})
        suggestions.append({\"mode\": \"bus\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 2.5), \"cost\": round(dist * 1.5)})
        suggestions.append({\"mode\": \"dolmus\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 3), \"cost\": round(dist * 1)})
    elif dist < 500:
        suggestions.append({\"mode\": \"bus\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 1.2), \"cost\": round(dist * 0.8)})
        suggestions.append({\"mode\": \"train\", \"distance_km\": round(dist, 2), \"duration_min\": round(dist * 0.8), \"cost\": round(dist * 0.5)})
        suggestions.append({\"mode\": \"airplane\", \"distance_km\": round(dist, 2), \"duration_min\": max(60, round(dist * 0.15)), \"cost\": round(dist * 1.5)})
    else:
        suggestions.append({\"mode\": \"airplane\", \"distance_km\": round(dist, 2), \"duration_min\": max(90, round(dist * 0.12)), \"cost\": round(dist * 0.8)})

    return suggestions


@router.post(\"/ai/suggest-route\")
async def suggest_route(origin_lat: float = None, origin_lng: float = None,
                         dest_lat: float = None, dest_lng: float = None,
                         origin_city: str = None, dest_city: str = None,
                         repo: TripPlannerRepository = Depends(get_trip_repo)):
    \"\"\"Yapay zeka rota onerisi: iki nokta arasindaki en iyi ulasim modlarini oner\"\"\"
    return await suggest_transport_between(repo, origin_lat, origin_lng, dest_lat, dest_lng)


@router.get(\"/explore/{city}\")
async def explore_city(city: str):
    \"\"\"Bir sehirdeki tum imkanlari kesfet (otel, aktivite, restoran, kiralama)\"\"\"
    import httpx
    results = {\"city\": city, \"hotels\": [], \"experiences\": [], \"stations\": [], \"rentals\": []}
    try:
        async with httpx.AsyncClient() as client:
            h = await client.get(f\"http://127.0.0.1:8000/hotels/search?city={city}\")
            if h.status_code == 200: results[\"hotels\"] = h.json()
            e = await client.get(f\"http://127.0.0.1:8000/tourism/experiences?city={city}\")
            if e.status_code == 200: results[\"experiences\"] = e.json()
            s = await client.get(f\"http://127.0.0.1:8000/transport/stations?city={city}\")
            if s.status_code == 200: results[\"stations\"] = s.json()
            r = await client.get(f\"http://127.0.0.1:8000/rental/branches?city={city}\")
            if r.status_code == 200: results[\"rentals\"] = r.json()
    except: pass
    return results


# ─── CRUD endpoints ──────────────────────────────────────────
@router.post(\"/plans\")
async def create_plan(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_plan(data)


@router.get(\"/plans\")
async def list_plans(user_id: int = None, status: str = None,
                      repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_plans(user_id, status)


@router.get(\"/plans/{plan_id}\")
async def get_plan(plan_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    trip = await repo.get_full_trip(plan_id)
    if not trip: raise HTTPException(404, \"Plan bulunamadi\")
    return trip


@router.put(\"/plans/{plan_id}\")
async def update_plan(plan_id: int, data: dict,
                       repo: TripPlannerRepository = Depends(get_trip_repo)):
    p = await repo.update_plan(plan_id, data)
    if not p: raise HTTPException(404, \"Plan bulunamadi\")
    return p


@router.delete(\"/plans/{plan_id}\")
async def delete_plan(plan_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    if not await repo.delete_plan(plan_id):
        raise HTTPException(404, \"Plan bulunamadi\")
    return {\"ok\": True}


@router.post(\"/segments\")
async def create_segment(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_segment(data)


@router.get(\"/segments/{trip_id}\")
async def list_segments(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_segments(trip_id)


@router.put(\"/segments/{seg_id}\")
async def update_segment(seg_id: int, data: dict,
                          repo: TripPlannerRepository = Depends(get_trip_repo)):
    s = await repo.update_segment(seg_id, data)
    if not s: raise HTTPException(404, \"Segment bulunamadi\")
    return s


@router.delete(\"/segments/{seg_id}\")
async def delete_segment(seg_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    if not await repo.delete_segment(seg_id):
        raise HTTPException(404, \"Segment bulunamadi\")
    return {\"ok\": True}


@router.post(\"/stays\")
async def create_stay(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_stay(data)


@router.get(\"/stays/{trip_id}\")
async def list_stays(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_stays(trip_id)


@router.post(\"/activities\")
async def create_activity(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_activity(data)


@router.get(\"/activities/{trip_id}\")
async def list_activities(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_activities(trip_id)


@router.post(\"/foods\")
async def create_food(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_food(data)


@router.get(\"/foods/{trip_id}\")
async def list_foods(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_foods(trip_id)


@router.post(\"/rentals\")
async def create_rental(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_rental(data)


@router.get(\"/rentals/{trip_id}\")
async def list_rentals(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_rentals(trip_id)


@router.post(\"/deliveries\")
async def create_delivery(data: dict, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.create_delivery(data)


@router.get(\"/deliveries/{trip_id}\")
async def list_deliveries(trip_id: int, repo: TripPlannerRepository = Depends(get_trip_repo)):
    return await repo.list_deliveries(trip_id)
