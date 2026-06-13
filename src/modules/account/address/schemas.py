from pydantic import BaseModel

class AddressCreate(BaseModel):
    label: str = "Ev"
    full_name: str | None = None
    phone: str | None = None
    address_line: str
    city: str
    district: str | None = None
    neighborhood: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool = False

class AddressUpdate(BaseModel):
    label: str | None = None
    full_name: str | None = None
    phone: str | None = None
    address_line: str | None = None
    city: str | None = None
    district: str | None = None
    neighborhood: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    is_default: bool | None = None
