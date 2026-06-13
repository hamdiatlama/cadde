from pydantic import BaseModel

class AddItem(BaseModel):
    product_id: int
    quantity: int = 1
    variant_label: str | None = None

class UpdateItem(BaseModel):
    quantity: int
