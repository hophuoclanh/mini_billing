from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'user'

    user_id = Column(String(36), primary_key=True)  # UUIDs are 36 characters long
    user_name = Column(String(45), nullable=False, unique=True)
    email = Column(String(45), nullable=False, unique=True)
    phone = Column(String(45), nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    password = Column(String(72), nullable=False)