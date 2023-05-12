from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class PermissionModel(Base):
    __tablename__ = 'authentication_permission'

    permission_id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(5), nullable=False, unique=True)
    resource = Column(String(50), nullable=False, unique=True)
