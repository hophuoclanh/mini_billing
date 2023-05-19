from pydantic import BaseModel, Field
import uuid

class PositionPermissionBase(BaseModel):
    position_id: str
    permission_id: str

class CreatePositionPermissionSchema(PositionPermissionBase):
    pass

class PositionPermissionSchema(PositionPermissionBase):
    position_permission_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        orm_mode = True