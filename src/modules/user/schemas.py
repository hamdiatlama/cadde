from datetime import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    phone: str | None = None
    password: str
    full_name: str
    role: str = "customer"


class UserLogin(BaseModel):
    email: str
    password: str


class UserUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    points: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
