from pydantic import BaseModel
from typing import Optional


class SupplierCreate(BaseModel):
    company_name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    supplier_type: str = "producer"
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website_url: Optional[str] = None
    is_organic_certified: bool = False
    is_halal_certified: bool = False
    certifications: Optional[str] = None
    product_categories: Optional[str] = None
    kitchen_photos: Optional[str] = None


class SupplierUpdate(BaseModel):
    company_name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    supplier_type: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website_url: Optional[str] = None
    is_organic_certified: Optional[bool] = None
    is_halal_certified: Optional[bool] = None
    certifications: Optional[str] = None
    product_categories: Optional[str] = None
    kitchen_photos: Optional[str] = None
    is_active: Optional[bool] = None


class SupplierResponse(BaseModel):
    id: int
    company_name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    supplier_type: str
    city: Optional[str] = None
    district: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    website_url: Optional[str] = None
    is_organic_certified: bool
    is_halal_certified: bool
    certifications: Optional[str] = None
    product_categories: Optional[str] = None
    kitchen_photos: Optional[str] = None
    rating: float
    review_count: int
    verification_status: str
    is_active: bool


class SupplierPageResponse(SupplierResponse):
    products: list["ProductResponse"] = []


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    unit: str = "kg"
    price_per_unit: Optional[float] = None
    is_organic: bool = False
    is_local: bool = False
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    unit: Optional[str] = None
    price_per_unit: Optional[float] = None
    is_organic: Optional[bool] = None
    is_local: Optional[bool] = None
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    supplier_id: int
    name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    unit: str
    price_per_unit: Optional[float] = None
    is_organic: bool
    is_local: bool
    season_start_month: Optional[int] = None
    season_end_month: Optional[int] = None
    image_url: Optional[str] = None
    is_active: bool


class LinkSupplier(BaseModel):
    supplier_id: int
    is_preferred: bool = False
    contract_start: Optional[str] = None
    contract_end: Optional[str] = None
    notes: Optional[str] = None


class SupplierLinkResponse(BaseModel):
    id: int
    restaurant_id: int
    supplier_id: int
    supplier_name: str
    is_preferred: bool
    contract_start: Optional[str] = None
    contract_end: Optional[str] = None
    notes: Optional[str] = None


class IngredientCreate(BaseModel):
    supplier_product_id: int
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    is_visible_to_customer: bool = True


class IngredientUpdate(BaseModel):
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    is_visible_to_customer: Optional[bool] = None


class IngredientResponse(BaseModel):
    id: int
    menu_item_id: int
    supplier_product_id: int
    product_name: str
    supplier_name: str
    supplier_slug: str
    quantity: Optional[float] = None
    unit: Optional[str] = None
    notes: Optional[str] = None
    is_visible_to_customer: bool


class TransparencyScoreResponse(BaseModel):
    restaurant_id: int
    total_menu_items: int
    items_with_ingredients: int
    total_suppliers_linked: int
    transparency_percentage: float
    total_points: int
    last_calculated_at: str


class TraceResponse(BaseModel):
    menu_item_id: int
    menu_item_name: str
    ingredients: list[IngredientResponse] = []
