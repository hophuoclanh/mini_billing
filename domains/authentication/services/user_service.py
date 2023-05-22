from fastapi import HTTPException
import re
from sqlalchemy.exc import IntegrityError
import bcrypt
from domains.authentication.models.user_model import UserModel
from domains.authentication.schemas.user_schema import CreateUserRequestSchema, CreateUserResponseSchema
from domains.authentication.schemas.update_user_schema import UpdateUserSchema
from repository import session
import uuid

def get_all_users() -> list[UserModel]:
    return session.query(UserModel).all()

def get_user_by_id(user_id: str) -> UserModel:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

def create_user(user: CreateUserRequestSchema) -> CreateUserResponseSchema:
    try:
        user_dict = user.dict()
        user_dict['user_id'] = str(uuid.uuid4())
        user = UserModel(**user_dict)

        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
        session.add(user)
        session.commit()
        session.refresh(user)

        # Return the created user
        return CreateUserResponseSchema(**user_dict)
    except IntegrityError as e:
        # Check if the error is due to a duplicate entry
        if '1062' in str(e.orig):
            # Extract the name of the duplicated field from the error message
            field_match = re.search(r"key '(\w+)_UNIQUE'", str(e.orig))
            if field_match:
                field_name = field_match.group(1)
                raise HTTPException(status_code=409, detail=f'{field_name} already exists')
            else:
                raise HTTPException(status_code=409, detail='User already exists')
        else:
            raise HTTPException(status_code=500, detail='Error occurred during user creation')
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error occurred during user creation')

def update_user(user_id: str, updated_user: UpdateUserSchema) -> None:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    user.user_name = updated_user.user_name
    user.email = updated_user.email
    user.phone = updated_user.phone
    user.address = updated_user.address
    salt = bcrypt.gensalt()
    user.password = bcrypt.hashpw(updated_user.password.encode('utf-8'), salt)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError as e:
        # Check if the error is due to a duplicate entry and handle it accordingly
        # (refer to the create_user function for how to do this)
        session.rollback()
        raise HTTPException(status_code=500, detail='Error occurred during user update')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Error occurred during user update')
def delete_user(user_id: str) -> None:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    try:
        session.delete(user)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Error occurred during user deletion')
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail='Error occurred during user deletion')