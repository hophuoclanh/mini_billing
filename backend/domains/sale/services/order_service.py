from sqlalchemy.exc import IntegrityError
from backend.domains.sale.models.orders_model import OrderModel
from backend.domains.sale.schemas.order_schema import (
    OrderResponseSchema,
    CreateOrderRequestSchema,
    UpdateOrderRequestSchema
)
from backend.repository import session
import uuid
from sqlalchemy.orm import Session

def get_all_orders(db: Session) -> list[OrderModel]:
    return db.query(OrderModel).all()

def get_order_by_id(order_id: str, db: Session) -> OrderModel:
    order = db.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        return None
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
        return None
    return OrderResponseSchema.from_orm(order)

def update_order(order_id: str, updated_order: UpdateOrderRequestSchema) -> OrderResponseSchema:
    order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        return None
    for key, value in updated_order.dict().items():
        setattr(order, key, value)
    try:
        session.commit()
        session.refresh(order)
    except IntegrityError:
        session.rollback()
        return None
    return OrderResponseSchema.from_orm(order)

def delete_order(order_id: str) -> bool:
    order = session.query(OrderModel).filter(OrderModel.order_id == order_id).first()
    if not order:
        return False
    session.delete(order)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return False
    return True
