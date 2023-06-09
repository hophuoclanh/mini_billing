from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from backend.domains.sale.models.order_detail_model import OrderDetailModel
from backend.domains.sale.schemas.order_detail_schema import (
    OrderDetailResponseSchema,
    CreateOrderDetailRequestSchema,
    UpdateOrderDetailRequestSchema
)
import uuid
from sqlalchemy.orm import Session
from backend.domains.sale.models.orders_model import OrderModel

def get_all_order_details(db: Session) -> list[OrderDetailModel]:
    return db.query(OrderDetailModel).all()

def get_order_detail_by_id(order_detail_id: str, db: Session) -> OrderDetailModel:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        return None
    return OrderDetailResponseSchema.from_orm(order_detail)

def create_order_detail(order_detail: CreateOrderDetailRequestSchema, db: Session) -> OrderDetailResponseSchema:
    order_detail_dict = order_detail.dict()
    order_detail_dict['order_detail_id'] = str(uuid.uuid4())
    order_detail_dict['total_amount_per_product'] = order_detail_dict['price_per_unit'] * order_detail_dict['quantity']
    order_detail = OrderDetailModel(**order_detail_dict)
    db.add(order_detail)

    # get or create an order with the same order_id
    order = db.query(OrderModel).filter(OrderModel.order_id == order_detail.order_id).first()
    if not order:
        order_dict = {"order_id": order_detail.order_id, "total_amount": order_detail.total_amount_per_product, "user_id": order_detail.user_id}
        order = OrderModel(**order_dict)
        db.add(order)
    else:
        order.total_amount += order_detail.total_amount_per_product  # increase total_amount in Order

    try:
        db.commit()
        db.refresh(order_detail)
    except IntegrityError:
        db.rollback()
        return None
    return OrderDetailResponseSchema.from_orm(order_detail)

def update_order_detail(order_detail_id: str, updated_order_detail: UpdateOrderDetailRequestSchema, db: Session) -> OrderDetailResponseSchema:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        return None
    for key, value in updated_order_detail.dict().items():
        setattr(order_detail, key, value)

    try:
        db.commit()
        db.refresh(order_detail)
    except IntegrityError:
        db.rollback()
        return None
    return OrderDetailResponseSchema.from_orm(order_detail)

def delete_order_detail(order_detail_id: str, db: Session) -> bool:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        return False
    db.delete(order_detail)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return False
    return True
