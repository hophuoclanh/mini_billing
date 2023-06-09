from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.sale.models.order_model import OrderModel
from domains.sale.schemas.order_schema import (
    OrderResponseSchema,
    CreateOrderRequestSchema,
    UpdateOrderRequestSchema
)
from repository import session
import uuid
from sqlalchemy.orm import Session

def get_all_orders(db: Session) -> list[OrderModel]:
    return db.query(OrderModel).all()

def get_order_by_id(order_id: str, db: Session) -> OrderModel:
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    return OrderResponseSchema.from_orm(order)

def create_order(order: CreateOrderRequestSchema, user_id: str, db: Session) -> OrderResponseSchema:
    order_dict = order.dict()
    order_dict['order_id'] = str(uuid.uuid4())
    order_dict['user_id'] = user_id
    order = OrderModel(**order_dict)
    db.add(order)
    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Order.")
    return OrderResponseSchema.from_orm(order)

def update_order(order_id: str, updated_order: UpdateOrderRequestSchema) -> OrderResponseSchema:
    order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    for key, value in updated_order.dict().items():
        setattr(order, key, value)
    try:
        session.commit()
        session.refresh(order)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during update of Order.")
    return OrderResponseSchema.from_orm(order)  # change here

def delete_order(order_id: str) -> None:
    order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail='Order not found')
    session.delete(order)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during deletion of Order.")
