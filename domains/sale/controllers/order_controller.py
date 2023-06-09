from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from domains.authentication.models.user_model import UserModel
from domains.authentication.schemas.user_schema import UserSchema
from domains.sale.schemas.order_schema import (
    CreateOrderRequestSchema,
    OrderResponseSchema,
    UpdateOrderRequestSchema
)
from domains.sale.models.order_model import OrderModel
from domains.sale.services.order_service import (
    create_order as co,
    delete_order as do,
    get_order_by_id as gobi,
    get_all_orders as gao,
    update_order as uo
)
from repository import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/", response_model=List[OrderResponseSchema])
def get_all_orders(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to get orders")
    orders = gao(db)
    return orders

@router.get("/{order_id}", response_model=OrderResponseSchema)
def get_order_by_id(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'order_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get an order")
    db_order = gobi(order_id=order_id, db=db)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@router.post("/", response_model=OrderResponseSchema)
def create_order(
    order: CreateOrderRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to create an order")
    return co(order=order, user_id=current_user.user_id, db=db)

@router.put("/{order_id}", response_model=OrderResponseSchema)
def update_order(
    order_id: str,
    order: UpdateOrderRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'update', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to update an order")
    updated_order = uo(order_id=order_id, updated_order=order)
    if updated_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{order_id}")
def delete_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'order'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete an order")
    do(order_id=order_id)
    return {"detail": "Order deleted"}
