import re
from sqlalchemy.exc import IntegrityError
import bcrypt
from backend.domains.authentication.models.user_model import UserModel
from backend.domains.authentication.schemas.user_schema import UserSchema, CreateUserRequestSchema, CreateUserResponseSchema
from backend.domains.authentication.schemas.update_user_schema import UpdateUserSchema
from backend.repository import session
import uuid
from backend.domains.authentication.exceptions import UserAlreadyExistsError
from sqlalchemy.exc import SQLAlchemyError


def get_all_users() -> list[UserModel]:
    return session.query(UserModel).all()

def get_user_by_id(user_id: str) -> UserModel:
    user = session.query(UserModel).filter(UserModel.user_id == user_id).first()
    if not user:
        raise ValueError('User not found')
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
        session.rollback()
        if '1062' in str(e.orig):
            field_match = re.search(r"key '(\w+)_UNIQUE'", str(e.orig))
            if field_match:
                field_name = field_match.group(1)
                raise ValueError(f'{field_name} already exists')
            else:
                raise ValueError('User already exists')
        else:
            raise Exception('Error occurred during user creation')
    except Exception as e:
        raise Exception('Error occurred during user creation')

def update_user(user_id: str, updated_user: UpdateUserSchema) -> UserSchema:
    user = get_user_by_id(user_id)
    if updated_user.user_name is not None:
        user.user_name = updated_user.user_name
    if updated_user.email is not None:
        user.email = updated_user.email
    if updated_user.phone is not None:
        user.phone = updated_user.phone
    if updated_user.address is not None:
        user.address = updated_user.address
    if updated_user.password is not None:
        salt = bcrypt.gensalt()
        user.password = bcrypt.hashpw(updated_user.password.encode('utf-8'), salt)

    try:
        session.commit()
        session.refresh(user)
    except IntegrityError as e:
        session.rollback()
        if 'duplicate key value violates unique constraint' in str(e.orig):
            field_match = re.search(r'DETAIL:  Key \((.*?)\)=', str(e.orig))
            if field_match:
                field_name = field_match.group(1)
                raise UserAlreadyExistsError(f'{field_name} already exists')  # <- Raise the custom exception here
            else:
                raise UserAlreadyExistsError('User already exists')
    except SQLAlchemyError as e:
        session.rollback()
        print(f"SQLAlchemy error: {str(e)}")
    except Exception as e:
        session.rollback()
        raise Exception(f'Unexpected error occurred during user update: {str(e)}')

    return UserSchema.from_orm(user)


def delete_user(user_id: str) -> None:
    user = get_user_by_id(user_id)
    try:
        session.delete(user)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        raise Exception('Error occurred during user deletion')
    except Exception as e:
        session.rollback()
        raise Exception('Error occurred during user deletion')