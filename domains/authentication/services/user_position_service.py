from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.authentication.models.user_position_model import UserPositionModel
from domains.authentication.schemas.user_position_schema import CreateUserPositionRequestSchema, CreateUserPositionResponseSchema
from domains.authentication.schemas.update_user_position_schema import UpdateUserPositionSchema
from repository import session
from sqlalchemy.orm.exc import NoResultFound
import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

# Import your database models and schemas
from domains.authentication.models.user_model import UserModel
from domains.authentication.models.position_model import PositionModel
from domains.authentication.schemas.user_schema import UserSchema
from domains.authentication.schemas.position_schema import PositionSchema
from typing import List
def get_all_user_positions() -> list[UserPositionModel]:
    return session.query(UserPositionModel).all()

def get_user_position_by_id(user_position_id: str) -> UserPositionModel:
    user_position = session.query(UserPositionModel).filter(UserPositionModel.user_position_id == user_position_id).first()
    if not user_position:
        raise HTTPException(status_code=404, detail='User-Position not found')
    return user_position

# List of positions in hierarchical order
POSITIONS = ['admin', 'manager', 'casher']

def create_user_position(user_position: CreateUserPositionRequestSchema, db: Session) -> List[CreateUserPositionResponseSchema]:
    created_positions = []  # List to store created UserPosition objects

    try:
        # Check if the user exists
        user = get_user_by_id(user_position.user_id, db)

        if user_position.role not in POSITIONS:
            raise HTTPException(status_code=400, detail="Invalid role")

        # Start from the assigned position and create user_positions for all following positions
        for role in POSITIONS[POSITIONS.index(user_position.role):]:
            # Query the position based on the role
            position = db.query(PositionModel).filter(PositionModel.role == role).first()
            if not position:
                raise HTTPException(status_code=404, detail="Position not found")

            # Check if the user-position combination already exists
            existing_user_position = db.query(UserPositionModel).filter(
                UserPositionModel.user_id == user_position.user_id,
                UserPositionModel.position_id == position.position_id
            ).first()

            if existing_user_position:
                raise HTTPException(status_code=409, detail=f"User-Position for {role} already exists.")

            # If not, create a new user-position
            new_user_position = UserPositionModel(user_id=user_position.user_id, position_id=position.position_id)
            new_user_position.user_position_id = str(uuid.uuid4())

            db.add(new_user_position)

            # Add the created user position to the list
            created_positions.append(CreateUserPositionResponseSchema.from_orm(new_user_position))

        db.commit()  # commit only once at the end

    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="User-Position already exists.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    # Return the list of created user positions
    return created_positions

def delete_user_position(user_position_id: str) -> None:
    user_position = get_user_position_by_id(user_position_id)
    try:
        session.delete(user_position)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e

def update_user_position(user_position_id: str, updated_user_position: UpdateUserPositionSchema, db: Session) -> None:
    try:# Check if the user and position exist
        user = get_user_by_id(updated_user_position.user_id, db)
        position = get_position_by_id(updated_user_position.position_id, db)

        existing_user_position = db.query(UserPositionModel).filter(
            UserPositionModel.user_id == updated_user_position.user_id,
            UserPositionModel.position_id == updated_user_position.position_id
        ).one()
        if existing_user_position.user_position_id != user_position_id:
            raise HTTPException(status_code=409, detail="User-Position already exists.")
    except NoResultFound:
        pass

    try:
        user_position = db.query(UserPositionModel).filter(UserPositionModel.user_position_id == user_position_id).one()
        user_position.user_id = updated_user_position.user_id
        user_position.position_id = updated_user_position.position_id
        db.commit()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="User-Position not found.")
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_id(user_id: str, db: Session) -> UserSchema:
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserSchema.from_orm(user)

def get_position_by_id(position_id: str, db: Session) -> PositionSchema:
    position = db.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return PositionSchema.from_orm(position)

def get_position_by_name(role: str, db: Session) -> PositionSchema:
    position = db.query(PositionModel).filter(PositionModel.role == role).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return PositionSchema.from_orm(position)
