from pydantic import BaseModel, Field
import uuid

class PositionBaseSchema(BaseModel):
    role: str

class CreatePositionRequestSchema(PositionBaseSchema):
    pass

class PositionResponseSchema(PositionBaseSchema):
    position_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class UpdatePositionRequestSchema(PositionBaseSchema):
    pass

class PositionSchema(BaseModel):
    position_id: str
    role: str

    class Config:
        orm_mode = True