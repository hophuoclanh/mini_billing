from pydantic import BaseModel, Field
import uuid

class UserPositionSchema(BaseModel):
    user_position_id: str
    user_id: str
    position_id: str

    class Config:
        orm_mode = True

class CreateUserPositionRequestSchema(BaseModel):
    user_id: str
    role: str

class CreateUserPositionResponseSchema(UserPositionSchema):
    user_position_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        orm_mode = True
