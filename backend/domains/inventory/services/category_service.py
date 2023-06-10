from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.inventory.models.category_model import CategoryModel
from domains.inventory.schemas.category_schema import (
    CategoryResponseSchema,
    CreateCategoryRequestSchema,
    UpdateCategoryRequestSchema
)
from repository import session
import uuid

def get_all_categories() -> list[CategoryModel]:
    return session.query(CategoryModel).all()
def get_category_by_id(category_id: str) -> CategoryModel:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

def create_category(category: CreateCategoryRequestSchema) -> CategoryResponseSchema:
    category_dict = category.dict()
    existing_category = session.query(CategoryModel).filter(CategoryModel.category_name == category_dict['category_name']).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category already exists.")
    category_dict['category_id'] = str(uuid.uuid4())
    category = CategoryModel(**category_dict)
    session.add(category)
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Category.")
    return CategoryResponseSchema(**category_dict)

def update_category(category_id: str, updated_category: UpdateCategoryRequestSchema) -> CategoryResponseSchema:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    for key, value in updated_category.dict().items():
        setattr(category, key, value)
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during update of Category.")
    return CategoryResponseSchema.from_orm(category)

def delete_category(category_id: str) -> None:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    session.delete(category)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during deletion of Category.")
