from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from domains.authentication.models.user_model import UserModel
from domains.sale.schemas.order_detail_schema import (
    CreateOrderDetailRequestSchema,
    OrderDetailResponseSchema,
    UpdateOrderDetailRequestSchema
)
from domains.sale.models.order_detail_model import OrderDetailModel
from domains.sale.services.order_detail_service import (
    create_order_detail as cod,
    delete_order_detail as dod,
    get_order_detail_by_id as godbi,
    get_all_order_details as gaod,
    update_order_detail as uod
)
from repository import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/", response_model=List[OrderDetailResponseSchema])
def get_all_order_details(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'order_detail'):
        raise HTTPException(status_code=403, detail="User does not have permission to get order details")
    order_details = gaod(db)
    return order_details

@router.get("/{order_detail_id}", response_model=OrderDetailResponseSchema)
def get_order_detail_by_id(
    order_detail_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'order_detail'):
        raise HTTPException(status_code=403, detail="User does not have permission to get an order detail")
    db_order_detail = godbi(order_detail_id=order_detail_id, db=db)
    if db_order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return db_order_detail

@router.post("/", response_model=OrderDetailResponseSchema)
def create_order_detail(
    order_detail: CreateOrderDetailRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'order_detail'):
        raise HTTPException(status_code=403, detail="User does not have permission to create an order detail")
    return cod(order_detail=order_detail, db=db)

@router.put("/{order_detail_id}", response_model=OrderDetailResponseSchema)
def update_order_detail(
    order_detail_id: str,
    order_detail: UpdateOrderDetailRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'update', 'order_detail'):
        raise HTTPException(status_code=403, detail="User does not have permission to update an order detail")
    updated_order_detail = uod(order_detail_id=order_detail_id, updated_order_detail=order_detail, db=db)
    if updated_order_detail is None:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return updated_order_detail

@router.delete("/{order_detail_id}")
def delete_order_detail(
    order_detail_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'order_detail'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete an order detail")
    dod(order_detail_id=order_detail_id)
    return {"detail": "Order detail deleted"}
