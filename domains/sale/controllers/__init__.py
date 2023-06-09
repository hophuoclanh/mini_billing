from fastapi import APIRouter, Depends, HTTPException
from domains.sale.controllers.order_controller import router as order_controller
from domains.sale.controllers.order_detail_controller import router as order_detail_controller
from domains.sale.schemas.order_schema import OrderResponseSchema, CreateOrderRequestSchema
from sqlalchemy.orm import Session
from repository import get_db
from domains.authentication.models.user_model import UserModel
from dependencies.get_current_user import get_current_user

router = APIRouter(tags=['Sale'])
router.include_router(order_controller, prefix='/order')
router.include_router(order_detail_controller, prefix='/order_detail')
