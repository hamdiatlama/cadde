from math import radians, sin, cos, sqrt, atan2, degrees
from datetime import datetime, timezone


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def bounding_box(lat: float, lon: float, radius_km: float) -> dict:
    lat_offset = radius_km / 111.0
    lon_offset = radius_km / (111.0 * abs(cos(radians(lat))) if abs(lat) < 89.9 else 111.0)
    return {
        "min_lat": lat - lat_offset,
        "max_lat": lat + lat_offset,
        "min_lon": lon - lon_offset,
        "max_lon": lon + lon_offset,
    }


def estimate_duration_seconds(dist_km: float, avg_speed_kmh: float = 30) -> int:
    if dist_km <= 0:
        return 0
    return int((dist_km / avg_speed_kmh) * 3600)


def calculate_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    dlon = radians(lon2 - lon1)
    x = sin(dlon) * cos(radians(lat2))
    y = cos(radians(lat1)) * sin(radians(lat2)) - sin(radians(lat1)) * cos(radians(lat2)) * cos(dlon)
    bearing = degrees(atan2(x, y))
    return (bearing + 360) % 360


EARTH_RADIUS_KM = 6371


def detect_gps_anomaly(
    lat: float, lon: float,
    prev_lat: float | None, prev_lon: float | None,
    prev_time: datetime | None,
    speed_kmh: float,
    accuracy_m: float,
    max_plausible_speed_kmh: float = 180,
    max_plausible_accuracy_m: float = 100,
) -> dict:
    anomalies = []

    if accuracy_m > max_plausible_accuracy_m and accuracy_m > 0:
        anomalies.append(f"low_accuracy:{accuracy_m}m")

    if speed_kmh > max_plausible_speed_kmh:
        anomalies.append(f"excessive_speed:{speed_kmh}kmh")

    if prev_lat is not None and prev_lon is not None and prev_time is not None:
        now = datetime.now(timezone.utc)
        dt = (now - prev_time).total_seconds()
        if dt > 0:
            implied_speed = (haversine_km(prev_lat, prev_lon, lat, lon) / dt) * 3600
            if implied_speed > max_plausible_speed_kmh:
                anomalies.append(f"teleportation:{implied_speed:.1f}kmh")
            if speed_kmh > 0 and implied_speed > 0:
                ratio = abs(implied_speed - speed_kmh) / max(speed_kmh, 1)
                if ratio > 3:
                    anomalies.append(f"speed_mismatch:reported={speed_kmh}kmh,implied={implied_speed:.1f}kmh")

    score = min(len(anomalies) * 0.25, 1.0)
    is_anomaly = len(anomalies) > 0

    return {
        "is_anomaly": is_anomaly,
        "score": score,
        "anomalies": anomalies,
    }
