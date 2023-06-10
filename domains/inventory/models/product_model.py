from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'product'

    product_id = Column(String(45), primary_key=True)
    product_name = Column(String(45), nullable=False)
    description = Column(String(255), nullable=False)
    category_id = Column(String(45), nullable=False)
    unit_price = Column(Float, nullable=False)
    unit_in_stock = Column(Integer, nullable=False)
