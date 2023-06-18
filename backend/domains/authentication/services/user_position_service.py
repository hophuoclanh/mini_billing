from sqlalchemy.exc import IntegrityError
from backend.domains.authentication.models.user_position_model import UserPositionModel
from backend.domains.authentication.schemas.user_position_schema import CreateUserPositionRequestSchema, CreateUserPositionResponseSchema
from backend.domains.authentication.schemas.update_user_position_schema import UpdateUserPositionSchema
from backend.repository import session
from sqlalchemy.orm.exc import NoResultFound
import uuid
from sqlalchemy.orm import Session

# Import your database models and schemas
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.authentication.models.position_model import PositionModel
from backend.domains.authentication.schemas.user_schema import UserSchema
from backend.domains.authentication.schemas.position_schema import PositionSchema
from typing import List
def get_all_user_positions() -> list[UserPositionModel]:
    return session.query(UserPositionModel).all()

def get_user_position_by_id(user_position_id: str) -> UserPositionModel:
    user_position = session.query(UserPositionModel).filter(UserPositionModel.user_position_id == user_position_id).first()
    if not user_position:
        raise ValueError('User-Position not found')
    return user_position

# List of positions in hierarchical order
POSITIONS = ['admin', 'manager', 'casher']

def create_user_position(user_position: CreateUserPositionRequestSchema, db: Session) -> List[CreateUserPositionResponseSchema]:
    created_positions = []
    try:
        user = get_user_by_id(user_position.user_id, db)
        if user_position.role not in POSITIONS:
            raise ValueError("Invalid role")
        for role in POSITIONS[POSITIONS.index(user_position.role):]:
            position = db.query(PositionModel).filter(PositionModel.role == role).first()
            if not position:
                raise ValueError("Position not found")
            existing_user_position = db.query(UserPositionModel).filter(
                UserPositionModel.user_id == user_position.user_id,
                UserPositionModel.position_id == position.position_id
            ).first()
            if existing_user_position:
                raise ValueError(f"User-Position for {role} already exists.")
            new_user_position = UserPositionModel(user_id=user_position.user_id, position_id=position.position_id)
            new_user_position.user_position_id = str(uuid.uuid4())
            db.add(new_user_position)
            created_positions.append(CreateUserPositionResponseSchema.from_orm(new_user_position))
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("User-Position already exists.")
    except Exception as e:
        db.rollback()
        raise e
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
    try:
        user = get_user_by_id(updated_user_position.user_id, db)
        position = get_position_by_id(updated_user_position.position_id, db)
        existing_user_position = db.query(UserPositionModel).filter(
            UserPositionModel.user_id == updated_user_position.user_id,
            UserPositionModel.position_id == updated_user_position.position_id
        ).one()
        if existing_user_position.user_position_id != user_position_id:
            raise ValueError("User-Position already exists.")
    except NoResultFound:
        pass
    try:
        user_position = db.query(UserPositionModel).filter(UserPositionModel.user_position_id == user_position_id).one()
        user_position.user_id = updated_user_position.user_id
        user_position.position_id = updated_user_position.position_id
        db.commit()
    except NoResultFound:
        raise ValueError("User-Position not found.")
    except Exception as e:
        db.rollback()
        raise e

def get_user_by_id(user_id: str, db: Session) -> UserSchema:
    user = db.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise ValueError("User not found")
    return UserSchema.from_orm(user)

def get_position_by_id(position_id: str, db: Session) -> PositionSchema:
    position = db.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        raise ValueError("Position not found")
    return PositionSchema.from_orm(position)

def get_position_by_name(role: str, db: Session) -> PositionSchema:
    position = db.query(PositionModel).filter(PositionModel.role == role).first()
    if not position:
        raise ValueError("Position not found")
    return PositionSchema.from_orm(position)
