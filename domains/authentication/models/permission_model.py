from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
import uuid
Base = declarative_base()

class PermissionModel(Base):
    __tablename__ = 'permission'

    permission_id = Column(String(45), primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String(10), nullable=False)
    resource = Column(String(50), nullable=False)