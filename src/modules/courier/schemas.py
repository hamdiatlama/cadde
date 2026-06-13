from datetime import datetime
from pydantic import BaseModel, Field


class LocationUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed_kmh: float = 0
    heading: float = Field(0, ge=0, le=360)
    accuracy_m: float = 0
    source: str = "gps"


class AssignRequest(BaseModel):
    order_id: int


class CourierResponse(BaseModel):
    id: int
    user_id: int
    is_available: bool
    status: str
    current_latitude: float | None = None
    current_longitude: float | None = None
    current_speed_kmh: float | None = None
    total_deliveries: int
    rating: float
    vehicle_type: str | None = None
    vehicle_plate: str | None = None
    service_zone: str | None = None

    class Config:
        from_attributes = True


class CourierNearbyResponse(BaseModel):
    id: int
    user_id: int
    latitude: float
    longitude: float
    distance_km: float
    vehicle_type: str | None = None
    rating: float
    total_deliveries: int


class LocationHistoryResponse(BaseModel):
    latitude: float
    longitude: float
    speed_kmh: float
    heading: float
    timestamp: datetime | None = None


class TrackResponse(BaseModel):
    status: str
    courier_id: int | None = None
    current_location: dict | None = None
    last_update: str | None = None
    history: list[LocationHistoryResponse] = []


class AssignResponse(BaseModel):
    message: str
    courier_id: int
    order_id: int
    courier_latitude: float | None = None
    courier_longitude: float | None = None
    eta_seconds: int | None = None


class DeliverResponse(BaseModel):
    message: str
    order_id: int


class ShiftStartResponse(BaseModel):
    status: str
    shift_id: int | None = None


class ShiftEndResponse(BaseModel):
    status: str
    total_earned: float = 0
    orders_completed: int = 0
    total_distance_km: float = 0


class EarningsResponse(BaseModel):
    total_delivery_fees: float = 0
    total_tips: float = 0
    total_bonuses: float = 0
    total_earned: float = 0
    total_deliveries: int = 0
    pending_payout: float = 0


class SpoofingStatus(BaseModel):
    courier_id: int
    spoofing_score: float
    consecutive_anomalies: int
    is_suspicious: bool
    last_anomaly_at: str | None = None
