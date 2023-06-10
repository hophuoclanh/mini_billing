from pydantic import BaseModel
from typing import List

class OrderAndOrderDetailRequestSchema(BaseModel):
    product_name: str
    quantity: int

class CreateOrderAndOrderDetailRequestSchema(BaseModel):
    order_details: List[OrderAndOrderDetailRequestSchema]