from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import uuid

class PositionPermissionModel(Base):
    __tablename__ = 'position_permission'

    position_permission_id = Column(String(45), primary_key=True, default=lambda: str(uuid.uuid4()))
    position_id = Column(String(45), unique=True)
    permission_id = Column(String(45), unique=True)

