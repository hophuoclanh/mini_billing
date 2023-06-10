from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from domains.authentication.models.user_model import UserModel
from domains.inventory.schemas.category_schema import (
    CreateCategoryRequestSchema,
    CategoryResponseSchema,
    UpdateCategoryRequestSchema
)
from domains.inventory.models.category_model import CategoryModel
from domains.inventory.services.category_service import (
    create_category as cc,
    delete_category as dc,
    get_category_by_id as gcbi,
    get_all_categories as gac,
    update_category as uc
)
from repository import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CategoryResponseSchema])
def get_all_categories(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'category'):
        raise HTTPException(status_code=403, detail="User does not have permission to get categories")
    categories_orm = gac()
    categories = [CategoryResponseSchema.from_orm(category) for category in categories_orm]
    return categories


@router.get("/{category_id}", response_model=CategoryResponseSchema)
def get_category_by_id(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'category_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get a category")
    db_category_orm = gcbi(category_id=category_id)
    if db_category_orm is None:
        raise HTTPException(status_code=404, detail="Category not found")
    db_category = CategoryResponseSchema.from_orm(db_category_orm)
    return db_category

@router.post("/", response_model=CategoryResponseSchema)
def create_category(
    category: CreateCategoryRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'category'):
        raise HTTPException(status_code=403, detail="User does not have permission to create a category")
    return cc(category=category)

@router.put("/{category_id}", response_model=CategoryResponseSchema)
def update_category(
    category_id: str,
    category: UpdateCategoryRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'update', 'category'):
        raise HTTPException(status_code=403, detail="User does not have permission to update a category")
    updated_category = uc( category_id=category_id,  updated_category=category)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category

@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'category'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete a category")
    dc(category_id=category_id)
    return {"detail": "Category deleted"}
