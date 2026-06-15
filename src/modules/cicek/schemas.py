from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class FloristProfileBase(BaseModel):
    shop_name: str
    slug: str
    description: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    preparation_time_min: int = 30
    delivery_radius_km: float = 5.0
    min_order_amount: float = 0
    delivery_fee: float = 0
    free_delivery_min_amount: Optional[float] = None
    working_hours_json: Optional[str] = None


class FloristProfileCreate(FloristProfileBase):
    pass


class FloristProfileUpdate(BaseModel):
    shop_name: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_open: Optional[bool] = None
    preparation_time_min: Optional[int] = None
    delivery_radius_km: Optional[float] = None
    min_order_amount: Optional[float] = None
    delivery_fee: Optional[float] = None
    free_delivery_min_amount: Optional[float] = None
    working_hours_json: Optional[str] = None


class FloristProfileResponse(FloristProfileBase):
    id: int
    is_active: bool
    is_open: bool
    verification_status: str
    rating: float
    review_count: int
    total_score: int
    created_at: datetime

    class Config:
        from_attributes = True


class FloristPublicResponse(BaseModel):
    id: int
    shop_name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    is_open: bool
    preparation_time_min: int
    delivery_radius_km: float
    min_order_amount: float
    delivery_fee: float
    free_delivery_min_amount: Optional[float] = None
    verification_status: str
    rating: float
    review_count: int
    total_score: int


class FlowerProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    occasion: Optional[str] = None
    price: float
    compare_price: Optional[float] = None
    stock: int = 0
    unit: str = "adet"
    size: Optional[str] = None
    color: Optional[str] = None
    colors_json: Optional[str] = None
    flowers_json: Optional[str] = None
    meaning: Optional[str] = None
    season: Optional[str] = None
    lifespan_days: Optional[int] = None
    care_level: Optional[str] = None
    has_vase: bool = False
    vase_type: Optional[str] = None
    is_express_eligible: bool = False
    is_customizable: bool = False
    images_json: Optional[str] = None
    origin: Optional[str] = None
    fragrance: Optional[str] = None


class FlowerProductCreate(FlowerProductBase):
    pass


class FlowerProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    occasion: Optional[str] = None
    price: Optional[float] = None
    compare_price: Optional[float] = None
    stock: Optional[int] = None
    size: Optional[str] = None
    color: Optional[str] = None
    colors_json: Optional[str] = None
    flowers_json: Optional[str] = None
    meaning: Optional[str] = None
    is_active: Optional[bool] = None
    has_vase: Optional[bool] = None
    vase_type: Optional[str] = None
    images_json: Optional[str] = None
    is_express_eligible: Optional[bool] = None
    is_customizable: Optional[bool] = None


class FlowerProductResponse(FlowerProductBase):
    id: int
    seller_type: str
    seller_id: int
    is_active: bool
    rating: float
    review_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class SpecialDayReminderCreate(BaseModel):
    name: str
    reminder_date: date
    occasion_type: Optional[str] = None
    is_yearly: bool = True


class SpecialDayReminderResponse(BaseModel):
    id: int
    name: str
    reminder_date: date
    occasion_type: Optional[str] = None
    is_yearly: bool
    is_active: bool

    class Config:
        from_attributes = True


class CustomOrderDesignCreate(BaseModel):
    florist_id: int
    theme: Optional[str] = None
    size: Optional[str] = None
    flowers_json: Optional[str] = None
    extras_json: Optional[str] = None
    vase_type: Optional[str] = None
    card_message: str
    card_design: Optional[str] = None
    card_type: str = "dijital"


class CustomOrderDesignResponse(BaseModel):
    id: int
    theme: Optional[str] = None
    size: Optional[str] = None
    total_price: Optional[float] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class FloristStatusResponse(BaseModel):
    durum: str
    calisma_saatleri: Optional[str] = None
    tatil_gunleri: Optional[str] = None
    en_erken_teslimat: Optional[str] = None


class FloristImageCreate(BaseModel):
    category: str
    file_path: str
    resolution: Optional[str] = None


class FloristDocumentCreate(BaseModel):
    document_type: str
    file_path: str
    valid_until: Optional[date] = None


class FlowerRatingCreate(BaseModel):
    order_id: int
    rated_id: int
    rated_type: str
    score: float = 5.0
    criteria_json: Optional[str] = None
    comment: Optional[str] = None


class FreshnessRecordCreate(BaseModel):
    order_id: int
    stage: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    photo_url: Optional[str] = None
