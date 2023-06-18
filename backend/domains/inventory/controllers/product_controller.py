from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.inventory.schemas.product_schema import (
    CreateProductRequestSchema,
    ProductResponseSchema,
    UpdateProductRequestSchema,
    ProductListResponseSchema
)
from backend.domains.inventory.services.product_service import (
    create_products as cp,
    delete_product as dp,
    get_product_by_id as gpid,
    get_all_products as gap,
    update_product as up,
    get_products_by_category_name
)
from backend.repository import get_db
from backend.dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductResponseSchema])
def get_all_products(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to get products")
    products = gap(db)
    if products is None:
        raise HTTPException(status_code=400, detail="Some products have missing description or category_id.")
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

@router.post("/", response_model=ProductListResponseSchema)
def create_products(
    product_request: CreateProductRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'create', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to create products")
    created_products = cp(product_request=product_request)
    if created_products is None:
        raise HTTPException(status_code=400, detail="Product already exists or an error occurred during creation.")
    return {"products": created_products}

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
        raise HTTPException(status_code=400, detail="Product not found or error occurred during update.")
    return updated_product

@router.delete("/{product_id}")
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete a product")
    if not dp(product_id=product_id):
        raise HTTPException(status_code=400, detail="Product not found or error occurred during deletion.")
    return {"detail": "Product deleted"}

@router.get("/category/{category_name}/products", response_model=list[ProductResponseSchema])
async def read_products_by_category_name(
    category_name: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'product'):
        raise HTTPException(status_code=403, detail="User does not have permission to get products by category")
    products = get_products_by_category_name(category_name, db)
    if products is None:
        raise HTTPException(status_code=404, detail='No category or products found for this category')
    return products
