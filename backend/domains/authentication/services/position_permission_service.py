from sqlalchemy.orm import Session
from domains.authentication.schemas.position_permission_schema import CreatePositionPermissionSchema, PositionPermissionSchema
from domains.authentication.models.position_permission_model import PositionPermissionModel
from fastapi import HTTPException
from domains.authentication.models.position_model import PositionModel
from domains.authentication.models.permission_model import PermissionModel
from sqlalchemy.exc import IntegrityError

def get_position_permission_by_id(position_permission_id: str, db: Session) -> PositionPermissionSchema:
    position_permission = db.query(PositionPermissionModel).filter(PositionPermissionModel.position_permission_id == position_permission_id).first()
    if not position_permission:
        raise HTTPException(status_code=404, detail='Position Permission not found')
    return PositionPermissionSchema.from_orm(position_permission)

def get_all_position_permissions(db: Session) -> list[PositionPermissionSchema]:
    position_permissions = db.query(PositionPermissionModel).all()
    return [PositionPermissionSchema.from_orm(pp) for pp in position_permissions]


def create_position_permission(position_permission: CreatePositionPermissionSchema,
                               db: Session) -> PositionPermissionSchema:
    # Check if position_id exists
    existing_position = db.query(PositionModel).filter(
        PositionModel.position_id == position_permission.position_id).first()
    if not existing_position:
        raise HTTPException(status_code=404, detail="Position does not exist.")

    # Check if permission_id exists
    existing_permission = db.query(PermissionModel).filter(
        PermissionModel.permission_id == position_permission.permission_id).first()
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission does not exist.")

    # Check for duplicates
    existing_position_permission = db.query(PositionPermissionModel).filter(
        PositionPermissionModel.position_id == position_permission.position_id,
        PositionPermissionModel.permission_id == position_permission.permission_id
    ).first()
    if existing_position_permission:
        raise HTTPException(status_code=400, detail="Position Permission already exists.")

    position_permission_db = PositionPermissionModel(**position_permission.dict())
    try:
        db.add(position_permission_db)
        db.commit()
        db.refresh(position_permission_db)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    return PositionPermissionSchema.from_orm(position_permission_db)

def update_position_permission(position_permission_id: str, position_permission: CreatePositionPermissionSchema,
                               db: Session) -> PositionPermissionSchema:
    position_permission_db = db.query(PositionPermissionModel).filter(
        PositionPermissionModel.position_permission_id == position_permission_id).first()
    if position_permission_db is None:
        raise HTTPException(status_code=404, detail="Position Permission not found")

    # Check if position_id exists
    existing_position = db.query(PositionModel).filter(PositionModel.position_id == position_permission.position_id).first()
    if not existing_position:
        raise HTTPException(status_code=404, detail="Position does not exist.")

    # Check if permission_id exists
    existing_permission = db.query(PermissionModel).filter(PermissionModel.permission_id == position_permission.permission_id).first()
    if not existing_permission:
        raise HTTPException(status_code=404, detail="Permission does not exist.")

    # Check for duplicates
    existing_position_permission = db.query(PositionPermissionModel).filter(
        PositionPermissionModel.position_id == position_permission.position_id,
        PositionPermissionModel.permission_id == position_permission.permission_id
    ).first()
    if existing_position_permission and existing_position_permission.position_permission_id != position_permission_id:
        raise HTTPException(status_code=400, detail="Position Permission already exists.")

    for key, value in position_permission.dict().items():
        setattr(position_permission_db, key, value)

    try:
        db.commit()
        db.refresh(position_permission_db)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database error: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Unexpected error: {str(e)}")
    finally:
        db.close()
    return PositionPermissionSchema.from_orm(position_permission_db)


def delete_position_permission(position_permission_id: str, db: Session) -> None:
    position_permission_db = db.query(PositionPermissionModel).filter(
        PositionPermissionModel.position_permission_id == position_permission_id).first()
    if position_permission_db is None:
        raise HTTPException(status_code=404, detail="Position Permission not found")

    try:
        db.delete(position_permission_db)
        db.commit()
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting Position Permission")
    finally:
        db.close()
