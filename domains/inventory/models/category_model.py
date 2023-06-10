from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CategoryModel(Base):
    __tablename__ = 'category'

    category_id = Column(String(45), primary_key=True)
    category_name = Column(String(45), nullable=False)
