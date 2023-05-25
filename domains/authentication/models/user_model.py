from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from domains.authentication.models.permission_model import PermissionModel
from domains.authentication.models.position_permission_model import PositionPermissionModel

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'

    user_id = Column(String(36), primary_key=True)  # UUIDs are 36 characters long
    user_name = Column(String(45), nullable=False)
    email = Column(String(45), nullable=False)
    phone = Column(String(45), nullable=False)
    address = Column(String(255), nullable=False)
    password = Column(String(72), nullable=False)
