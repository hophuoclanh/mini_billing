from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
