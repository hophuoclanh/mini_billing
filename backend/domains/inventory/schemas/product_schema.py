from pydantic import BaseModel, Field
import uuid
from typing import List
from typing import Optional

class ProductBaseSchema(BaseModel):
    product_name: str
    description: str
    category_id: str
    unit_price: float
    unit_in_stock: int

    class Config:
        orm_mode = True

class CreateProductRequestSchema(BaseModel):
    products: List[ProductBaseSchema]

class ProductResponseSchema(ProductBaseSchema):
    product_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class UpdateProductRequestSchema(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[str] = None
    unit_price: Optional[float] = None
    unit_in_stock: Optional[int] = None

class ProductListResponseSchema(BaseModel):
    products: List[ProductResponseSchema]
