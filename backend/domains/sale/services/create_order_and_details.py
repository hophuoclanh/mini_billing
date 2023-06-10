from domains.inventory.models.product_model import ProductModel
from domains.inventory.schemas.product_schema import ProductResponseSchema
from domains.sale.models.order_model import OrderModel
from domains.sale.schemas.order_schema import OrderResponseSchema
from domains.sale.schemas.order_and_order_detail_schema import CreateOrderAndOrderDetailRequestSchema
from domains.sale.models.order_detail_model import OrderDetailModel
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from domains.authentication.models.user_model import UserModel

def create_order_and_details(order_request: CreateOrderAndOrderDetailRequestSchema, db: Session, current_user: UserModel) -> dict:
    # create a new order
    order_dict = {'user_id': current_user.user_id, 'order_id': str(uuid.uuid4()), 'total_amount': 0}
    order = OrderModel(**order_dict)
    db.add(order)
    db.flush()  # Get the new order id

    products = []

    # create order details and update total_amount in order
    for detail in order_request.order_details:
        product = db.query(ProductModel).filter(ProductModel.product_name == detail.product_name).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.unit_in_stock < detail.quantity:
            raise HTTPException(status_code=400, detail="Not enough products in stock")

        products.append({
            **ProductResponseSchema.from_orm(product).dict(),
            'quantity': detail.quantity,
            'total_money': detail.quantity * product.unit_price,
        })
        product.unit_in_stock -= detail.quantity  # decrease the amount in stock

        total_amount_per_product = product.unit_price * detail.quantity

        order_detail_dict = {
            'order_detail_id': str(uuid.uuid4()),
            'order_id': order.order_id,
            'product_id': product.product_id,
            'quantity': detail.quantity,
            'price_per_unit': product.unit_price,
            'total_amount_per_product': total_amount_per_product,
        }

        order_detail = OrderDetailModel(**order_detail_dict)
        db.add(order_detail)

        order.total_amount += total_amount_per_product  # increase total_amount in Order

    try:
        db.commit()
        db.refresh(order)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Order and OrderDetails.")
    return {
        **OrderResponseSchema.from_orm(order).dict(),
        'products': products,
    }
