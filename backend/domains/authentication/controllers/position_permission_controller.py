from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.domains.authentication.schemas.position_permission_schema import CreatePositionPermissionSchema, PositionPermissionSchema
import backend.domains.authentication.services.position_permission_service as position_permission_service
from backend.dependencies.get_current_user import get_current_user
from backend.domains.authentication.models.user_model import UserModel
from backend.repository import get_db

router = APIRouter()

@router.get("/", response_model=list[PositionPermissionSchema])
def get_all_position_permissions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "get", "position_permission"):
        raise HTTPException(status_code=403, detail="Permission denied")
    return position_permission_service.get_all_position_permissions(db)

@router.get("/{position_permission_id}", response_model=PositionPermissionSchema)
def get_position_permission_by_id(
    position_permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "get", "position_permission_by_id"):
        raise HTTPException(status_code=403, detail="Permission denied")
    position_permission = position_permission_service.get_position_permission_by_id(position_permission_id, db)
    if position_permission is None:
        raise HTTPException(status_code=404, detail="Position Permission not found")
    return position_permission

@router.post("/", response_model=PositionPermissionSchema)
def create_position_permission(
    position_permission: CreatePositionPermissionSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "create", "position_permission"):
        raise HTTPException(status_code=403, detail="Permission denied")
    position_permission_db = position_permission_service.create_position_permission(position_permission, db)
    if position_permission_db is None:
        raise HTTPException(status_code=400, detail="Error creating Position Permission or Position Permission already exists.")
    return position_permission_db

@router.put("/{position_permission_id}")
def update_position_permission(
    position_permission_id: str,
    position_permission: CreatePositionPermissionSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "update", "position_permission"):
        raise HTTPException(status_code=403, detail="Permission denied")
    updated_position_permission = position_permission_service.update_position_permission(position_permission_id, position_permission, db)
    if updated_position_permission is None:
        raise HTTPException(status_code=400, detail="Error updating Position Permission or Position Permission already exists.")
    return updated_position_permission

@router.delete("/{position_permission_id}")
def delete_position_permission(
    position_permission_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "delete", "position_permission"):
        raise HTTPException(status_code=403, detail="Permission denied")
    if not position_permission_service.delete_position_permission(position_permission_id, db):
        raise HTTPException(status_code=400, detail="Error deleting Position Permission")
