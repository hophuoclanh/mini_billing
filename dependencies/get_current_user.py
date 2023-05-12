from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from domains.authentication.jwt import validate_access_token

from domains.authentication.schemas.user_schema import UserSchema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/authentication/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserSchema:
    return validate_access_token(token)
