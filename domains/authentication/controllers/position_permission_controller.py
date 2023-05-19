from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domains.authentication.schemas.position_permission_schema import CreatePositionPermissionSchema, PositionPermissionSchema
import domains.authentication.services.position_permission_service as position_permission_service
from dependencies.get_current_user import get_current_user
from domains.authentication.models.user_model import UserModel
from repository import get_db

router = APIRouter()

@router.get("/", response_model=list[PositionPermissionSchema])
def get_all_position_permissions(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to view all position permissions
    if not current_user.has_permission(db, 'get', 'position_permission'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return position_permission_service.get_all_position_permissions(db)

@router.get("/{position_permission_id}", response_model=PositionPermissionSchema)
def get_position_permission_by_id(
    position_permission_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to view a position permission
    if not current_user.has_permission(db, 'get', 'position_permission_by_id'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return position_permission_service.get_position_permission_by_id(position_permission_id, db)

@router.post("/", response_model=PositionPermissionSchema)
def create_position_permission(
    position_permission: CreatePositionPermissionSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the user has the required permission
    if not current_user.has_permission(db, 'create', 'position_permission'):
        raise HTTPException(status_code=403, detail="User does not have permission to create a position permission")
    try:
        return position_permission_service.create_position_permission(position_permission, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{position_permission_id}")
def update_position_permission(
    position_permission_id: str,
    position_permission: CreatePositionPermissionSchema,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to update a position permission
    if not current_user.has_permission(db, 'update', 'position_permission'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return position_permission_service.update_position_permission(position_permission_id, position_permission, db)

@router.delete("/{position_permission_id}")
def delete_position_permission(
    position_permission_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if the current user has permission to delete a position permission
    if not current_user.has_permission(db, 'delete', 'position_permission'):
        raise HTTPException(status_code=403, detail='Not authorized')
    return position_permission_service.delete_position_permission(position_permission_id, db)
