from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.inventory.models.product_model import ProductModel
from domains.inventory.schemas.product_schema import (
    ProductResponseSchema,
    CreateProductRequestSchema,
    UpdateProductRequestSchema
)
from repository import session
import uuid
from sqlalchemy.orm import Session

def get_all_products(db: Session) -> list[ProductModel]:
    return db.query(ProductModel).all()

def get_product_by_id(product_id: str) -> ProductModel:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return ProductResponseSchema.from_orm(product)

def create_product(product: CreateProductRequestSchema) -> ProductResponseSchema:
    product_dict = product.dict()
    existing_product = session.query(ProductModel).filter(ProductModel.product_name == product_dict['product_name']).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Product already exists.")
    product_dict['product_id'] = str(uuid.uuid4())
    product = ProductModel(**product_dict)
    session.add(product)
    try:
        session.commit()
        session.refresh(product)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Product.")
    return ProductResponseSchema(**product_dict)

def update_product(product_id: str, updated_product: UpdateProductRequestSchema) -> ProductResponseSchema:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    for key, value in updated_product.dict().items():
        setattr(product, key, value)
    try:
        session.commit()
        session.refresh(product)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during update of Product.")
    return ProductResponseSchema.from_orm(product)

def delete_product(product_id: str) -> None:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    session.delete(product)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during deletion of Product.")
