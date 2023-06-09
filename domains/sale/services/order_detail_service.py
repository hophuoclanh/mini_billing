from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.sale.models.order_detail_model import OrderDetailModel
from domains.sale.schemas.order_detail_schema import (
    OrderDetailResponseSchema,
    CreateOrderDetailRequestSchema,
    UpdateOrderDetailRequestSchema
)
from repository import session
import uuid
from sqlalchemy.orm import Session
from domains.sale.models.order_model import OrderModel

def get_all_order_details(db: Session) -> list[OrderDetailModel]:
    return db.query(OrderDetailModel).all()

def get_order_detail_by_id(order_detail_id: str, db: Session) -> OrderDetailModel:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail='Order detail not found')
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
        raise HTTPException(status_code=400, detail="Error occurred during creation of OrderDetail.")
    return OrderDetailResponseSchema.from_orm(order_detail)


def update_order_detail(order_detail_id: str, updated_order_detail: UpdateOrderDetailRequestSchema, db: Session) -> OrderDetailResponseSchema:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail='Order detail not found')
    for key, value in updated_order_detail.dict().items():
        setattr(order_detail, key, value)
    try:
        db.commit()
        db.refresh(order_detail)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during update of OrderDetail.")
    return OrderDetailResponseSchema.from_orm(order_detail)

def delete_order_detail(order_detail_id: str, db: Session) -> None:
    order_detail = db.query(OrderDetailModel).filter(OrderDetailModel.order_detail_id == order_detail_id).first()
    if not order_detail:
        raise HTTPException(status_code=404, detail='Order detail not found')
    db.delete(order_detail)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during deletion of OrderDetail.")
