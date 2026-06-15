from pydantic import BaseModel
from typing import Optional


class CompanyCreate(BaseModel):
    company_name: str
    slug: str
    tax_id: Optional[str] = None
    tax_office: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    api_webhook_url: Optional[str] = None
    api_allowed_ips: Optional[str] = None


class CompanyUpdate(BaseModel):
    company_name: Optional[str] = None
    tax_id: Optional[str] = None
    tax_office: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    api_webhook_url: Optional[str] = None
    api_allowed_ips: Optional[str] = None
    is_active: Optional[bool] = None


class CompanyResponse(BaseModel):
    id: int
    company_name: str
    slug: str
    tax_id: Optional[str] = None
    tax_office: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    api_key: Optional[str] = None
    is_verified: bool
    verification_status: str
    is_active: bool
    rating: float
    review_count: int
    shipment_count: int


class BranchCreate(BaseModel):
    branch_name: str
    branch_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: str
    district: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_main_branch: bool = False
    working_hours: Optional[str] = None
    manager_name: Optional[str] = None
    capacity_daily: Optional[int] = None


class BranchUpdate(BaseModel):
    branch_name: Optional[str] = None
    branch_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_main_branch: Optional[bool] = None
    is_active: Optional[bool] = None
    working_hours: Optional[str] = None
    manager_name: Optional[str] = None
    capacity_daily: Optional[int] = None


class BranchResponse(BaseModel):
    id: int
    company_id: int
    branch_name: str
    branch_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    city: str
    district: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_main_branch: bool
    is_active: bool
    working_hours: Optional[str] = None
    manager_name: Optional[str] = None
    capacity_daily: Optional[int] = None


class CourierCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[str] = None
    branch_id: Optional[int] = None
    tc_kimlik: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    license_no: Optional[str] = None


class CourierUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    branch_id: Optional[int] = None
    tc_kimlik: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    license_no: Optional[str] = None
    is_active: Optional[bool] = None
    is_available: Optional[bool] = None


class CourierResponse(BaseModel):
    id: int
    company_id: int
    branch_id: Optional[int] = None
    full_name: str
    phone: str
    email: Optional[str] = None
    tc_kimlik: Optional[str] = None
    vehicle_type: Optional[str] = None
    vehicle_plate: Optional[str] = None
    is_active: bool
    is_available: bool
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    rating: float
    total_deliveries: int


class ShipmentCreate(BaseModel):
    company_id: int
    branch_id: Optional[int] = None
    courier_id: Optional[int] = None
    sender_name: str
    sender_phone: Optional[str] = None
    sender_email: Optional[str] = None
    sender_city: Optional[str] = None
    sender_district: Optional[str] = None
    sender_address: Optional[str] = None
    sender_latitude: Optional[float] = None
    sender_longitude: Optional[float] = None
    recipient_name: str
    recipient_phone: Optional[str] = None
    recipient_email: Optional[str] = None
    recipient_city: str
    recipient_district: Optional[str] = None
    recipient_address: str
    recipient_latitude: Optional[float] = None
    recipient_longitude: Optional[float] = None
    reference_no: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_dm3: Optional[float] = None
    piece_count: int = 1
    package_type: Optional[str] = None
    description: Optional[str] = None
    is_express: bool = False
    is_international: bool = False
    total_price: Optional[float] = None
    is_paid: bool = False
    payment_method: Optional[str] = None
    source_module: Optional[str] = None
    source_order_id: Optional[int] = None
    estimated_delivery_date: Optional[str] = None


class ShipmentUpdate(BaseModel):
    courier_id: Optional[int] = None
    branch_id: Optional[int] = None
    status: Optional[str] = None
    total_price: Optional[float] = None
    is_paid: Optional[bool] = None
    payment_method: Optional[str] = None
    estimated_delivery_date: Optional[str] = None


class ShipmentResponse(BaseModel):
    id: int
    company_id: int
    branch_id: Optional[int] = None
    courier_id: Optional[int] = None
    sender_name: str
    sender_phone: Optional[str] = None
    sender_city: Optional[str] = None
    sender_district: Optional[str] = None
    sender_address: Optional[str] = None
    recipient_name: str
    recipient_phone: Optional[str] = None
    recipient_city: str
    recipient_district: Optional[str] = None
    recipient_address: str
    tracking_no: str
    reference_no: Optional[str] = None
    weight_kg: Optional[float] = None
    volume_dm3: Optional[float] = None
    piece_count: int
    package_type: Optional[str] = None
    description: Optional[str] = None
    status: str
    is_express: bool
    is_international: bool
    total_price: Optional[float] = None
    currency: str
    is_paid: bool
    payment_method: Optional[str] = None
    source_module: Optional[str] = None
    source_order_id: Optional[int] = None
    delivery_code: Optional[str] = None
    delivery_confirmed_by_recipient: bool = False
    delivery_note: Optional[str] = None
    is_fragile: bool = False
    sensitivity_note: Optional[str] = None
    requires_signature: bool = False
    estimated_delivery_date: Optional[str] = None
    actual_delivery_date: Optional[str] = None


class ShipmentPublicResponse(BaseModel):
    tracking_no: str
    status: str
    sender_name: str
    sender_city: Optional[str] = None
    recipient_name: str
    recipient_city: str
    is_fragile: bool
    sensitivity_note: Optional[str] = None
    estimated_delivery: Optional[str] = None
    steps: list = []


class TrackingCreate(BaseModel):
    status: str
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None


