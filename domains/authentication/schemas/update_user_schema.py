from pydantic import BaseModel

class UpdateUserSchema(BaseModel):
    user_name: str
    email: str
    phone: str
    address: str
    password: str