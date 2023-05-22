from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from dependencies.get_current_user import get_current_user
from domains.authentication.models.user_model import UserModel
from domains.authentication.schemas.position_schema import (
    CreatePositionRequestSchema,
    PositionResponseSchema,
    UpdatePositionRequestSchema
)
from domains.authentication.models.position_model import PositionModel
from domains.authentication.services.position_service import (
    create_position,
    delete_position,
    get_position_by_id,
    get_all_positions,
    update_position
)
from repository import get_db

router = APIRouter()

@router.get("/", response_model=List[PositionResponseSchema])
def get_all_positions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # Change UserSchema to UserModel
):
    if not current_user.has_permission(db, 'get', 'position'):
        raise HTTPException(status_code=403, detail="User does not have permission to get positions")
    positions = get_all_positions(db)
    return positions

@router.get("/{position_id}", response_model=PositionResponseSchema)
def get_position_by_id(
    position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'get', 'position_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get position data")
    db_position = get_position_by_id(db, position_id=position_id)
    if db_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return db_position

@router.post("/", response_model=PositionResponseSchema)
def create_new_position(
    position: CreatePositionRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # Change UserSchema to UserModel
):
    if not current_user.has_permission(db, 'create', 'position'):
        raise HTTPException(status_code=403, detail="User does not have permission to create a position")
    return create_position(db=db, position=position)

@router.put("/{position_id}", response_model=PositionResponseSchema)
def update_position(
    position_id: str,
    position: UpdatePositionRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'update', 'position'):
        raise HTTPException(status_code=403, detail="User does not have permission to update position data")
    updated_position = update_position(db=db, position_id=position_id, position=position)
    if updated_position is None:
        raise HTTPException(status_code=404, detail="Position not found")
    return updated_position

@router.delete("/{position_id}")
def delete_position(
    position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, 'delete', 'position'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete position")
    delete_position(db=db, position_id=position_id)
    return {"detail": "Position deleted"}