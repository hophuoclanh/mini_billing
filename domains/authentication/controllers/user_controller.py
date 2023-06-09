from fastapi import APIRouter, Depends, HTTPException
from dependencies.get_current_user import get_current_user
from domains.authentication.schemas.user_schema import CreateUserRequestSchema, UserSchema, CreateUserResponseSchema
from domains.authentication.schemas.update_user_schema import UpdateUserSchema
from domains.authentication.schemas.permission_schema import PermissionResponseSchema
from domains.authentication.models.user_model import UserModel
import domains.authentication.services.user_service as user_service
from repository import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get('')
def get_user(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> list[UserSchema]:
    if not current_user.has_permission(db, "get", "user"):
        raise HTTPException(status_code=403, detail="Permission denied")
    users = user_service.get_all_users()
    return [UserSchema.from_orm(user) for user in users]

@router.get('/{user_id}')
def get_user_by_id(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> UserSchema:
    if not current_user.has_permission(db, "get", "user_by_id"):
        raise HTTPException(status_code=403, detail="Permission denied")
    return user_service.get_user_by_id(user_id)

@router.post('', response_model=CreateUserResponseSchema)
def create_user(
    user: CreateUserRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> CreateUserResponseSchema:
    if not current_user.has_permission(db, "create", "user"):
        raise HTTPException(status_code=403, detail="Permission denied")
    created_user = user_service.create_user(user)
    return created_user

@router.put('/{user_id}')
def update_user(
    user_id: str,
    updated_user: UpdateUserSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, "update", "user"):
        raise HTTPException(status_code=403, detail="Permission denied")
    user_service.update_user(user_id, updated_user)

@router.delete('/{user_id}')
def delete_user(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, "delete", "user"):
        raise HTTPException(status_code=403, detail="Permission denied")
    user_service.delete_user(user_id)

@router.get('/{user_id}/permissions', response_model= List[PermissionResponseSchema])
def get_user_permissions(
    user_id: str,
    db: Session = Depends(get_db),
) -> list[PermissionResponseSchema]:
    user = user_service.get_user_by_id(user_id)
    permissions = user.get_permissions(db)
    return [PermissionResponseSchema.from_orm(permission) for permission in permissions]
