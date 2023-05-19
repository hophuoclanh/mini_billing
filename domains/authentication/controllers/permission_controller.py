from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domains.authentication.schemas.permission_schema import PermissionResponseSchema, CreatePermissionRequestSchema
import domains.authentication.services.permission_service as permission_service
from dependencies.get_current_user import get_current_user
from domains.authentication.models.user_model import UserModel  # Changed from UserSchema to UserModel
from repository import get_db

router = APIRouter()

@router.get("/", response_model=list[PermissionResponseSchema])
def get_all_permissions(
    current_user: UserModel = Depends(get_current_user),  # Changed from UserSchema to UserModel
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to view all permissions
    if not current_user.has_permission(db, 'get', 'permission'):  # Modified the permission argument
        raise HTTPException(status_code=403, detail='Not authorized')
    return permission_service.get_all_permissions(db)

@router.get("/{permission_id}", response_model=PermissionResponseSchema)
def get_permission_by_id(
    permission_id: str,
    current_user: UserModel = Depends(get_current_user),  # Changed from UserSchema to UserModel
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to view a permission
    if not current_user.has_permission(db, 'get', 'permission_by_id'):  # Modified the permission argument
        raise HTTPException(status_code=403, detail='Not authorized')
    return permission_service.get_permission_by_id(permission_id, db)

@router.post("/", response_model=PermissionResponseSchema)
def create_permission(
    permission: CreatePermissionRequestSchema,
    current_user: UserModel = Depends(get_current_user),  # Changed from UserSchema to UserModel
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to create a permission
    if not current_user.has_permission(db, 'create', 'permission'):  # Modified the permission argument
        raise HTTPException(status_code=403, detail='Not authorized')
    return permission_service.create_permission(permission=permission, db=db)

@router.put("/{permission_id}")
def update_permission(
    permission_id: str,
    permission: CreatePermissionRequestSchema,
    current_user: UserModel = Depends(get_current_user),  # Changed from UserSchema to UserModel
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to update a permission
    if not current_user.has_permission(db, 'update', 'permission'):  # Modified the permission argument
        raise HTTPException(status_code=403, detail='Not authorized')
    return permission_service.update_permission(permission_id, permission, db)

@router.delete("/{permission_id}")
def delete_permission(
    permission_id: str,
    current_user: UserModel = Depends(get_current_user),  # Changed from UserSchema to UserModel
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to delete a permission
    if not current_user.has_permission(db, 'delete', 'permission'):  # Modified the permission argument
        raise HTTPException(status_code=403, detail='Not authorized')
    return permission_service.delete_permission(permission_id, db)
