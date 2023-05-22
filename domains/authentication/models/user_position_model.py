from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
import uuid

class UserPositionModel(Base):
    __tablename__ = 'user_position'

    user_position_id = Column(String(45), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(45))
    position_id = Column(String(45))