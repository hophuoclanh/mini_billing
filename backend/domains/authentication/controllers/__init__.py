from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import bcrypt
from backend.dependencies.get_current_user import get_current_user
from backend.domains.authentication.controllers.user_controller import router as user_controller
from backend.domains.authentication.controllers.position_controller import router as position_controller
from backend.domains.authentication.controllers.user_position_controller import router as user_position_controller
from backend.domains.authentication.controllers.permission_controller import router as permission_controller
from backend.domains.authentication.controllers.position_permission_controller import router as position_permission_controller
from backend.domains.authentication.jwt import create_access_token
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.authentication.schemas.authentication_schema import LoginResponseSchema
from backend.domains.authentication.schemas.user_schema import UserSchema
from backend.domains.authentication.schemas.permission_schema import PermissionResponseSchema
from backend.dependencies.get_permission_for_position import get_permissions_for_role
from backend.repository import get_db  # You should use the get_db function from dependencies

router = APIRouter(tags=['Authentication'])
router.include_router(user_controller, prefix='/user')
router.include_router(position_controller, prefix="/position")
router.include_router(user_position_controller, prefix="/user_position")
router.include_router(permission_controller, prefix="/permission")
router.include_router(position_permission_controller, prefix="/position_permission")

@router.post('/login', response_model=LoginResponseSchema)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> LoginResponseSchema:
    user = db.query(UserModel).filter(UserModel.user_name == form_data.username).first()

    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    if not bcrypt.checkpw(form_data.password.encode('utf-8'), str(user.password).encode('utf-8')):
        raise HTTPException(status_code=401, detail='Wrong password')
    access_token = create_access_token(user.user_id)

    return LoginResponseSchema(access_token=access_token)


@router.get('/me', response_model=UserSchema)
def get_me(current_user: UserModel = Depends(get_current_user)) -> UserSchema:  # Changed UserSchema to UserModel
    return current_user

@router.get("/position/permissions/{role}")
def read_role_permissions(role: str, db: Session = Depends(get_db)) -> list[PermissionResponseSchema]:
    permissions = get_permissions_for_role(db, role)
    return [PermissionResponseSchema.from_orm(permission) for permission in permissions]



