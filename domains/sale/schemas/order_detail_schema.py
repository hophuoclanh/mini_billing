from pydantic import BaseModel, Field
import uuid

class OrderDetailBaseSchema(BaseModel):
    order_id: str
    product_id: str
    quantity: int
    price_per_unit: float

    class Config:
        orm_mode = True

class CreateOrderDetailRequestSchema(OrderDetailBaseSchema):
    pass

class OrderDetailResponseSchema(OrderDetailBaseSchema):
    order_detail_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    total_amount_per_product: float

class UpdateOrderDetailRequestSchema(OrderDetailBaseSchema):
    pass
