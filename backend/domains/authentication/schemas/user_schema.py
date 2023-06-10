from pydantic import BaseModel, Field
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
    user_name: str
    email: str
    phone: str
    address: str
    password: str

# Use this schema for outgoing data
class CreateUserResponseSchema(BaseModel):
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_name: str
    email: str
    phone: str
    address: str
    password: str