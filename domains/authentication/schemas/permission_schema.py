from pydantic import BaseModel, Field
import uuid

class PermissionBaseSchema(BaseModel):
    action: str
    resource: str

class CreatePermissionSchema(PermissionBaseSchema):
    pass

class CreatePermissionRequestSchema(BaseModel):
    action: str
    resource: str

class PermissionResponseSchema(BaseModel):
    permission_id: uuid.UUID = Field(default_factory=lambda: str(uuid.uuid4()))
    action: str
    resource: str

    class Config:
        orm_mode = True
