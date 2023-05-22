from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class PositionModel(Base):
    __tablename__ = 'position'

    position_id = Column(String(45), primary_key=True)
    role = Column(String(45), nullable=False)