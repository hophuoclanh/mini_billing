from pydantic import BaseModel, Field
import uuid

class ProductBaseSchema(BaseModel):
    product_name: str
    description: str
    category_id: str
    unit_price: float
    unit_in_stock: int

    class Config:
        orm_mode = True

class CreateProductRequestSchema(ProductBaseSchema):
    pass

class ProductResponseSchema(ProductBaseSchema):
    product_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class UpdateProductRequestSchema(ProductBaseSchema):
    pass
