from datetime import datetime
from pydantic import BaseModel

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    type: str
    title: str
    message: str | None = None
    reference_type: str | None = None
    reference_id: int | None = None
    is_read: bool
    created_at: datetime | None = None

    class Config:
        from_attributes = True