class TrackingResponse(BaseModel):
    id: int
    shipment_id: int
    status: str
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    created_by: Optional[str] = None


class PricingCreate(BaseModel):
    tier_name: str
    min_weight_kg: float = 0
    max_weight_kg: Optional[float] = None
    min_volume_dm3: float = 0
    max_volume_dm3: Optional[float] = None
    zone_type: Optional[str] = None
    base_price: float
    price_per_kg: float = 0
    price_per_dm3: float = 0
    fuel_surcharge_percent: float = 0


class PricingUpdate(BaseModel):
    tier_name: Optional[str] = None
    min_weight_kg: Optional[float] = None
    max_weight_kg: Optional[float] = None
    min_volume_dm3: Optional[float] = None
    max_volume_dm3: Optional[float] = None
    zone_type: Optional[str] = None
    base_price: Optional[float] = None
    price_per_kg: Optional[float] = None
    price_per_dm3: Optional[float] = None
    fuel_surcharge_percent: Optional[float] = None
    is_active: Optional[bool] = None


class PricingResponse(BaseModel):
    id: int
    company_id: int
    tier_name: str
    min_weight_kg: float
    max_weight_kg: Optional[float] = None
    min_volume_dm3: float
    max_volume_dm3: Optional[float] = None
    zone_type: Optional[str] = None
    base_price: float
    price_per_kg: float
    price_per_dm3: float
    fuel_surcharge_percent: float
    is_active: bool


class ServiceAreaCreate(BaseModel):
    branch_id: Optional[int] = None
    city: str
    district: Optional[str] = None
    is_available: bool = True
    delivery_time_hours: Optional[int] = None
    pickup_available: bool = True
    daily_capacity: Optional[int] = None
    notes: Optional[str] = None


class ServiceAreaUpdate(BaseModel):
    is_available: Optional[bool] = None
    delivery_time_hours: Optional[int] = None
    pickup_available: Optional[bool] = None
    daily_capacity: Optional[int] = None
    notes: Optional[str] = None


class ServiceAreaResponse(BaseModel):
    id: int
    company_id: int
    branch_id: Optional[int] = None
    city: str
    district: Optional[str] = None
    is_available: bool
    delivery_time_hours: Optional[int] = None
    pickup_available: bool
    daily_capacity: Optional[int] = None
    notes: Optional[str] = None


class AgreementCreate(BaseModel):
    company_id: int
    is_preferred: bool = False
    contract_start: Optional[str] = None
    contract_end: Optional[str] = None
    negotiated_price_factor: float = 1.0
    notes: Optional[str] = None


class AgreementResponse(BaseModel):
    id: int
    seller_id: int
    company_id: int
    company_name: str
    is_preferred: bool
    contract_start: Optional[str] = None
    contract_end: Optional[str] = None
    negotiated_price_factor: float
    notes: Optional[str] = None
    is_active: bool


class PriceQuoteRequest(BaseModel):
    company_id: int
    weight_kg: float = 0
    volume_dm3: float = 0
    from_city: str
    to_city: str
    is_express: bool = False


class ProductShippingCreate(BaseModel):
    product_id: int
    company_id: int
    estimated_delivery_hours: Optional[int] = None
    max_delivery_days: Optional[int] = None
    available_days: Optional[str] = None
    max_distance_km: Optional[float] = None
    sensitivity_level: str = "normal"
    is_fragile: bool = False
    requires_special_packaging: bool = False
    packaging_instructions: Optional[str] = None
    shipping_price: Optional[float] = None
    free_shipping_min_amount: Optional[float] = None
    is_free_shipping: bool = False


class ProductShippingResponse(BaseModel):
    id: int
    seller_id: int
    product_id: int
    company_id: int
    company_name: str
    estimated_delivery_hours: Optional[int] = None
    max_delivery_days: Optional[int] = None
    available_days: Optional[str] = None
    max_distance_km: Optional[float] = None
    sensitivity_level: str
    is_fragile: bool
    requires_special_packaging: bool
    packaging_instructions: Optional[str] = None
    shipping_price: Optional[float] = None
    free_shipping_min_amount: Optional[float] = None
    is_free_shipping: bool


class DeliverySurveyCreate(BaseModel):
    delivered_on_time: Optional[bool] = None
    package_condition: Optional[str] = None
    is_package_damaged: Optional[bool] = None
    is_package_opened: Optional[bool] = None
    satisfaction_score: Optional[int] = None
    courier_rating: Optional[int] = None
    comment: Optional[str] = None
    photo_url: Optional[str] = None


class DeliverySurveyResponse(BaseModel):
    id: int
    shipment_id: int
    delivered_on_time: Optional[bool] = None
    package_condition: Optional[str] = None
    is_package_damaged: Optional[bool] = None
    is_package_opened: Optional[bool] = None
    satisfaction_score: Optional[int] = None
    courier_rating: Optional[int] = None
    comment: Optional[str] = None


class DeliveryConfirmRequest(BaseModel):
    delivery_code: str
    delivery_note: Optional[str] = None


class ReturnRequestCreate(BaseModel):
    reason: str
    description: Optional[str] = None
    evidence_photos: Optional[str] = None
    evidence_videos: Optional[str] = None


class ReturnRequestResponse(BaseModel):
    id: int
    shipment_id: int
    reason: str
    description: Optional[str] = None
    evidence_photos: Optional[str] = None
    evidence_videos: Optional[str] = None
    status: str
    is_within_window: Optional[bool] = None
    resolution: Optional[str] = None
