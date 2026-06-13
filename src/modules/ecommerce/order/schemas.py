from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    seller_id: int
    items: List[OrderItemCreate]
    delivery_address: Optional[str] = None
    delivery_latitude: Optional[float] = None
    delivery_longitude: Optional[float] = None
    recipient_name: Optional[str] = None
    recipient_phone: Optional[str] = None
    notes: Optional[str] = None
    scheduled_date: Optional[datetime] = None
    delivery_time_slot: Optional[str] = None
    is_express: Optional[bool] = False
    is_gift: Optional[bool] = False
    gift_card_message: Optional[str] = None
    gift_card_sender: Optional[str] = None
    coupon_code: Optional[str] = None
    payment_method: Optional[str] = "card"


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    seller_id: int
    courier_id: Optional[int]
    status: str
    subtotal: float
    delivery_fee: float
    total: float
    payment_method: str
    payment_status: str
    delivery_address: Optional[str]
    scheduled_date: Optional[datetime]
    delivery_time_slot: Optional[str] = None
    is_express: bool = False
    is_gift: bool = False
    gift_card_message: Optional[str] = None
    gift_card_sender: Optional[str] = None
    coupon_code: Optional[str] = None
    discount_amount: float = 0
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    reject_reason: Optional[str] = None
    approval_deadline: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None
    cancel_reason: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderCancelRequest(BaseModel):
    reason: str


class OrderModifyRequest(BaseModel):
    notes: Optional[str] = None
    delivery_address: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_phone: Optional[str] = None
    scheduled_date: Optional[datetime] = None
