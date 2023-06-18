from sqlalchemy.orm import Session
from backend.domains.authentication.schemas.position_permission_schema import CreatePositionPermissionSchema, PositionPermissionSchema
from backend.domains.authentication.models.position_permission_model import PositionPermissionModel
from backend.domains.authentication.models.position_model import PositionModel
from backend.domains.authentication.models.permission_model import PermissionModel
from typing import Optional

def get_position_permission_by_id(position_permission_id: str, db: Session) -> Optional[PositionPermissionSchema]:
    position_permission = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_permission_id == position_permission_id).first()
    if position_permission:
        return PositionPermissionSchema.from_orm(position_permission)
    return None

def get_all_position_permissions(db: Session) -> list[PositionPermissionSchema]:
    position_permissions = db.query(PositionPermissionModel).all()
    return [PositionPermissionSchema.from_orm(pp) for pp in position_permissions]

def create_position_permission(position_permission: CreatePositionPermissionSchema, db: Session) -> Optional[PositionPermissionSchema]:
    existing_position = db.query(PositionModel).filter(PositionModel.position_id == position_permission.position_id).first()
    existing_permission = db.query(PermissionModel).filter(PermissionModel.permission_id == position_permission.permission_id).first()
    existing_position_permission = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_id == position_permission.position_id, PositionPermissionModel.permission_id == position_permission.permission_id).first()
    if not existing_position or not existing_permission or existing_position_permission:
        return None
    position_permission_db = PositionPermissionModel(**position_permission.dict())
    try:
        db.add(position_permission_db)
        db.commit()
        db.refresh(position_permission_db)
    except:
        db.rollback()
        return None
    return PositionPermissionSchema.from_orm(position_permission_db)

def update_position_permission(position_permission_id: str, position_permission: CreatePositionPermissionSchema, db: Session) -> Optional[PositionPermissionSchema]:
    position_permission_db = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_permission_id == position_permission_id).first()
    existing_position = db.query(PositionModel).filter(PositionModel.position_id == position_permission.position_id).first()
    existing_permission = db.query(PermissionModel).filter(PermissionModel.permission_id == position_permission.permission_id).first()
    existing_position_permission = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_id == position_permission.position_id, PositionPermissionModel.permission_id == position_permission.permission_id).first()
    if not position_permission_db or not existing_position or not existing_permission or (existing_position_permission and existing_position_permission.position_permission_id != position_permission_id):
        return None
    for key, value in position_permission.dict().items():
        setattr(position_permission_db, key, value)
    try:
        db.commit()
        db.refresh(position_permission_db)
    except:
        db.rollback()
        return None
    return PositionPermissionSchema.from_orm(position_permission_db)


def delete_position_permission(position_permission_id: str, db: Session) -> bool:
    position_permission_db = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_permission_id == position_permission_id).first()
    if position_permission_db is None:
        return False
    try:
        db.delete(position_permission_db)
        db.commit()
    except:
        db.rollback()
        return False
    return True