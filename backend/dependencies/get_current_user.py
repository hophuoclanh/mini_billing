from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from backend.domains.authentication.jwt import validate_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/authentication/login")

from backend.domains.authentication.models.user_model import UserModel

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    user = validate_access_token(token)
    return user


