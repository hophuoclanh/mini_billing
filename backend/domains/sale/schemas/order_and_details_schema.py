from pydantic import BaseModel
from typing import List

class OrderAndDetailsRequestSchema(BaseModel):
    product_name: str
    quantity: int

class CreateOrderAndDetailsRequestSchema(BaseModel):
    order_details: List[OrderAndDetailsRequestSchema]