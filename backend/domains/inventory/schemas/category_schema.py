from pydantic import BaseModel, Field
import uuid

class CategoryBaseSchema(BaseModel):
    category_name: str

    class Config:
        orm_mode = True

class CreateCategoryRequestSchema(CategoryBaseSchema):
    pass

class CategoryResponseSchema(CategoryBaseSchema):
    category_id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        orm_mode = True

class UpdateCategoryRequestSchema(CategoryBaseSchema):
    pass

class Config:
    orm_mode = True
