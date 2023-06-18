from sqlalchemy.exc import IntegrityError
from backend.domains.inventory.models.product_model import ProductModel
from backend.domains.inventory.models.category_model import CategoryModel
from backend.domains.inventory.schemas.product_schema import (
    ProductResponseSchema,
    CreateProductRequestSchema,
    UpdateProductRequestSchema
)
from backend.repository import session
import uuid
from sqlalchemy.orm import Session
from typing import List

def get_all_products(db: Session) -> list[ProductModel]:
    products = db.query(ProductModel).all()
    if any(product.description is None or product.category_id is None for product in products):
        return None
    return products

def get_product_by_id(product_id: str) -> ProductModel:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    return ProductResponseSchema.from_orm(product) if product else None

def create_products(product_request: CreateProductRequestSchema) -> List[ProductResponseSchema]:
    response = []
    for product in product_request.products:
        product_dict = product.dict()
        existing_product = session.query(ProductModel).filter(ProductModel.product_name == product_dict['product_name']).first()
        if existing_product:
            return None
        product_dict['product_id'] = str(uuid.uuid4())
        new_product = ProductModel(**product_dict)
        session.add(new_product)
        try:
            session.commit()
            session.refresh(new_product)
        except IntegrityError:
            session.rollback()
            return None
        response.append(ProductResponseSchema(**product_dict))
    return response

def update_product(product_id: str, updated_product: UpdateProductRequestSchema) -> ProductResponseSchema:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        return None
    for key, value in updated_product.dict().items():
        if value is not None:
            setattr(product, key, value)
    try:
        session.commit()
        session.refresh(product)
    except IntegrityError:
        session.rollback()
        return None
    return ProductResponseSchema.from_orm(product)

def delete_product(product_id: str) -> bool:
    product = session.query(ProductModel).filter(ProductModel.product_id == product_id).first()
    if not product:
        return False
    session.delete(product)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return False
    return True

def get_products_by_category_name(category_name: str, db: Session) -> list[ProductModel]:
    category = db.query(CategoryModel).filter(CategoryModel.category_name == category_name).first()
    if not category:
        return None

    products = db.query(ProductModel).filter(ProductModel.category_id == category.category_id).all()
    return [ProductResponseSchema.from_orm(product) for product in products] if products else None
