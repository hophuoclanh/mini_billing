from pydantic import BaseModel
from typing import Optional

class UpdateUserSchema(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    password: Optional[str] = None
