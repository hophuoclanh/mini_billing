import string
from typing import re
from pydantic import BaseModel, Field, validator
import uuid

class UserSchema(BaseModel):
    user_id: str
    user_name: str
    email: str
    phone: str
    address: str

    class Config:
        orm_mode = True

# Use this schema for incoming data
class CreateUserRequestSchema(BaseModel):
    user_name: str = Field(..., min_length=1, max_length=45)
    email: str = Field(..., min_length=5, max_length=45)  # EmailStr doesn't support max_length
    phone: str = Field(..., min_length=1, max_length=45, regex=r"^\S+$")  # No whitespace allowed, length 1-45
    address: str = Field(..., min_length=1, max_length=255)
    password: str = Field(..., min_length=1, max_length=72)  # Minimum password length 1

# Use this schema for outgoing data
class CreateUserResponseSchema(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str
    email: str
    phone: str
    address: str
    password: str