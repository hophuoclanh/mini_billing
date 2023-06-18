from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.domains.authentication.schemas.permission_schema import PermissionResponseSchema, CreatePermissionRequestSchema
import backend.domains.authentication.services.permission_service as permission_service
from backend.dependencies.get_current_user import get_current_user
from backend.domains.authentication.models.user_model import UserModel
from backend.repository import get_db

router = APIRouter()

@router.get("/", response_model=list[PermissionResponseSchema])
def get_all_permissions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.has_permission(db, 'get', 'permission'):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    return permission_service.get_all_permissions(db)

@router.get("/{permission_id}", response_model=PermissionResponseSchema)
def get_permission_by_id(
    permission_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.has_permission(db, 'get', 'permission_by_id'):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    permission = permission_service.get_permission_by_id(permission_id, db)
    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return permission

@router.post("/", response_model=PermissionResponseSchema)
def create_permission(
    permission: CreatePermissionRequestSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.has_permission(db, 'create', 'permission'):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    new_permission = permission_service.create_permission(permission=permission, db=db)
    if new_permission is None:
        raise HTTPException(status_code=400, detail="Permission already exists or an error occurred during creation.")
    return new_permission

@router.put("/{permission_id}")
def update_permission(
    permission_id: str,
    permission: CreatePermissionRequestSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.has_permission(db, 'update', 'permission'):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    updated_permission = permission_service.update_permission(permission_id, permission, db)
    if updated_permission is None:
        raise HTTPException(status_code=400, detail="Permission not found or updated permission already exists.")
    return updated_permission

@router.delete("/{permission_id}")
def delete_permission(
    permission_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user.has_permission(db, 'delete', 'permission'):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    if not permission_service.delete_permission(permission_id, db):
        raise HTTPException(status_code=400, detail="Permission not found or error occurred during deletion.")
    return {"detail": "Permission successfully deleted"}
