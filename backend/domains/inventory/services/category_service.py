from sqlalchemy.exc import IntegrityError
from backend.domains.inventory.models.category_model import CategoryModel
from backend.domains.inventory.schemas.category_schema import (
    CategoryResponseSchema,
    CreateCategoryRequestSchema,
    UpdateCategoryRequestSchema
)
from backend.repository import session
import uuid

def get_all_categories() -> list[CategoryModel]:
    return session.query(CategoryModel).all()

def get_category_by_id(category_id: str) -> CategoryModel:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    return category

def create_category(category: CreateCategoryRequestSchema) -> CategoryResponseSchema:
    category_dict = category.dict()
    existing_category = session.query(CategoryModel).filter(CategoryModel.category_name == category_dict['category_name']).first()
    if existing_category:
        return None
    category_dict['category_id'] = str(uuid.uuid4())
    category = CategoryModel(**category_dict)
    session.add(category)
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        return None
    return CategoryResponseSchema(**category_dict)

def update_category(category_id: str, updated_category: UpdateCategoryRequestSchema) -> CategoryResponseSchema:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    if not category:
        return None
    for key, value in updated_category.dict().items():
        setattr(category, key, value)
    try:
        session.commit()
        session.refresh(category)
    except IntegrityError:
        session.rollback()
        return None
    return CategoryResponseSchema.from_orm(category)

def delete_category(category_id: str) -> bool:
    category = session.query(CategoryModel).filter(CategoryModel.category_id == category_id).first()
    if not category:
        return False
    session.delete(category)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return False
    return True
