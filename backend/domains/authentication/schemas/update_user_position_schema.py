from pydantic import BaseModel

class UpdateUserPositionSchema(BaseModel):
    user_id: str
    position_id: str