from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: float
    compare_price: Optional[float] = None
    image_url: Optional[str] = None
    stock: Optional[int] = 0
    tags: Optional[str] = None
    color: Optional[str] = None
    occasion: Optional[str] = None
    care_instructions: Optional[str] = None
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None
    is_express_eligible: Optional[bool] = False
    original_product_id: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    price: Optional[float] = None
    compare_price: Optional[float] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    tags: Optional[str] = None
    color: Optional[str] = None
    occasion: Optional[str] = None
    care_instructions: Optional[str] = None
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None
    is_express_eligible: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    seller_id: int
    name: str
    slug: Optional[str]
    description: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    price: float
    compare_price: Optional[float]
    original_price: Optional[float]
    discount_start_at: Optional[datetime]
    is_discounted: bool
    original_product_id: Optional[int]
    image_url: Optional[str]
    stock: int
    is_active: bool
    tags: Optional[str]
    color: Optional[str]
    occasion: Optional[str]
    care_instructions: Optional[str]
    season_start_month: Optional[int]
    season_end_month: Optional[int]
    is_express_eligible: bool
    rating: float
    review_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ProductSearchParams(BaseModel):
    q: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    occasion: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    color: Optional[str] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: Optional[int] = 1
    per_page: Optional[int] = 20
