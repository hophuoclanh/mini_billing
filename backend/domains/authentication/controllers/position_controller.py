from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.dependencies.get_current_user import get_current_user
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.authentication.schemas.position_schema import (
    CreatePositionRequestSchema,
    PositionResponseSchema,
    UpdatePositionRequestSchema
)
from backend.domains.authentication.services.position_service import (
    create_position,
    delete_position as dp,
    get_position_by_id as fetch_position_by_id,
    get_all_positions as fetch_all_positions,
    update_position as up,
)
from backend.repository import get_db

router = APIRouter()

@router.get("/", response_model=List[PositionResponseSchema])
def get_all_positions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "get", "position"):
        raise HTTPException(
            status_code=403,
            detail="User does not have the required permissions",
        )

    positions = fetch_all_positions()  # calls the renamed function
    return positions

@router.get("/{position_id}", response_model=PositionResponseSchema)
def get_position_by_id(
    position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "get", "position_by_id"):
        raise HTTPException(status_code=403, detail="User does not have the required permissions")
    position = fetch_position_by_id(position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position

@router.delete("/{position_id}")
def delete_position(
    position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "delete", "position"):
        raise HTTPException(status_code=403, detail="User does not have the required permissions")
    position = dp(position_id=position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found or error occurred during deletion")
    return {"detail": "Position deleted"}

@router.post("/", response_model=PositionResponseSchema)
def create_new_position(
    position: CreatePositionRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "create", "position"):
        raise HTTPException(status_code=403, detail="User does not have the required permissions")
    created_position = create_position(position)
    if not created_position:
        raise HTTPException(status_code=400, detail="Position already exists or an error occurred during creation")
    return created_position

@router.put("/{position_id}", response_model=PositionResponseSchema)
def update_position(
    position_id: str,
    position: UpdatePositionRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if not current_user.has_permission(db, "update", "position"):
        raise HTTPException(status_code=403, detail="User does not have the required permissions")
    updated_position = up(position_id=position_id,  updated_position=position)
    if not updated_position:
        raise HTTPException(status_code=404, detail="Position not found or already exists")
    return updated_position
