from jose import JWTError, jwt
from fastapi import HTTPException, status
import os
from datetime import timedelta, datetime
from domains.authentication.models.user_model import UserModel
from domains.authentication.services.user_service import get_user_by_id

secret = os.getenv('JWT_SECRET')
if not secret:
    raise ValueError('JWT_SECRET environment variable not set')
expires_in_seconds = int(os.getenv('JWT_EXPIRES_IN_SECONDS', 7 * 24 * 60 * 60))  # 7 days in seconds
algorithm = 'HS256'

def create_access_token(user_id):
    current_time = datetime.utcnow()
    payload = {
        'sub': str(user_id),
        'exp': current_time + timedelta(seconds=expires_in_seconds),
    }
    access_token = jwt.encode(payload, secret, algorithm=algorithm)
    return access_token

def validate_access_token(access_token: str) -> UserModel:
    try:
        payload = jwt.decode(access_token, secret, algorithms=['HS256'])
        user_id = str(payload.get('sub'))
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is not in the correct format')
        user = get_user_by_id(user_id)
        if not isinstance(user, UserModel):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid User')
        return user
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid')


