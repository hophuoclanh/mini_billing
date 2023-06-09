from sqlalchemy.orm import Session
from sqlalchemy import exc
from fastapi import HTTPException
from domains.authentication.models.permission_model import PermissionModel
from domains.authentication.schemas.permission_schema import CreatePermissionSchema, PermissionResponseSchema

def get_all_permissions(db: Session):
    return db.query(PermissionModel).all()

def get_permission_by_id(permission_id: str, db: Session):
    permission = db.query(PermissionModel).filter(PermissionModel.permission_id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found.")
    return permission

def create_permission(permission: CreatePermissionSchema, db: Session) -> PermissionResponseSchema:
    db_permission = PermissionModel(**permission.dict())

    # Check if permission already exists
    existing_permission = db.query(PermissionModel).filter(
        PermissionModel.action == db_permission.action,
        PermissionModel.resource == db_permission.resource
    ).first()

    print("Existing permission:", existing_permission)  # Print the existing permission

    if existing_permission:
        print("Raising exception for existing permission...")  # Print a statement before raising the exception
        raise HTTPException(status_code=400, detail="Permission already exists")

    db.add(db_permission)
    try:
        db.commit()
        db.refresh(db_permission)
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error occurred during creation of Permission.")
    return PermissionResponseSchema(**db_permission.__dict__)


def update_permission(permission_id: str, permission: CreatePermissionSchema, db: Session) -> PermissionResponseSchema:
    db_permission = db.query(PermissionModel).filter(PermissionModel.permission_id == permission_id).first()

    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found.")

    # Check if updated permission already exists
    existing_permission = db.query(PermissionModel).filter(
        PermissionModel.action == permission.action,
        PermissionModel.resource == permission.resource
    ).first()

    if existing_permission and existing_permission.permission_id != permission_id:
        raise HTTPException(status_code=400, detail="Updated permission already exists.")

    for key, value in permission.dict().items():
        setattr(db_permission, key, value)
    try:
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error updating Permission.")
    return PermissionResponseSchema.from_orm(db_permission)

def delete_permission(permission_id: str, db: Session):
    db_permission = db.query(PermissionModel).filter(PermissionModel.permission_id == permission_id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found.")
    try:
        db.delete(db_permission)
        db.commit()
    except exc.IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error deleting Permission.")
    return {"detail": "Permission successfully deleted"}
