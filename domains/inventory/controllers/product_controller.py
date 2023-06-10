from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from domains.authentication.models.user_model import UserModel
from domains.inventory.schemas.product_schema import (
    CreateProductRequestSchema,
    ProductResponseSchema,
    UpdateProductRequestSchema
)
from domains.inventory.models.product_model import ProductModel
from domains.inventory.services.product_service import (
    create_product as cp,
    delete_product as dp,
    get_product_by_id as gpid,
    get_all_products as gap,
    update_product as up
)
from repository import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductResponseSchema])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to get products")
    products = gap(db)
    return products

@router.get("/{product_id}", response_model=ProductResponseSchema)
def get_product_by_id(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'product_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get a product")
    db_product = gpid(product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/", response_model=ProductResponseSchema)
def create_product(
    product: CreateProductRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to create a product")
    return cp(product=product)

@router.put("/{product_id}", response_model=ProductResponseSchema)
def update_product(
    product_id: str,
    product: UpdateProductRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'update', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to update a product")
    updated_product = up(product_id=product_id, updated_product=product)
    if updated_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete a product")
    dp(product_id=product_id)
    return {"detail": "Product deleted"}
