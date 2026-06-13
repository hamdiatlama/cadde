from datetime import datetime
from pydantic import BaseModel


class SellerUpdate(BaseModel):
    store_name: str | None = None
    slug: str | None = None
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class SellerResponse(BaseModel):
    id: int
    user_id: int
    store_name: str
    slug: str | None = None
    description: str | None = None
    phone: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    rating: float
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class QuestionCreate(BaseModel):
    product_id: int
    question: str


class AnswerCreate(BaseModel):
    answer: str


class QuestionResponse(BaseModel):
    id: int
    product_id: int
    user_id: int
    question: str
    answer: str | None = None
    answered_at: datetime | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
