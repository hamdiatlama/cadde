from datetime import datetime
from pydantic import BaseModel


class RestaurantCreate(BaseModel):
    name: str
    cuisine_type: str | None = None
    cuisine_subtypes: str | None = None
    phone: str | None = None
    description: str | None = None
    logo_url: str | None = None
    opening_time: str = "09:00"
    closing_time: str = "22:00"
    closed_days: str | None = None
    min_order_amount: float = 0
    delivery_fee: float = 19.90
    free_delivery_min_amount: float = 100
    max_delivery_radius_km: float = 5.0
    preparation_time_min: int = 20
    has_thermal_bags: bool = False
    commission_rate: float = 0.15


class RestaurantUpdate(BaseModel):
    name: str | None = None
    cuisine_type: str | None = None
    cuisine_subtypes: str | None = None
    phone: str | None = None
    description: str | None = None
    logo_url: str | None = None
    is_open: bool | None = None
    accepts_orders: bool | None = None
    opening_time: str | None = None
    closing_time: str | None = None
    closed_days: str | None = None
    min_order_amount: float | None = None
    delivery_fee: float | None = None
    free_delivery_min_amount: float | None = None
    max_delivery_radius_km: float | None = None
    preparation_time_min: int | None = None


class MenuItemCreate(BaseModel):
    name: str
    category: str | None = None
    subcategory: str | None = None
    price: float
    compare_price: float | None = None
    description: str | None = None
    calories_kcal: int | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None
    fiber_g: float | None = None
    serving_size: str | None = None
    is_vegetarian: bool = False
    is_vegan: bool = False
    is_gluten_free: bool = False
    is_halal: bool = False
    is_spicy: bool = False
    dietary_tags: str | None = None
    allergens: str | None = None
    image_url: str | None = None
    preparation_time_min: int = 10


class MenuItemUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    subcategory: str | None = None
    price: float | None = None
    compare_price: float | None = None
    description: str | None = None
    calories_kcal: int | None = None
    protein_g: float | None = None
    carbs_g: float | None = None
    fat_g: float | None = None
    fiber_g: float | None = None
    serving_size: str | None = None
    is_vegetarian: bool | None = None
    is_vegan: bool | None = None
    is_gluten_free: bool | None = None
    is_halal: bool | None = None
    is_spicy: bool | None = None
    dietary_tags: str | None = None
    allergens: str | None = None
    image_url: str | None = None
    is_available: bool | None = None
    preparation_time_min: int | None = None


class ModifierCreate(BaseModel):
    group_name: str
    name: str
    price_modifier: float = 0
    max_select: int = 1
    is_default: bool = False


class BranchCreate(BaseModel):
    name: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    phone: str | None = None
    opening_time: str | None = None
    closing_time: str | None = None


class ZoneCreate(BaseModel):
    name: str
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    delivery_fee: float = 0
    min_order: float = 0
    estimated_delivery_min: int = 30


class ChatSend(BaseModel):
    receiver_role: str
    message: str


class TemperatureLog(BaseModel):
    order_id: int
    temperature_celsius: float
    check_type: str = "pickup"
    photo_url: str | None = None
    notes: str | None = None


class HygieneReportCreate(BaseModel):
    order_id: int
    issue_type: str
    description: str | None = None
    photo_urls: str | None = None


class DriverReportCreate(BaseModel):
    order_id: int
    courier_id: int
    rating: int = 5
    issue_type: str | None = None
    description: str | None = None
    is_anonymous: bool = False


class BatchPreventCreate(BaseModel):
    max_batch_size: int = 1
