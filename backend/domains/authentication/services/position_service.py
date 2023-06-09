from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from backend.domains.authentication.models.position_model import PositionModel
from backend.domains.authentication.schemas.position_schema import PositionResponseSchema, CreatePositionRequestSchema, UpdatePositionRequestSchema
from backend.repository import session
import uuid
from typing import List

def get_all_positions() -> List[PositionResponseSchema]:
    position_models = session.query(PositionModel).all()
    return [PositionResponseSchema.from_orm(position_model) for position_model in position_models]

def get_position_by_id(position_id: str) -> PositionModel:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    return position

def create_position(position: CreatePositionRequestSchema) -> PositionResponseSchema:
    position_dict = position.dict()
    existing_position = session.query(PositionModel).filter(PositionModel.role == position_dict['role']).first()
    if existing_position:
        return None
    position_dict['position_id'] = str(uuid.uuid4())
    position = PositionModel(**position_dict)
    session.add(position)
    try:
        session.commit()
        session.refresh(position)
    except IntegrityError:
        session.rollback()
        return None
    return PositionResponseSchema(**position_dict)

def update_position(position_id: str, updated_position: UpdatePositionRequestSchema) -> PositionResponseSchema:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        return None
    for key, value in updated_position.dict().items():
        if key == "position_id":  # Skip updating the position_id
            continue
        existing_position = session.query(PositionModel).filter(PositionModel.role == value).first()
        if existing_position and existing_position.position_id != position_id:
            return None
        setattr(position, key, value)
    try:
        session.commit()
        session.refresh(position)
    except IntegrityError:
        session.rollback()
        return None
    return PositionResponseSchema.from_orm(position)

def delete_position(position_id: str) -> None:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        return None
    session.delete(position)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        return None