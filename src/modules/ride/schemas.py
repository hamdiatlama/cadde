from datetime import datetime
from pydantic import BaseModel, Field


class RideCreateRequest(BaseModel):
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_address: str
    dropoff_latitude: float
    dropoff_longitude: float
    payment_method: str = "card"
    notes: str | None = None


class DriverLocationUpdate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    speed_kmh: float = 0
    heading: float = Field(0, ge=0, le=360)
    accuracy_m: float = 0
    source: str = "gps"


class SafetyConfirmRequest(BaseModel):
    plate_confirmed: bool = False
    photo_confirmed: bool = False


class EmergencyContactRequest(BaseModel):
    phone: str


class IncidentReportRequest(BaseModel):
    incident_type: str
    description: str


class RideRatingRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = None
    categories: str | None = None


class DriverRegisterRequest(BaseModel):
    license_plate: str
    vehicle_model: str
    vehicle_color: str
    vehicle_type: str = "sedan"


class RideResponse(BaseModel):
    id: int
    customer_id: int
    driver_id: int | None = None
    status: str
    pickup_address: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_address: str
    dropoff_latitude: float
    dropoff_longitude: float
    estimated_fare: float
    actual_fare: float | None = None
    surge_multiplier: float
    payment_method: str
    payment_status: str
    optimal_distance_km: float | None = None
    actual_distance_km: float | None = None
    route_deviation_km: float | None = None
    eta_at_booking: int | None = None
    actual_wait_seconds: int | None = None
    notes: str | None = None
    accepted_at: datetime | None = None
    arrived_at: datetime | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    cancelled_at: datetime | None = None
    cancel_reason: str | None = None
    cancelled_by: str | None = None
    created_at: datetime | None = None
    driver_plate: str | None = None
    driver_vehicle: str | None = None
    driver_name: str | None = None

    class Config:
        from_attributes = True


class DriverResponse(BaseModel):
    id: int
    user_id: int
    is_available: bool
    current_latitude: float | None = None
    current_longitude: float | None = None
    current_speed_kmh: float | None = None
    total_rides: int
    cancelled_rides: int
    rating: float
    total_ratings: int
    license_plate: str | None = None
    vehicle_model: str | None = None
    vehicle_color: str | None = None
    is_active: bool

    class Config:
        from_attributes = True


class RideSafetyResponse(BaseModel):
    ride_id: int
    driver_plate_confirmed: bool = False
    driver_photo_confirmed: bool = False
    emergency_contact_phone: str | None = None
    share_link: str | None = None
    incident_reported: bool = False
    incident_type: str | None = None
    incident_description: str | None = None

    class Config:
        from_attributes = True


class SpoofingStatus(BaseModel):
    driver_id: int
    spoofing_score: float
    consecutive_anomalies: int
    is_suspicious: bool
    last_anomaly_at: str | None = None
