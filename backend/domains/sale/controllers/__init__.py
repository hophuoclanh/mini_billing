from fastapi import APIRouter, Depends, HTTPException
from backend.domains.sale.controllers.order_controller import router as order_controller
from backend.domains.sale.controllers.order_detail_controller import router as order_detail_controller
from sqlalchemy.orm import Session
from backend.repository import get_db
from backend.domains.authentication.models.user_model import UserModel
from backend.dependencies.get_current_user import get_current_user
from backend.domains.sale.services.order_and_details_service import (
    create_order_and_details,
    get_orders_by_time_range as gobtr
)
from backend.domains.sale.schemas.order_and_details_schema import CreateOrderAndDetailsRequestSchema
from datetime import datetime

router = APIRouter(tags=['Sale'])
router.include_router(order_controller, prefix='/order')
router.include_router(order_detail_controller, prefix='/order_detail')

@router.post("/")
def create_super_order(
    order: CreateOrderAndDetailsRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to create an order")
    result = create_order_and_details(order_request=order, db=db, current_user=current_user)
    print(result)
    return result

@router.get("/orders/time_range")
async def get_orders_by_time_range(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to get orders")

    orders = gobtr(start_date, end_date, db)
    return orders




