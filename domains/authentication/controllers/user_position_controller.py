from fastapi import APIRouter, Depends, HTTPException
from dependencies.get_current_user import get_current_user
from domains.authentication.models.user_position_model import UserPositionModel
from domains.authentication.schemas.user_position_schema import CreateUserPositionResponseSchema, UserPositionSchema, CreateUserPositionRequestSchema
import domains.authentication.services.user_position_service as user_position_service
from domains.authentication.models.user_model import UserModel
from domains.authentication.schemas.update_user_position_schema import UpdateUserPositionSchema
from sqlalchemy.orm import Session
from repository import get_db
from typing import List

router = APIRouter()

@router.get('')
def get_all_user_positions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> list[UserPositionSchema]:
    if not current_user.has_permission(db, 'get', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to get user positions")
    user_positions = user_position_service.get_all_user_positions()
    return [UserPositionSchema.from_orm(user_position) for user_position in user_positions]

@router.get('/{user_position_id}')
def get_user_position_by_id(
    user_position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> UserPositionSchema:
    if not current_user.has_permission(db, 'get', 'user_position_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get a user position")
    return user_position_service.get_user_position_by_id(user_position_id)

@router.post('', response_model=List[UserPositionSchema])
def create_user_position(
    user_position: CreateUserPositionRequestSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> List[UserPositionSchema]:
    if not current_user.has_permission(db, 'create', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to create a user position")
    try:
        created_user_positions = user_position_service.create_user_position(user_position, db)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return created_user_positions

@router.put('/{user_position_id}')
def update_user_position(
    user_position_id: str,
    updated_user_position: UpdateUserPositionSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, 'update', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to update a user position")
    user_position_service.update_user_position(user_position_id, updated_user_position, db)

@router.delete('/{user_position_id}')
def delete_user_position(
    user_position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, 'delete', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete a user position")
    user_position_service.delete_user_position(user_position_id)
