from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PaymentRequest(BaseModel):
    order_id: int
    method: str
    points_to_use: Optional[int] = 0
    installment: Optional[int] = 1


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    method: str
    amount: float
    points_used: int
    points_earned: int
    installment: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PointsResponse(BaseModel):
    balance: int
    transactions: list

    model_config = {"from_attributes": True}


class InstallmentOption(BaseModel):
    bank: str
    count: int
    monthly: float
    total: float
