from fastapi import APIRouter, Depends, HTTPException
from backend.dependencies.get_current_user import get_current_user
from backend.domains.authentication.schemas.user_position_schema import UserPositionSchema, CreateUserPositionRequestSchema
import backend.domains.authentication.services.user_position_service as user_position_service
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.authentication.schemas.update_user_position_schema import UpdateUserPositionSchema
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from backend.repository import get_db
from typing import List

router = APIRouter()

@router.get('')
def get_all_user_positions(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> list[UserPositionSchema]:
    if not current_user.has_permission(db, 'get', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to get user positions")
    try:
        user_positions = user_position_service.get_all_user_positions()
        return [UserPositionSchema.from_orm(user_position) for user_position in user_positions]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get('/{user_position_id}')
def get_user_position_by_id(
    user_position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> UserPositionSchema:
    if not current_user.has_permission(db, 'get', 'user_position_by_id'):
        raise HTTPException(status_code=403, detail="User does not have permission to get a user position")
    try:
        return user_position_service.get_user_position_by_id(user_position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        return created_user_positions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{user_position_id}')
def update_user_position(
    user_position_id: str,
    updated_user_position: UpdateUserPositionSchema,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, 'update', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to update a user position")
    try:
        user_position_service.update_user_position(user_position_id, updated_user_position, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User-Position not found.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete('/{user_position_id}')
def delete_user_position(
    user_position_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
) -> None:
    if not current_user.has_permission(db, 'delete', 'user_position'):
        raise HTTPException(status_code=403, detail="User does not have permission to delete a user position")
    try:
        user_position_service.delete_user_position(user_position_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
