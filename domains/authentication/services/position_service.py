from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from domains.authentication.models.position_model import PositionModel
from domains.authentication.schemas.position_schema import PositionResponseSchema, CreatePositionRequestSchema, UpdatePositionRequestSchema
from repository import session
import uuid

def get_all_positions() -> list[PositionModel]:
    return session.query(PositionModel).all()

def get_position_by_id(position_id: str) -> PositionModel:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail='Position not found')
    return position

def create_position(position: CreatePositionRequestSchema) -> PositionResponseSchema:
    position_dict = position.dict()
    existing_position = session.query(PositionModel).filter(PositionModel.role == position_dict['role']).first()
    if existing_position:
        raise HTTPException(status_code=400, detail="Position already exists.")
    position_dict['position_id'] = str(uuid.uuid4())
    position = PositionModel(**position_dict)
    session.add(position)
    try:
        session.commit()
        session.refresh(position)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Position.")
    return PositionResponseSchema(**position_dict)

def update_position(position_id: str, updated_position: UpdatePositionRequestSchema) -> PositionResponseSchema:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail='Position not found')
    for key, value in updated_position.dict().items():
        if key == "position_id":  # Skip updating the position_id
            continue
        existing_position = session.query(PositionModel).filter(PositionModel.role == value).first()
        if existing_position and existing_position.position_id != position_id:
            raise HTTPException(status_code=400, detail="Position already exists.")
        setattr(position, key, value)
    try:
        session.commit()
        session.refresh(position)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during update of Position.")
    return PositionResponseSchema.from_orm(position)

def delete_position(position_id: str) -> None:
    position = session.query(PositionModel).filter(PositionModel.position_id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail='Position not found')
    session.delete(position)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during deletion of Position.")