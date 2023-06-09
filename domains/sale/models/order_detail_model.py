from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OrderDetailModel(Base):
    __tablename__ = 'order_detail'

    order_detail_id = Column(String(45), primary_key=True)
    order_id = Column(String(45), nullable=False)
    product_id = Column(String(45), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    total_amount_per_product = Column(Float, nullable=False)
