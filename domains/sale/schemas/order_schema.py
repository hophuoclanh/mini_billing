from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import uuid

class OrderBaseSchema(BaseModel):
    total_amount: float

    class Config:
        orm_mode = True

class CreateOrderRequestSchema(OrderBaseSchema):
    pass

class OrderResponseSchema(OrderBaseSchema):
    order_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    date: datetime  # change str to datetime

class UpdateOrderRequestSchema(OrderBaseSchema):
    pass
